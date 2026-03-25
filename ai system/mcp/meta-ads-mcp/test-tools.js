#!/usr/bin/env node

/**
 * Simple Tool Registration Test
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { MetaApiClient } from "./src/meta-client.ts";
import { AuthManager } from "./src/utils/auth.ts";
import { registerCampaignTools } from "./src/tools/campaigns.ts";
import { registerAnalyticsTools } from "./src/tools/analytics.ts";
import { registerAudienceTools } from "./src/tools/audiences.ts";
import { registerCreativeTools } from "./src/tools/creatives.ts";
import { registerOAuthTools } from "./src/tools/oauth.ts";

process.env.META_ACCESS_TOKEN = "test_token_for_validation";
process.env.META_APP_ID = "test_app_id";
process.env.META_APP_SECRET = "test_app_secret";

console.log("🧪 Starting Tool Validation Test");
console.log("=================================");

async function testTools() {
  try {
    const server = new McpServer({ name: "Meta Ads MCP Test Server", version: "0.1.0" });

    const auth = new AuthManager({
      accessToken: "test_token",
      appId: "test_app_id",
      appSecret: "test_app_secret",
    });

    const metaClient = new MetaApiClient(auth);

    registerCampaignTools(server, metaClient);
    registerAnalyticsTools(server, metaClient);
    registerAudienceTools(server, metaClient);
    registerCreativeTools(server, metaClient);
    registerOAuthTools(server, auth);

    console.log("✅ Tool registration completed (no runtime calls performed).");
    return true;
  } catch (error) {
    console.error("❌ Tool validation failed:", error.message);
    return false;
  }
}

testTools()
  .then((success) => process.exit(success ? 0 : 1))
  .catch((error) => {
    console.error("❌ Unexpected error:", error);
    process.exit(1);
  });

