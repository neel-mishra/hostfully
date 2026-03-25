import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { MetaApiClient } from "../meta-client.js";
import {
  getPrimaryResultLast7d,
  resolveConversionContext,
} from "../utils/conversion-analysis.js";

export function registerInsightsResources(server: McpServer, metaClient: MetaApiClient) {
  server.resource(
    "account-dashboard",
    new ResourceTemplate("meta://insights/account/{account_id}", { list: undefined }),
    async (uri, { account_id }) => {
      try {
        const [campaigns, accountInsights] = await Promise.all([
          metaClient.getCampaigns(account_id as string, { limit: 50 }),
          metaClient.getInsights(metaClient.authManager.getAccountId(account_id as string), {
            level: "account",
            date_preset: "last_30d",
            fields: ["impressions", "clicks", "spend", "reach", "frequency", "ctr", "cpc", "cpm"],
          }),
        ]);

        const accountTotals = accountInsights.data.reduce(
          (acc, insight) => {
            acc.impressions += parseFloat(insight.impressions || "0");
            acc.clicks += parseFloat(insight.clicks || "0");
            acc.spend += parseFloat(insight.spend || "0");
            acc.reach += parseFloat(insight.reach || "0");
            return acc;
          },
          { impressions: 0, clicks: 0, spend: 0, reach: 0 },
        );

        const top_campaigns = await Promise.all(
          campaigns.data.slice(0, 10).map(async (campaign) => {
            const conversion_action = await resolveConversionContext(metaClient, campaign.id, "campaign");
            const primary_result_last_7d = await getPrimaryResultLast7d(
              metaClient,
              campaign.id,
              "campaign",
              conversion_action,
            );
            return {
              id: campaign.id,
              name: campaign.name,
              objective: campaign.objective,
              status: campaign.status,
              conversion_action,
              primary_result_last_7d,
            };
          }),
        );

        const dashboard = {
          account_id,
          overview: {
            total_campaigns: campaigns.data.length,
            active_campaigns: campaigns.data.filter((c) => c.status === "ACTIVE").length,
            paused_campaigns: campaigns.data.filter((c) => c.status === "PAUSED").length,
            period: "Last 30 days",
          },
          account_performance: {
            impressions: accountTotals.impressions,
            clicks: accountTotals.clicks,
            spend: Math.round(accountTotals.spend * 100) / 100,
            reach: accountTotals.reach,
            ctr: accountTotals.impressions > 0 ? (accountTotals.clicks / accountTotals.impressions) * 100 : 0,
            cpc: accountTotals.clicks > 0 ? accountTotals.spend / accountTotals.clicks : 0,
            frequency: accountTotals.reach > 0 ? accountTotals.impressions / accountTotals.reach : 0,
          },
          top_campaigns,
          last_updated: new Date().toISOString(),
        };

        return {
          contents: [{ uri: uri.href, mimeType: "application/json", text: JSON.stringify(dashboard, null, 2) }],
        };
      } catch (error) {
        const msg = error instanceof Error ? error.message : "Unknown error occurred";
        return {
          contents: [
            {
              uri: uri.href,
              mimeType: "application/json",
              text: JSON.stringify({ error: "Failed to fetch account dashboard data", message: msg, account_id }, null, 2),
            },
          ],
        };
      }
    },
  );
}

