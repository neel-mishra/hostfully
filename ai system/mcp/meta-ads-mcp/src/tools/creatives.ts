import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { MetaApiClient } from "../meta-client.js";
import { CreateAdCreativeSchema, ListCreativesSchema } from "../types/mcp-tools.js";
import { errorResult, jsonResult } from "../utils/mcp-response.js";
import {
  analyzeCreativeUsage,
  extractCreativeCopyPreview,
} from "../utils/conversion-analysis.js";

export function registerCreativeTools(server: McpServer, metaClient: MetaApiClient) {
  server.tool("list_ad_creatives", ListCreativesSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { account_id, limit, after } = args;
      const result = await metaClient.listAdCreatives(account_id, {
        limit,
        after,
        fields: ["id", "name", "title", "body", "image_url", "object_story_spec", "asset_feed_spec", "url_tags", "call_to_action_type"],
      });
      const creativeUsage = await analyzeCreativeUsage(
        metaClient,
        account_id,
        result.data.map((creative) => creative.id),
      );
      const creatives = result.data.map((creative: any) => {
        const usage = creativeUsage[creative.id] || {};
        return {
          ...creative,
          ...usage,
          copy_preview: extractCreativeCopyPreview(creative) || usage.copy_preview || null,
        };
      });
      const response = {
        creatives,
        pagination: {
          has_next_page: result.hasNextPage,
          next_cursor: result.paging?.cursors?.after,
        },
        total_count: result.data.length,
      };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error listing creatives: ${msg}`);
    }
  });

  server.tool(
    "create_ad_creative",
    CreateAdCreativeSchema.shape as any,
    async (args: any, _extra: any) => {
      try {
        const { account_id, name, object_story_spec, body, title, image_url, url_tags, call_to_action } = args;
        const creativeData: any = { name };
        if (object_story_spec) creativeData.object_story_spec = object_story_spec;
        if (body) creativeData.body = body;
        if (title) creativeData.title = title;
        if (image_url) creativeData.image_url = image_url;
        if (url_tags) creativeData.url_tags = url_tags;
        if (call_to_action) creativeData.call_to_action = call_to_action;

        const result = await metaClient.createAdCreative(account_id, creativeData);
        const response = { success: true, creative_id: result.id, message: "Ad creative created successfully" };
        return jsonResult(response);
      } catch (error) {
        const msg = error instanceof Error ? error.message : "Unknown error occurred";
        return errorResult(`Error creating creative: ${msg}`);
      }
    },
  );
}

