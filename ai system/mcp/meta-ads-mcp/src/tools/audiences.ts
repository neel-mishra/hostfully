import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { MetaApiClient } from "../meta-client.js";
import {
  CreateCustomAudienceSchema,
  CreateLookalikeAudienceSchema,
  EstimateAudienceSizeSchema,
  ListAudiencesSchema,
} from "../types/mcp-tools.js";
import { errorResult, jsonResult } from "../utils/mcp-response.js";
import { analyzeAudienceUsage } from "../utils/conversion-analysis.js";

export function registerAudienceTools(server: McpServer, metaClient: MetaApiClient) {
  const getApproximateCount = (audience: any) => {
    if (typeof audience.approximate_count === "number") return audience.approximate_count;
    if (
      typeof audience.approximate_count_lower_bound === "number" &&
      typeof audience.approximate_count_upper_bound === "number"
    ) {
      return Math.round((audience.approximate_count_lower_bound + audience.approximate_count_upper_bound) / 2);
    }
    return audience.approximate_count_lower_bound || audience.approximate_count_upper_bound || null;
  };

  server.tool("list_audiences", ListAudiencesSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { account_id, type, limit, after } = args;
      const result = await metaClient.getCustomAudiences(account_id, { limit, after });

      let audiences = result.data;
      if (type) {
        audiences = audiences.filter((audience) => {
          if (type === "custom") return audience.subtype !== "LOOKALIKE";
          if (type === "lookalike") return audience.subtype === "LOOKALIKE";
          return true;
        });
      }

      const audienceUsage = await analyzeAudienceUsage(
        metaClient,
        account_id,
        audiences.map((audience) => audience.id),
      );

      const formattedAudiences = audiences.map((audience) => ({
        id: audience.id,
        name: audience.name,
        description: audience.description,
        type: audience.subtype === "LOOKALIKE" ? "lookalike" : "custom",
        subtype: audience.subtype,
        approximate_count: getApproximateCount(audience),
        approximate_count_lower_bound: audience.approximate_count_lower_bound,
        approximate_count_upper_bound: audience.approximate_count_upper_bound,
        data_source: audience.data_source,
        retention_days: audience.retention_days,
        creation_time: audience.creation_time,
        operation_status: audience.operation_status,
        linked_usage: audienceUsage[audience.id] || {
          linked_ad_set_count: 0,
          linked_campaign_ids: [],
          linked_conversion_actions: [],
        },
      }));

      const response = {
        audiences: formattedAudiences,
        pagination: {
          has_next_page: result.hasNextPage,
          has_previous_page: result.hasPreviousPage,
          next_cursor: result.paging?.cursors?.after,
          previous_cursor: result.paging?.cursors?.before,
        },
        total_count: formattedAudiences.length,
        filter_applied: type || "all",
      };

      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error listing audiences: ${msg}`);
    }
  });

  server.tool(
    "create_custom_audience",
    CreateCustomAudienceSchema.shape as any,
    async (args: any, _extra: any) => {
      try {
        const { account_id, name, description, subtype, customer_file_source, retention_days, rule } = args;
        const audienceData: any = { name, subtype };
        if (description) audienceData.description = description;
        if (customer_file_source) audienceData.customer_file_source = customer_file_source;
        if (retention_days) audienceData.retention_days = retention_days;
        if (rule) audienceData.rule = rule;

        const result = await metaClient.createCustomAudience(account_id, audienceData);

        const response = {
          success: true,
          audience_id: result.id,
          message: `Custom audience \"${name}\" created successfully`,
          details: { id: result.id, name, subtype, account_id, description, retention_days },
          next_steps: [
            "Upload customer data to populate the audience",
            "Wait for the audience to process (may take a few hours)",
            "Use the audience in ad targeting once it's ready",
          ],
        };

        return jsonResult(response);
      } catch (error) {
        const msg = error instanceof Error ? error.message : "Unknown error occurred";
        return errorResult(`Error creating custom audience: ${msg}`);
      }
    },
  );

  server.tool(
    "create_lookalike_audience",
    CreateLookalikeAudienceSchema.shape as any,
    async (args: any, _extra: any) => {
      try {
        const { account_id, name, origin_audience_id, country, ratio, description } = args;
        if (ratio < 0.01 || ratio > 0.2) {
          return errorResult("Error: Ratio must be between 0.01 and 0.2");
        }

        const audienceData: any = { name, origin_audience_id, country, ratio };
        if (description) audienceData.description = description;

        const result = await metaClient.createLookalikeAudience(account_id, audienceData);

        const response = {
          success: true,
          audience_id: result.id,
          message: `Lookalike audience \"${name}\" created successfully`,
          details: { id: result.id, name, origin_audience_id, country, ratio: `${ratio * 100}%`, account_id, description },
          estimated_processing_time: "6-24 hours",
          next_steps: [
            "Wait for the lookalike audience to finish processing",
            "Check the audience size once processing is complete",
            "Use the audience in ad targeting",
          ],
        };

        return jsonResult(response);
      } catch (error) {
        const msg = error instanceof Error ? error.message : "Unknown error occurred";
        return errorResult(`Error creating lookalike audience: ${msg}`);
      }
    },
  );

  server.tool("estimate_audience_size", EstimateAudienceSizeSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { account_id, targeting, optimization_goal } = args;
      const estimate = await metaClient.estimateAudienceSize(account_id, targeting, optimization_goal);

      const formatNumber = (num: number) => {
        if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
        if (num >= 1000) return `${(num / 1000).toFixed(1)}K`;
        return num.toString();
      };

      const response = {
        estimate: {
          monthly_active_users: estimate.estimate_mau,
          daily_active_users: estimate.estimate_dau,
          formatted: {
            monthly_active_users: formatNumber(estimate.estimate_mau),
            daily_active_users: estimate.estimate_dau ? formatNumber(estimate.estimate_dau) : "N/A",
          },
        },
        targeting_parameters: targeting,
        optimization_goal,
        recommendations: generateTargetingRecommendations(estimate.estimate_mau),
        account_id,
      };

      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error estimating audience size: ${msg}`);
    }
  });
}

function generateTargetingRecommendations(audienceSize: number): string[] {
  const recommendations: string[] = [];

  if (audienceSize < 1000) {
    recommendations.push(
      "Audience size is very small. Consider broadening your targeting criteria.",
      "Add additional interests or behaviors to reach more people.",
      "Consider using lookalike audiences based on your existing customers.",
    );
  } else if (audienceSize < 10000) {
    recommendations.push(
      "Audience size is small but workable for niche targeting.",
      "Monitor performance closely as small audiences can have higher costs.",
      "Consider testing broader targeting to find additional relevant users.",
    );
  } else if (audienceSize < 100000) {
    recommendations.push(
      "Good audience size for most campaign objectives.",
      "You have room to test different creative approaches.",
      "Consider creating exclusion audiences to avoid overlap.",
    );
  } else if (audienceSize < 1000000) {
    recommendations.push(
      "Large audience size - good for reach and awareness campaigns.",
      "Consider using detailed targeting expansion for optimization.",
      "You may benefit from breaking this into smaller, more specific audiences.",
    );
  } else {
    recommendations.push(
      "Very large audience - consider narrowing your targeting.",
      "Use additional demographic or interest filters to improve relevance.",
      "Large audiences work well for brand awareness but may be less efficient for conversions.",
    );
  }

  recommendations.push(
    "Test different audience sizes to find the optimal balance of reach and relevance.",
    "Use Facebook's detailed targeting expansion when appropriate.",
    "Monitor frequency to avoid ad fatigue in smaller audiences.",
  );

  return recommendations;
}

