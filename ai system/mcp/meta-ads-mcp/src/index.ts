#!/usr/bin/env node

import { config } from "dotenv";
config({ path: ".env.local" });

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { MetaApiClient } from "./meta-client.js";
import { AuthManager } from "./utils/auth.js";

import { registerCampaignTools } from "./tools/campaigns.js";
import { registerAnalyticsTools } from "./tools/analytics.js";
import { registerAudienceTools } from "./tools/audiences.js";
import { registerCreativeTools } from "./tools/creatives.js";
import { registerOAuthTools } from "./tools/oauth.js";

import { registerCampaignResources } from "./resources/campaigns.js";
import { registerInsightsResources } from "./resources/insights.js";
import { registerAudienceResources } from "./resources/audiences.js";

async function main() {
  try {
    console.error("🚀 Starting Meta Marketing API MCP Server...");
    console.error("📋 Environment check:");
    console.error(` NODE_VERSION: ${process.version}`);
    console.error(` META_ACCESS_TOKEN: ${process.env.META_ACCESS_TOKEN ? "Present" : "Missing"}`);
    console.error(` MCP_SERVER_NAME: ${process.env.MCP_SERVER_NAME || "Not set"}`);

    console.error("🔐 Initializing authentication...");
    const auth = AuthManager.fromEnvironment();
    console.error("✅ Auth manager created successfully");

    console.error("🔍 Validating Meta access token...");
    try {
      const currentToken = await auth.refreshTokenIfNeeded();
      console.error("✅ Token validation and refresh successful");
      console.error(`🔑 Token ready: ${currentToken.substring(0, 20)}...`);

      const hasOAuthConfig = !!(process.env.META_APP_ID && process.env.META_APP_SECRET);
      console.error(`🔧 OAuth configuration: ${hasOAuthConfig ? "Available" : "Not configured"}`);
      console.error(`🔄 Auto-refresh: ${process.env.META_AUTO_REFRESH === "true" ? "Enabled" : "Disabled"}`);
    } catch (error) {
      console.error("❌ Token validation failed:", error);
      console.error("💡 Use OAuth tools to obtain a new token or check configuration");
      process.exit(1);
    }

    console.error("🌐 Initializing Meta API client...");
    const metaClient = new MetaApiClient(auth);
    console.error("✅ Meta API client created successfully");

    console.error("🔧 Initializing MCP Server...");
    const server = new McpServer({
      name: process.env.MCP_SERVER_NAME || "Meta Marketing API Server",
      version: process.env.MCP_SERVER_VERSION || "1.0.0",
    });
    console.error("✅ MCP Server instance created");

    console.error("🛠️ Registering tools...");
    registerCampaignTools(server, metaClient);
    console.error(" ✅ Campaign tools registered");
    registerAnalyticsTools(server, metaClient);
    console.error(" ✅ Analytics tools registered");
    registerAudienceTools(server, metaClient);
    console.error(" ✅ Audience tools registered");
    registerCreativeTools(server, metaClient);
    console.error(" ✅ Creative tools registered");
    registerOAuthTools(server, auth);
    console.error(" ✅ OAuth tools registered");

    console.error("📚 Registering resources...");
    registerCampaignResources(server, metaClient);
    console.error(" ✅ Campaign resources registered");
    registerInsightsResources(server, metaClient);
    console.error(" ✅ Insights resources registered");
    registerAudienceResources(server, metaClient);
    console.error(" ✅ Audience resources registered");

    // Basic tools (account discovery + server health)
    server.tool("get_ad_accounts", {}, async () => {
      try {
        const accounts = await metaClient.getAdAccounts();
        const accountsData = accounts.map((account) => ({
          id: account.id,
          name: account.name,
          account_status: account.account_status,
          currency: account.currency,
          timezone_name: account.timezone_name,
          balance: account.balance,
          business: account.business ? { id: account.business.id, name: account.business.name } : null,
        }));

        const response = {
          success: true,
          accounts: accountsData,
          total_accounts: accountsData.length,
          message: "Ad accounts retrieved successfully",
        };

        return { content: [{ type: "text", text: JSON.stringify(response, null, 2) }] };
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : "Unknown error occurred";
        return {
          content: [{ type: "text", text: `Error getting ad accounts: ${errorMessage}` }],
          isError: true,
        };
      }
    });

    server.tool("health_check", {}, async () => {
      try {
        const accounts = await metaClient.getAdAccounts();
        const response = {
          status: "healthy",
          server_name: process.env.MCP_SERVER_NAME || "Meta Marketing API Server",
          version: process.env.MCP_SERVER_VERSION || "1.0.0",
          timestamp: new Date().toISOString(),
          meta_api_connection: "connected",
          accessible_accounts: accounts.length,
          rate_limit_status: "operational",
          features: {
            campaign_management: true,
            analytics_reporting: true,
            audience_management: true,
            creative_management: true,
            real_time_insights: true,
          },
        };

        return { content: [{ type: "text", text: JSON.stringify(response, null, 2) }] };
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : "Unknown error occurred";
        const response = {
          status: "unhealthy",
          server_name: process.env.MCP_SERVER_NAME || "Meta Marketing API Server",
          version: process.env.MCP_SERVER_VERSION || "1.0.0",
          timestamp: new Date().toISOString(),
          error: errorMessage,
          meta_api_connection: "failed",
        };

        return {
          content: [{ type: "text", text: JSON.stringify(response, null, 2) }],
          isError: true,
        };
      }
    });

    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("✅ MCP Server connected via stdio");
  } catch (error) {
    console.error("❌ Fatal error starting server:", error);
    process.exit(1);
  }
}

main();

