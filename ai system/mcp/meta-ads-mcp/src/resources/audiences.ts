import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { MetaApiClient } from "../meta-client.js";
import { analyzeAudienceUsage } from "../utils/conversion-analysis.js";

export function registerAudienceResources(server: McpServer, metaClient: MetaApiClient) {
  const getApproximateCount = (audience: any) => {
    if (typeof audience.approximate_count === "number") return audience.approximate_count;
    if (
      typeof audience.approximate_count_lower_bound === "number" &&
      typeof audience.approximate_count_upper_bound === "number"
    ) {
      return Math.round((audience.approximate_count_lower_bound + audience.approximate_count_upper_bound) / 2);
    }
    return audience.approximate_count_lower_bound || audience.approximate_count_upper_bound || 0;
  };

  server.resource(
    "audiences",
    new ResourceTemplate("meta://audiences/{account_id}", { list: undefined }),
    async (uri, { account_id }) => {
      try {
        const result = await metaClient.getCustomAudiences(account_id as string, {
          limit: 100,
          fields: [
            "id",
            "name",
            "description",
            "subtype",
            "approximate_count_lower_bound",
            "approximate_count_upper_bound",
            "data_source",
            "retention_days",
            "creation_time",
            "operation_status",
          ],
        });

        const audiences = result.data;
        const customAudiences = audiences.filter((a) => a.subtype !== "LOOKALIKE");
        const lookalikeAudiences = audiences.filter((a) => a.subtype === "LOOKALIKE");
        const audienceUsage = await analyzeAudienceUsage(
          metaClient,
          account_id as string,
          audiences.map((audience) => audience.id),
        );

        const overview = {
          account_id,
          summary: {
            total_audiences: audiences.length,
            custom_audiences: customAudiences.length,
            lookalike_audiences: lookalikeAudiences.length,
            total_reach: audiences.reduce((sum, a) => sum + getApproximateCount(a), 0),
          },
          recent_audiences: audiences
            .sort(
              (a, b) =>
                new Date(b.creation_time).getTime() - new Date(a.creation_time).getTime(),
            )
            .slice(0, 10)
            .map((audience) => ({
              ...audience,
              linked_usage: audienceUsage[audience.id] || {
                linked_ad_set_count: 0,
                linked_campaign_ids: [],
                linked_conversion_actions: [],
              },
            })),
          last_updated: new Date().toISOString(),
        };

        return {
          contents: [{ uri: uri.href, mimeType: "application/json", text: JSON.stringify(overview, null, 2) }],
        };
      } catch (error) {
        const msg = error instanceof Error ? error.message : "Unknown error occurred";
        return {
          contents: [
            {
              uri: uri.href,
              mimeType: "application/json",
              text: JSON.stringify({ error: "Failed to fetch audiences data", message: msg, account_id }, null, 2),
            },
          ],
        };
      }
    },
  );
}

