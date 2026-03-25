import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { MetaApiClient } from "../meta-client.js";
import {
  getPrimaryResultLast7d,
  resolveConversionContext,
} from "../utils/conversion-analysis.js";

export function registerCampaignResources(server: McpServer, metaClient: MetaApiClient) {
  server.resource(
    "campaigns",
    new ResourceTemplate("meta://campaigns/{account_id}", { list: undefined }),
    async (uri, { account_id }) => {
      try {
        const result = await metaClient.getCampaigns(account_id as string, {
          limit: 100,
          fields: [
            "id",
            "name",
            "objective",
            "status",
            "effective_status",
            "created_time",
            "updated_time",
            "daily_budget",
            "lifetime_budget",
            "budget_remaining",
          ],
        });

        const campaigns = await Promise.all(
          result.data.map(async (campaign) => {
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
              effective_status: campaign.effective_status,
              created_time: campaign.created_time,
              daily_budget: campaign.daily_budget,
              lifetime_budget: campaign.lifetime_budget,
              budget_remaining: campaign.budget_remaining,
              conversion_action,
              primary_result_last_7d,
            };
          }),
        );

        const campaignSummary = {
          account_id,
          total_campaigns: result.data.length,
          active_campaigns: result.data.filter((c) => c.status === "ACTIVE").length,
          paused_campaigns: result.data.filter((c) => c.status === "PAUSED").length,
          campaigns,
          last_updated: new Date().toISOString(),
        };

        return {
          contents: [
            {
              uri: uri.href,
              mimeType: "application/json",
              text: JSON.stringify(campaignSummary, null, 2),
            },
          ],
        };
      } catch (error) {
        const msg = error instanceof Error ? error.message : "Unknown error occurred";
        return {
          contents: [
            {
              uri: uri.href,
              mimeType: "application/json",
              text: JSON.stringify({ error: "Failed to fetch campaign data", message: msg, account_id }, null, 2),
            },
          ],
        };
      }
    },
  );

  server.resource(
    "campaign-details",
    new ResourceTemplate("meta://campaign/{campaign_id}", { list: undefined }),
    async (uri, { campaign_id }) => {
      try {
        const [campaign, adSets] = await Promise.all([
          metaClient.getCampaign(campaign_id as string),
          metaClient.getAdSets({ campaignId: campaign_id as string, limit: 50 }),
        ]);

        const conversion_action = await resolveConversionContext(metaClient, campaign_id as string, "campaign");
        const primary_result_last_7d = await getPrimaryResultLast7d(
          metaClient,
          campaign_id as string,
          "campaign",
          conversion_action,
        );

        const campaignDetails = {
          campaign,
          conversion_action,
          primary_result_last_7d,
          ad_sets: {
            total_count: adSets.data.length,
            active_count: adSets.data.filter((as) => as.status === "ACTIVE").length,
            paused_count: adSets.data.filter((as) => as.status === "PAUSED").length,
            list: adSets.data,
          },
          last_updated: new Date().toISOString(),
        };

        return {
          contents: [
            {
              uri: uri.href,
              mimeType: "application/json",
              text: JSON.stringify(campaignDetails, null, 2),
            },
          ],
        };
      } catch (error) {
        const msg = error instanceof Error ? error.message : "Unknown error occurred";
        return {
          contents: [
            {
              uri: uri.href,
              mimeType: "application/json",
              text: JSON.stringify({ error: "Failed to fetch campaign details", message: msg, campaign_id }, null, 2),
            },
          ],
        };
      }
    },
  );
}

