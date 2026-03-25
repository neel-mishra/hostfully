import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { AuthManager } from "../utils/auth.js";
import {
  ExchangeCodeSchema,
  GenerateAuthUrlSchema,
  GenerateSystemTokenSchema,
  RefreshTokenSchema,
} from "../types/mcp-tools.js";
import { errorResult, jsonResult } from "../utils/mcp-response.js";

export function registerOAuthTools(server: McpServer, authManager: AuthManager) {
  server.tool("generate_auth_url", GenerateAuthUrlSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { scopes, state } = args;
      const authUrl = authManager.generateAuthUrl(scopes, state);

      const response = {
        success: true,
        authorization_url: authUrl,
        scopes_requested: scopes,
        instructions: [
          "1. Open the authorization URL in a web browser",
          "2. Log in to your Facebook account",
          "3. Grant the requested permissions to your app",
          "4. Copy the authorization code from the redirect URL",
          "5. Use the 'exchange_code_for_token' tool with the authorization code",
        ],
        security_note: state ? "State parameter included for CSRF protection" : "Consider adding a state parameter for additional security",
        redirect_uri: (authManager as any)["config"]?.redirectUri,
      };

      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error generating authorization URL: ${msg}`);
    }
  });

  server.tool("exchange_code_for_token", ExchangeCodeSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { code } = args;
      const result = await authManager.exchangeCodeForToken(code);

      const response = {
        success: true,
        message: "Authorization code exchanged successfully",
        token_info: {
          access_token: result.accessToken,
          token_type: result.tokenType,
          expires_in: result.expiresIn,
          expires_at: result.expiresIn ? new Date(Date.now() + result.expiresIn * 1000).toISOString() : undefined,
        },
        next_steps: [
          "Token is now active and will be used for API calls",
          "Consider exchanging for a long-lived token using 'refresh_to_long_lived_token'",
          "Store the token securely for future use",
        ],
        recommendations: [
          "Long-lived tokens last ~60 days vs ~1-2 hours for short-lived tokens",
          "Enable auto-refresh by setting META_AUTO_REFRESH=true",
          "Monitor token expiration and refresh before it expires",
        ],
      };

      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error exchanging authorization code: ${msg}`);
    }
  });

  server.tool("refresh_to_long_lived_token", RefreshTokenSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { short_lived_token } = args;
      const result = await authManager.exchangeForLongLivedToken(short_lived_token);

      const response = {
        success: true,
        message: "Token successfully exchanged for long-lived token",
        token_info: {
          access_token: result.accessToken,
          token_type: result.tokenType,
          expires_in: result.expiresIn,
          expires_at: new Date(Date.now() + result.expiresIn * 1000).toISOString(),
          lifetime: "Approximately 60 days",
        },
        token_management: {
          auto_refresh_enabled: !!(authManager as any)["config"]?.autoRefresh,
          current_expiration: (authManager as any)["config"]?.tokenExpiration?.toISOString(),
          refresh_recommendation: "Set up automatic refresh or manually refresh before expiration",
        },
        environment_variables: {
          META_ACCESS_TOKEN: "Update with the new long-lived token",
          META_AUTO_REFRESH: "Set to 'true' to enable automatic refresh",
        },
      };

      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error refreshing to long-lived token: ${msg}`);
    }
  });

  server.tool(
    "generate_system_user_token",
    GenerateSystemTokenSchema.shape as any,
    async (args: any, _extra: any) => {
      try {
        const { system_user_id, scopes, expiring_token } = args;
        const result = await authManager.generateSystemUserToken(system_user_id, scopes, expiring_token);

        const response = {
          success: true,
          message: "System user token generated successfully",
          system_user_id,
          token_info: {
            access_token: result.accessToken,
            token_type: result.tokenType,
            expires_in: result.expiresIn,
            expires_at: result.expiresIn ? new Date(Date.now() + result.expiresIn * 1000).toISOString() : "Never (non-expiring token)",
            scopes,
          },
          token_characteristics: {
            type: expiring_token ? "Expiring (60 days)" : "Non-expiring",
            use_case: "Server-to-server automation",
            security_level: "High - requires Business Manager admin access",
          },
          recommendations: [
            "Store the system user token securely",
            "Use for automated, server-side operations",
            "Monitor token usage and permissions",
            expiring_token ? "Set up refresh mechanism before 60-day expiration" : "Non-expiring tokens require manual revocation if compromised",
          ],
        };

        return jsonResult(response);
      } catch (error) {
        const msg = error instanceof Error ? error.message : "Unknown error occurred";
        return errorResult(`Error generating system user token: ${msg}`);
      }
    },
  );

  server.tool("get_token_info", {}, async () => {
    try {
      const tokenInfo = await authManager.getTokenInfo();

      const response = {
        token_info: tokenInfo,
        current_config: {
          has_app_credentials: !!((authManager as any)["config"]?.appId && (authManager as any)["config"]?.appSecret),
          has_redirect_uri: !!(authManager as any)["config"]?.redirectUri,
          auto_refresh_enabled: !!(authManager as any)["config"]?.autoRefresh,
          token_expiration: (authManager as any)["config"]?.tokenExpiration?.toISOString(),
        },
        token_status: {
          is_valid: tokenInfo.isValid,
          is_expiring_soon: authManager.isTokenExpiring(60),
          requires_refresh: authManager.isTokenExpiring(5),
        },
      };

      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error getting token info: ${msg}`);
    }
  });

  server.tool("validate_token", {}, async () => {
    try {
      const isValid = await authManager.validateToken();
      const tokenInfo = await authManager.getTokenInfo();

      const response = {
        is_valid: isValid,
        validation_timestamp: new Date().toISOString(),
        token_details: tokenInfo,
      };

      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error validating token: ${msg}`);
    }
  });
}

