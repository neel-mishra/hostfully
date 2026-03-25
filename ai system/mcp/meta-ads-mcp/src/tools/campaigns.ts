import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { MetaApiClient } from "../meta-client.js";
import {
  CreateAdSchema,
  CreateAdSetSchema,
  CreateCampaignSchema,
  DeleteCampaignSchema,
  ListAdSetsSchema,
  ListAdsSchema,
  ListCampaignsSchema,
  UpdateAdSchema,
  UpdateAdSetSchema,
  UpdateCampaignSchema,
} from "../types/mcp-tools.js";
import { errorResult, jsonResult } from "../utils/mcp-response.js";
import {
  extractCreativeCopyPreview,
  getPrimaryResultLast7d,
  resolveConversionContext,
} from "../utils/conversion-analysis.js";

export function registerCampaignTools(server: McpServer, metaClient: MetaApiClient) {
  // Campaigns
  server.tool("list_campaigns", ListCampaignsSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { account_id, status, limit, after } = args;
      const result = await metaClient.getCampaigns(account_id, { status, limit, after });
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
            ...campaign,
            conversion_action,
            primary_result_last_7d,
          };
        }),
      );

      const response = {
        campaigns,
        pagination: {
          has_next_page: result.hasNextPage,
          has_previous_page: result.hasPreviousPage,
          next_cursor: result.paging?.cursors?.after,
          previous_cursor: result.paging?.cursors?.before,
        },
        total_count: result.data.length,
      };

      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error listing campaigns: ${msg}`);
    }
  });

  server.tool("create_campaign", CreateCampaignSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { account_id, budget_optimization, ...rest } = args;
      const result = await metaClient.createCampaign(account_id, {
        ...rest,
        ...(budget_optimization !== undefined ? { is_budget_optimization_enabled: budget_optimization } : {}),
      });
      const response = { success: true, campaign_id: result.id, message: "Campaign created successfully" };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error creating campaign: ${msg}`);
    }
  });

  server.tool("update_campaign", UpdateCampaignSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { campaign_id, ...updates } = args;
      const result = await metaClient.updateCampaign(campaign_id, updates);
      const response = { success: true, result, message: "Campaign updated successfully" };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error updating campaign: ${msg}`);
    }
  });

  server.tool("pause_campaign", UpdateCampaignSchema.pick({ campaign_id: true }).shape as any, async (args: any, _extra: any) => {
    try {
      const { campaign_id } = args;
      const result = await metaClient.updateCampaign(campaign_id, { status: "PAUSED" });
      const response = { success: true, result, message: "Campaign paused successfully" };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error pausing campaign: ${msg}`);
    }
  });

  server.tool("resume_campaign", UpdateCampaignSchema.pick({ campaign_id: true }).shape as any, async (args: any, _extra: any) => {
    try {
      const { campaign_id } = args;
      const result = await metaClient.updateCampaign(campaign_id, { status: "ACTIVE" });
      const response = { success: true, result, message: "Campaign resumed successfully" };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error resuming campaign: ${msg}`);
    }
  });

  server.tool("delete_campaign", DeleteCampaignSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { campaign_id } = args;
      const result = await metaClient.deleteCampaign(campaign_id);
      const response = { success: true, result, message: "Campaign deleted successfully" };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error deleting campaign: ${msg}`);
    }
  });

  // Ad sets
  server.tool("list_ad_sets", ListAdSetsSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { campaign_id, account_id, status, limit, after } = args;
      const result = await metaClient.getAdSets({
        campaignId: campaign_id,
        accountId: account_id,
        status,
        limit,
        after,
        fields: ["id", "name", "campaign_id", "status", "effective_status", "optimization_goal", "billing_event", "promoted_object", "targeting"],
      });
      const ad_sets = await Promise.all(
        result.data.map(async (adSet: any) => {
          const conversion_action = await resolveConversionContext(metaClient, adSet.id, "adset");
          const primary_result_last_7d = await getPrimaryResultLast7d(
            metaClient,
            adSet.id,
            "adset",
            conversion_action,
          );
          return {
            ...adSet,
            conversion_action,
            primary_result_last_7d,
          };
        }),
      );
      const response = {
        ad_sets,
        pagination: {
          has_next_page: result.hasNextPage,
          next_cursor: result.paging?.cursors?.after,
        },
        total_count: result.data.length,
      };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error listing ad sets: ${msg}`);
    }
  });

  server.tool("create_ad_set", CreateAdSetSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { account_id, ...adSetData } = args;
      const result = await metaClient.createAdSet(account_id, adSetData);
      const response = { success: true, adset_id: result.id, message: "Ad set created successfully" };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error creating ad set: ${msg}`);
    }
  });

  server.tool("update_ad_set", UpdateAdSetSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { adset_id, ...updates } = args;
      const result = await metaClient.updateAdSet(adset_id, updates);
      const response = { success: true, result, message: "Ad set updated successfully" };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error updating ad set: ${msg}`);
    }
  });

  // Ads
  server.tool("list_ads", ListAdsSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { adset_id, campaign_id, account_id, status, limit, after } = args;
      const result = await metaClient.getAds({
        adsetId: adset_id,
        campaignId: campaign_id,
        accountId: account_id,
        status,
        limit,
        after,
        fields: [
          "id",
          "name",
          "adset_id",
          "campaign_id",
          "status",
          "effective_status",
          "created_time",
          "updated_time",
          "creative{id,name,title,body,object_story_spec,asset_feed_spec}",
        ],
      });
      const ads = await Promise.all(
        result.data.map(async (ad: any) => {
          const conversion_action = await resolveConversionContext(metaClient, ad.id, "ad");
          const primary_result_last_7d = await getPrimaryResultLast7d(
            metaClient,
            ad.id,
            "ad",
            conversion_action,
          );
          return {
            ...ad,
            ad_copy_preview: extractCreativeCopyPreview(ad.creative),
            conversion_action,
            primary_result_last_7d,
          };
        }),
      );
      const response = {
        ads,
        pagination: {
          has_next_page: result.hasNextPage,
          next_cursor: result.paging?.cursors?.after,
        },
        total_count: result.data.length,
      };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error listing ads: ${msg}`);
    }
  });

  server.tool("create_ad", CreateAdSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { account_id, ...adData } = args;
      const result = await metaClient.createAd(account_id, adData);
      const response = { success: true, ad_id: result.id, message: "Ad created successfully" };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error creating ad: ${msg}`);
    }
  });

  server.tool("update_ad", UpdateAdSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { ad_id, ...updates } = args;
      const result = await metaClient.updateAd(ad_id, updates);
      const response = { success: true, result, message: "Ad updated successfully" };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error updating ad: ${msg}`);
    }
  });
}

