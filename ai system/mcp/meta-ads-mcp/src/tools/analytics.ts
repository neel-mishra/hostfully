import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { MetaApiClient } from "../meta-client.js";
import {
  GetInsightsSchema,
  ComparePerformanceSchema,
  ExportInsightsSchema,
  AnalyzePlacementsSchema,
  AnalyzeDevicesSchema,
  AnalyzeDemographicsSchema,
  AnalyzeGeoSchema,
  AnalyzeFunnelSchema,
  AnalyzeWinnersSchema,
  AnalyzeLosersSchema,
  AnalyzeAccountSchema,
  GenerateOptimizationBriefSchema,
} from "../types/mcp-tools.js";
import type { AdInsights } from "../types/meta-api.js";
import { errorResult, jsonResult } from "../utils/mcp-response.js";
import {
  extractPrimaryResult,
  resolveConversionContext,
} from "../utils/conversion-analysis.js";

const PRIMARY_RESULT_FIELDS = ["actions", "conversions", "cost_per_action_type", "spend"];
const DEFAULT_ANALYSIS_FIELDS = ["impressions", "clicks", "spend", "reach", "frequency", "ctr", "cpc", "cpm"];
const KNOWN_INSIGHT_KEYS = new Set([
  "date_start",
  "date_stop",
  "impressions",
  "clicks",
  "spend",
  "reach",
  "frequency",
  "ctr",
  "cpc",
  "cpm",
  "cpp",
  "actions",
  "conversions",
  "cost_per_action_type",
  "video_views",
  "video_view_time",
  "account_id",
  "campaign_name",
  "campaign_id",
  "adset_name",
  "adset_id",
  "ad_name",
  "ad_id",
]);

export function registerAnalyticsTools(server: McpServer, metaClient: MetaApiClient) {
  const runInsightsAnalysis = async (args: any, forcedBreakdowns?: string[]) => {
    const { object_id, level, date_preset, time_range, fields, breakdowns, limit } = args;
    const appliedBreakdowns = forcedBreakdowns || breakdowns;
    const params: Record<string, any> = {
      level,
      limit: limit || 25,
    };

    if (date_preset) params.date_preset = date_preset;
    else if (time_range) params.time_range = time_range;
    else params.date_preset = "last_7d";

    params.fields = ensurePrimaryResultFields(fields || DEFAULT_ANALYSIS_FIELDS);
    if (appliedBreakdowns?.length) params.breakdowns = appliedBreakdowns;

    const result = await metaClient.getInsights(object_id, params);
    const conversionContext = await resolveConversionContext(metaClient, object_id, level);
    const insights = result.data.map((insight) => formatInsightRow(insight, conversionContext, appliedBreakdowns));
    const summary = calculateSummaryMetrics(result.data);
    const primary_result = extractPrimaryResult(result.data, conversionContext);
    const breakdown_summary = buildBreakdownSummary(insights, appliedBreakdowns);

    return {
      insights,
      summary,
      conversion_action: conversionContext,
      primary_result,
      breakdown_summary,
      pagination: {
        has_next_page: result.hasNextPage,
        has_previous_page: result.hasPreviousPage,
        next_cursor: result.paging?.cursors?.after,
        previous_cursor: result.paging?.cursors?.before,
      },
      query_parameters: {
        object_id,
        level,
        date_preset,
        time_range,
        fields,
        breakdowns: appliedBreakdowns,
      },
      total_count: insights.length,
    };
  };

  // Get Insights Tool
  server.tool(
    "get_insights",
    GetInsightsSchema.shape as any,
    async (args: any, _extra: any) => {
      try {
        return jsonResult(await runInsightsAnalysis(args));
      } catch (error) {
        const msg = error instanceof Error ? error.message : "Unknown error occurred";
        return errorResult(`Error getting insights: ${msg}`);
      }
    },
  );

  // Compare Performance Tool
  server.tool(
    "compare_performance",
    ComparePerformanceSchema.shape as any,
    async (args: any, _extra: any) => {
      try {
        const { object_ids, level, date_preset, time_range, metrics } = args;
        const params: Record<string, any> = { level, fields: ensurePrimaryResultFields(metrics) };
        if (date_preset) params.date_preset = date_preset;
        else if (time_range) params.time_range = time_range;
        else params.date_preset = "last_7d";

        const comparisons: any[] = [];
        for (const objectId of object_ids) {
          try {
            const result = await metaClient.getInsights(objectId, params);
            const summary = calculateSummaryMetrics(result.data);
            const conversion_action = await resolveConversionContext(metaClient, objectId, level);
            const primary_result = extractPrimaryResult(result.data, conversion_action);

            let objectName = objectId;
            try {
              if (level === "campaign") {
                const campaign = await metaClient.getCampaign(objectId);
                objectName = campaign.name;
              }
            } catch {
              // ignore
            }

            comparisons.push({
              object_id: objectId,
              object_name: objectName,
              object_type: level,
              metrics: summary,
              conversion_action,
              primary_result,
            });
          } catch (err) {
            comparisons.push({
              object_id: objectId,
              object_name: objectId,
              object_type: level,
              error: err instanceof Error ? err.message : "Unknown error",
            });
          }
        }

        const rankings = calculatePerformanceRankings(comparisons, metrics);
        const response = {
          comparison_results: comparisons,
          rankings,
          query_parameters: { object_ids, level, date_preset, time_range, metrics },
          comparison_date: new Date().toISOString(),
        };

        return jsonResult(response);
      } catch (error) {
        const msg = error instanceof Error ? error.message : "Unknown error occurred";
        return errorResult(`Error comparing performance: ${msg}`);
      }
    },
  );

  // Export Insights Tool
  server.tool(
    "export_insights",
    ExportInsightsSchema.shape as any,
    async (args: any, _extra: any) => {
      try {
        const { object_id, level, format, date_preset, time_range, fields, breakdowns } = args;
        const params: Record<string, any> = { level, limit: 1000 };
        if (date_preset) params.date_preset = date_preset;
        else if (time_range) params.time_range = time_range;
        else params.date_preset = "last_30d";

        params.fields = ensurePrimaryResultFields(fields || DEFAULT_ANALYSIS_FIELDS);
        if (breakdowns?.length) params.breakdowns = breakdowns;

        const result = await metaClient.getInsights(object_id, params);
        const conversion_action = await resolveConversionContext(metaClient, object_id, level);
        const primary_result = extractPrimaryResult(result.data, conversion_action);
        const formattedInsights = result.data.map((insight) =>
          formatInsightRow(insight, conversion_action, breakdowns),
        );
        const breakdown_summary = buildBreakdownSummary(formattedInsights, breakdowns);

        let exportData: string;
        let mimeType: string;
        if (format === "csv") {
          exportData = convertToCSV(formattedInsights);
          mimeType = "text/csv";
        } else {
          exportData = JSON.stringify(formattedInsights, null, 2);
          mimeType = "application/json";
        }

        const response = {
          success: true,
          format,
          mime_type: mimeType,
          data_size: exportData.length,
          record_count: result.data.length,
          export_date: new Date().toISOString(),
          conversion_action,
          primary_result,
          breakdown_summary,
          query_parameters: { object_id, level, date_preset, time_range, fields, breakdowns },
          data: exportData,
        };

        return jsonResult(response);
      } catch (error) {
        const msg = error instanceof Error ? error.message : "Unknown error occurred";
        return errorResult(`Error exporting insights: ${msg}`);
      }
    },
  );

  // Convenience: campaign performance
  server.tool("get_campaign_performance", GetInsightsSchema.shape as any, async (params: any, _extra: any) => {
    try {
      const campaignParams = {
        ...params,
        level: "campaign" as const,
        fields: ensurePrimaryResultFields(
          params.fields || ["impressions", "clicks", "spend", "ctr", "cpc", "cpm", "reach", "frequency"],
        ),
      };
      const result = await metaClient.getInsights(params.object_id, campaignParams);
      const conversionContext = await resolveConversionContext(metaClient, params.object_id, "campaign");
      const formattedBreakdown = result.data.map((insight) =>
        formatInsightRow(insight, conversionContext, params.breakdowns),
      );
      const summary = calculateSummaryMetrics(result.data);
      const primary_result = extractPrimaryResult(result.data, conversionContext);

      let campaignDetails: any;
      try {
        campaignDetails = await metaClient.getCampaign(params.object_id);
      } catch {
        campaignDetails = { id: params.object_id, name: "Unknown Campaign" };
      }

      const response = {
        campaign: {
          id: campaignDetails.id,
          name: campaignDetails.name,
          objective: campaignDetails.objective,
          status: campaignDetails.status,
        },
        performance: summary,
        conversion_action: conversionContext,
        primary_result,
        daily_breakdown: formattedBreakdown,
        breakdown_summary: buildBreakdownSummary(formattedBreakdown, params.breakdowns),
        query_parameters: campaignParams,
      };

      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error getting campaign performance: ${msg}`);
    }
  });

  server.tool("get_attribution_data", GetInsightsSchema.shape as any, async (params: any, _extra: any) => {
    try {
      const attributionParams = {
        ...params,
        fields: ensurePrimaryResultFields(
          params.fields || ["impressions", "clicks", "spend", "actions", "cost_per_action_type"],
        ),
        breakdowns: params.breakdowns || ["action_attribution_windows"],
      };
      const result = await metaClient.getInsights(params.object_id, attributionParams);
      const conversion_action = await resolveConversionContext(metaClient, params.object_id, params.level || "campaign");
      const primary_result = extractPrimaryResult(result.data, conversion_action);
      const attribution_data = result.data.map((insight) =>
        formatInsightRow(insight, conversion_action, attributionParams.breakdowns),
      );
      const response = {
        attribution_data,
        summary: calculateAttributionMetrics(result.data),
        conversion_action,
        primary_result,
        breakdown_summary: buildBreakdownSummary(attribution_data, attributionParams.breakdowns),
        query_parameters: attributionParams,
        total_records: result.data.length,
      };
      return jsonResult(response);
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error getting attribution data: ${msg}`);
    }
  });

  server.tool("analyze_placements", AnalyzePlacementsSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const response = await runInsightsAnalysis(args, ["publisher_platform", "platform_position"]);
      return jsonResult({
        analysis_type: "placements",
        breakdown_dimensions: ["publisher_platform", "platform_position"],
        ...response,
      });
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error analyzing placements: ${msg}`);
    }
  });

  server.tool("analyze_devices", AnalyzeDevicesSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const response = await runInsightsAnalysis(args, ["impression_device"]);
      return jsonResult({
        analysis_type: "devices",
        breakdown_dimensions: ["impression_device"],
        ...response,
      });
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error analyzing devices: ${msg}`);
    }
  });

  server.tool("analyze_demographics", AnalyzeDemographicsSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const response = await runInsightsAnalysis(args, ["age", "gender"]);
      return jsonResult({
        analysis_type: "demographics",
        breakdown_dimensions: ["age", "gender"],
        ...response,
      });
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error analyzing demographics: ${msg}`);
    }
  });

  server.tool("analyze_geo", AnalyzeGeoSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const geographyLevel = args.geography_level || "country";
      const response = await runInsightsAnalysis(args, [geographyLevel]);
      return jsonResult({
        analysis_type: "geo",
        breakdown_dimensions: [geographyLevel],
        geography_level: geographyLevel,
        ...response,
      });
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error analyzing geo breakdowns: ${msg}`);
    }
  });

  server.tool("analyze_funnel", AnalyzeFunnelSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const { object_id, level, date_preset, time_range, fields, limit } = args;
      const params: Record<string, any> = {
        level,
        limit: limit || 100,
      };

      if (date_preset) params.date_preset = date_preset;
      else if (time_range) params.time_range = time_range;
      else params.date_preset = "last_7d";

      params.fields = ensurePrimaryResultFields(fields || DEFAULT_ANALYSIS_FIELDS);

      const result = await metaClient.getInsights(object_id, params);
      const conversion_action = await resolveConversionContext(metaClient, object_id, level);
      const primary_result = extractPrimaryResult(result.data, conversion_action);
      const funnel = buildFunnelAnalysis(result.data, conversion_action);

      return jsonResult({
        analysis_type: "funnel",
        funnel,
        summary: calculateSummaryMetrics(result.data),
        conversion_action,
        primary_result,
        pagination: {
          has_next_page: result.hasNextPage,
          has_previous_page: result.hasPreviousPage,
          next_cursor: result.paging?.cursors?.after,
          previous_cursor: result.paging?.cursors?.before,
        },
        query_parameters: { object_id, level, date_preset, time_range, fields: params.fields },
        total_count: result.data.length,
      });
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error analyzing funnel: ${msg}`);
    }
  });

  server.tool("analyze_winners", AnalyzeWinnersSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const {
        object_id,
        scope,
        geography_level,
        date_preset,
        time_range,
        fields,
        limit,
        top_n,
        min_spend,
        sort_by,
      } = args;

      const winnerConfig = getWinnerConfig(scope, geography_level || "country");
      const params: Record<string, any> = {
        level: winnerConfig.level,
        limit: limit || 100,
        fields: ensurePrimaryResultFields([...DEFAULT_ANALYSIS_FIELDS, ...(fields || []), ...winnerConfig.fields]),
      };

      if (date_preset) params.date_preset = date_preset;
      else if (time_range) params.time_range = time_range;
      else params.date_preset = "last_7d";

      if (winnerConfig.breakdowns?.length) {
        params.breakdowns = winnerConfig.breakdowns;
      }

      const result = await metaClient.getInsights(object_id, params);
      const conversion_action = await resolveWinnerConversionContext(metaClient, object_id, scope);
      const ranked_rows = rankWinnerRows(
        result.data,
        conversion_action,
        winnerConfig,
        sort_by || "results",
        top_n || 10,
        min_spend || 0,
      );

      return jsonResult({
        analysis_type: "winners",
        scope,
        geography_level: scope === "geo" ? geography_level || "country" : undefined,
        ranking_metric: sort_by || "results",
        minimum_spend_filter: min_spend || 0,
        conversion_action,
        winners: ranked_rows,
        summary: {
          evaluated_rows: result.data.length,
          returned_rows: ranked_rows.length,
          rows_with_results: ranked_rows.filter((row) => (row.primary_result?.results || 0) > 0).length,
          total_primary_results_in_returned_rows: ranked_rows.reduce(
            (sum, row) => sum + (row.primary_result?.results || 0),
            0,
          ),
        },
        query_parameters: {
          object_id,
          level: winnerConfig.level,
          breakdowns: winnerConfig.breakdowns,
          date_preset,
          time_range,
          fields: params.fields,
          limit: params.limit,
          top_n: top_n || 10,
        },
      });
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error analyzing winners: ${msg}`);
    }
  });

  server.tool("analyze_losers", AnalyzeLosersSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const {
        object_id,
        scope,
        geography_level,
        date_preset,
        time_range,
        fields,
        limit,
        top_n,
        min_spend,
        sort_by,
      } = args;

      const loserConfig = getWinnerConfig(scope, geography_level || "country");
      const params: Record<string, any> = {
        level: loserConfig.level,
        limit: limit || 100,
        fields: ensurePrimaryResultFields([...DEFAULT_ANALYSIS_FIELDS, ...(fields || []), ...loserConfig.fields]),
      };

      if (date_preset) params.date_preset = date_preset;
      else if (time_range) params.time_range = time_range;
      else params.date_preset = "last_7d";

      if (loserConfig.breakdowns?.length) {
        params.breakdowns = loserConfig.breakdowns;
      }

      const result = await metaClient.getInsights(object_id, params);
      const conversion_action = await resolveWinnerConversionContext(metaClient, object_id, scope);
      const ranked_rows = rankLoserRows(
        result.data,
        conversion_action,
        loserConfig,
        sort_by || "cost_per_result",
        top_n || 10,
        min_spend || 0,
      );

      return jsonResult({
        analysis_type: "losers",
        scope,
        geography_level: scope === "geo" ? geography_level || "country" : undefined,
        ranking_metric: sort_by || "cost_per_result",
        minimum_spend_filter: min_spend || 0,
        conversion_action,
        losers: ranked_rows,
        summary: {
          evaluated_rows: result.data.length,
          returned_rows: ranked_rows.length,
          rows_with_zero_results: ranked_rows.filter((row) => (row.primary_result?.results || 0) === 0).length,
          zero_result_spend_in_returned_rows: round2(
            ranked_rows.reduce(
              (sum, row) => sum + ((row.primary_result?.results || 0) === 0 ? row.spend || 0 : 0),
              0,
            ),
          ),
          total_spend_in_returned_rows: round2(ranked_rows.reduce((sum, row) => sum + (row.spend || 0), 0)),
        },
        query_parameters: {
          object_id,
          level: loserConfig.level,
          breakdowns: loserConfig.breakdowns,
          date_preset,
          time_range,
          fields: params.fields,
          limit: params.limit,
          top_n: top_n || 10,
        },
      });
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error analyzing losers: ${msg}`);
    }
  });

  server.tool("analyze_account", AnalyzeAccountSchema.shape as any, async (args: any, _extra: any) => {
    try {
      return jsonResult(await buildExecutiveSummary(metaClient, args));
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error analyzing account summary: ${msg}`);
    }
  });

  server.tool("generate_optimization_brief", GenerateOptimizationBriefSchema.shape as any, async (args: any, _extra: any) => {
    try {
      const summary = await buildExecutiveSummary(metaClient, args);
      const brief = buildOptimizationBrief(summary);
      return jsonResult({
        analysis_type: "optimization_brief",
        object_id: summary.object_id,
        level: summary.level,
        conversion_action: summary.conversion_action,
        overview: summary.overview,
        primary_result: summary.primary_result,
        highlights: summary.highlights,
        recommendations: brief.recommendations,
        markdown: brief.markdown,
        query_parameters: summary.query_parameters,
      });
    } catch (error) {
      const msg = error instanceof Error ? error.message : "Unknown error occurred";
      return errorResult(`Error generating optimization brief: ${msg}`);
    }
  });
}

function ensurePrimaryResultFields(fields?: string[]): string[] | undefined {
  if (!fields?.length) return undefined;
  const deduped = new Set(fields);
  for (const field of PRIMARY_RESULT_FIELDS) deduped.add(field);
  return Array.from(deduped);
}

function formatInsightRow(insight: any, conversionContext: any, requestedBreakdowns?: string[]) {
  const breakdown_values = extractBreakdownValues(insight, requestedBreakdowns);
  const primary_result = extractPrimaryResult([insight], conversionContext);

  return {
    date_start: insight.date_start,
    date_stop: insight.date_stop,
    impressions: insight.impressions,
    clicks: insight.clicks,
    spend: insight.spend,
    reach: insight.reach,
    frequency: insight.frequency,
    ctr: insight.ctr,
    cpc: insight.cpc,
    cpm: insight.cpm,
    cpp: insight.cpp,
    actions: insight.actions,
    conversions: insight.conversions,
    cost_per_action_type: insight.cost_per_action_type,
    video_views: insight.video_views,
    video_view_time: insight.video_view_time,
    account_id: insight.account_id,
    campaign_id: insight.campaign_id,
    adset_id: insight.adset_id,
    ad_id: insight.ad_id,
    ...breakdown_values,
    ...(Object.keys(breakdown_values).length > 0 ? { breakdown_values } : {}),
    primary_result,
  };
}

function extractBreakdownValues(insight: any, requestedBreakdowns?: string[]): Record<string, any> {
  if (requestedBreakdowns?.length) {
    return requestedBreakdowns.reduce((acc: Record<string, any>, key) => {
      if (insight[key] !== undefined) acc[key] = insight[key];
      return acc;
    }, {});
  }

  return Object.keys(insight).reduce((acc: Record<string, any>, key) => {
    if (KNOWN_INSIGHT_KEYS.has(key)) return acc;
    const value = insight[key];
    if (value === undefined || value === null) return acc;
    if (typeof value === "object") return acc;
    acc[key] = value;
    return acc;
  }, {});
}

function buildBreakdownSummary(rows: any[], requestedBreakdowns?: string[]) {
  if (!requestedBreakdowns?.length) return null;

  const normalizedRows = rows.map((row) => ({
    breakdown_values: row.breakdown_values || extractBreakdownValues(row, requestedBreakdowns),
    result_label: row.primary_result?.label || null,
    results: row.primary_result?.results || 0,
    cost_per_result: row.primary_result?.cost_per_result ?? null,
    spend: parseFloat(row.spend || "0"),
    impressions: parseFloat(row.impressions || "0"),
    clicks: parseFloat(row.clicks || "0"),
    ctr: parseFloat(row.ctr || "0"),
  }));

  const top_rows_by_results = normalizedRows
    .filter((row) => row.results > 0)
    .sort((a, b) => b.results - a.results)
    .slice(0, 10);

  const top_rows_by_spend = normalizedRows.sort((a, b) => b.spend - a.spend).slice(0, 10);

  return {
    dimensions: requestedBreakdowns,
    row_count: rows.length,
    rows_with_results: normalizedRows.filter((row) => row.results > 0).length,
    top_rows_by_results,
    top_rows_by_spend,
  };
}

function buildFunnelAnalysis(insights: AdInsights[], conversionContext: any) {
  const totals = insights.reduce(
    (acc, insight) => {
      acc.impressions += parseFloat(insight.impressions || "0");
      acc.clicks += parseFloat(insight.clicks || "0");
      acc.spend += parseFloat(insight.spend || "0");
      acc.landing_page_views += getActionValue(insight, [
        "landing_page_view",
        "omni_landing_page_view",
      ]);
      acc.leads += getActionValue(insight, [
        "lead",
        "onsite_web_lead",
        "offsite_conversion.fb_pixel_lead",
      ]);
      return acc;
    },
    {
      impressions: 0,
      clicks: 0,
      spend: 0,
      landing_page_views: 0,
      leads: 0,
    },
  );

  const primaryResult = extractPrimaryResult(insights, conversionContext);
  const primaryConversions = primaryResult?.results || 0;

  const steps = [
    {
      key: "impressions",
      label: "Impressions",
      value: Math.round(totals.impressions),
    },
    {
      key: "clicks",
      label: "Clicks",
      value: Math.round(totals.clicks),
      rate_from_previous: safeRate(totals.clicks, totals.impressions),
      cost_per_step: safeCost(totals.spend, totals.clicks),
    },
    {
      key: "landing_page_views",
      label: "Landing Page Views",
      value: Math.round(totals.landing_page_views),
      rate_from_previous: safeRate(totals.landing_page_views, totals.clicks),
      cost_per_step: safeCost(totals.spend, totals.landing_page_views),
    },
    {
      key: "leads",
      label: "Leads",
      value: Math.round(totals.leads),
      rate_from_previous: safeRate(totals.leads, totals.landing_page_views || totals.clicks),
      cost_per_step: safeCost(totals.spend, totals.leads),
    },
    {
      key: "primary_conversion",
      label: conversionContext?.label || primaryResult?.label || "Primary Conversion",
      value: Math.round(primaryConversions),
      rate_from_previous: safeRate(primaryConversions, totals.leads || totals.landing_page_views || totals.clicks),
      cost_per_step: safeCost(totals.spend, primaryConversions),
      action_type: primaryResult?.action_type || conversionContext?.action_type || null,
    },
  ];

  return {
    steps,
    overall: {
      spend: round2(totals.spend),
      ctr: safeRate(totals.clicks, totals.impressions),
      landing_page_view_rate: safeRate(totals.landing_page_views, totals.clicks),
      lead_rate_from_click: safeRate(totals.leads, totals.clicks),
      primary_conversion_rate_from_click: safeRate(primaryConversions, totals.clicks),
      primary_conversion_rate_from_impression: safeRate(primaryConversions, totals.impressions),
      cpc: safeCost(totals.spend, totals.clicks),
      cplpv: safeCost(totals.spend, totals.landing_page_views),
      cpl: safeCost(totals.spend, totals.leads),
      cost_per_primary_conversion: safeCost(totals.spend, primaryConversions),
    },
  };
}

function buildScopedInsightsParams(
  scopeConfig: any,
  fields: string[] | undefined,
  limit: number | undefined,
  baseDateParams: Record<string, any>,
) {
  const params: Record<string, any> = {
    level: scopeConfig.level,
    limit: limit || 100,
    fields: ensurePrimaryResultFields([...DEFAULT_ANALYSIS_FIELDS, ...(fields || []), ...scopeConfig.fields]),
    ...baseDateParams,
  };

  if (scopeConfig.breakdowns?.length) {
    params.breakdowns = scopeConfig.breakdowns;
  }

  return params;
}

function getChildEntityScope(level: string) {
  if (level === "account") return "campaigns";
  if (level === "campaign") return "adsets";
  return "ads";
}

function buildExecutiveHighlights(summary: any) {
  const highlights: string[] = [];
  const topEntity = summary.top_entities?.[0];
  const weakEntity = summary.weak_entities?.[0];
  const topDevice = summary.top_devices?.[0];
  const weakDevice = summary.weak_devices?.[0];
  const topGeo = summary.top_geo?.[0];
  const weakGeo = summary.weak_geo?.[0];
  const topPlacement = summary.top_placements?.[0];

  if (summary.primary_result?.results !== undefined) {
    highlights.push(
      `Primary conversion ${summary.primary_result.label || "result"} delivered ${summary.primary_result.results} results.`,
    );
  }
  if (topEntity) {
    highlights.push(
      `Top ${summary.childScope.slice(0, -1)}: ${topEntity.label} with ${topEntity.primary_result?.results || 0} labeled results.`,
    );
  }
  if (weakEntity && (weakEntity.primary_result?.results || 0) === 0) {
    highlights.push(`Weakest ${summary.childScope.slice(0, -1)}: ${weakEntity.label} spent ${weakEntity.spend} with zero labeled results.`);
  } else if (weakEntity) {
    highlights.push(
      `Least efficient ${summary.childScope.slice(0, -1)}: ${weakEntity.label} at ${weakEntity.primary_result?.cost_per_result ?? "N/A"} cost per result.`,
    );
  }
  if (topDevice) {
    highlights.push(
      `Best device: ${topDevice.label} produced ${topDevice.primary_result?.results || 0} results at ${topDevice.primary_result?.cost_per_result ?? "N/A"} cost per result.`,
    );
  }
  if (weakDevice && (weakDevice.primary_result?.results || 0) === 0) {
    highlights.push(`Waste device pocket: ${weakDevice.label} spent ${weakDevice.spend} with zero labeled results.`);
  }
  if (topGeo) {
    highlights.push(`Top geo: ${topGeo.label} generated ${topGeo.primary_result?.results || 0} labeled results.`);
  }
  if (weakGeo && (weakGeo.primary_result?.results || 0) === 0) {
    highlights.push(`Weak geo: ${weakGeo.label} spent ${weakGeo.spend} with zero labeled results.`);
  }
  if (topPlacement) {
    highlights.push(
      `Best placement slice: ${topPlacement.label} with ${topPlacement.primary_result?.results || 0} labeled results.`,
    );
  }

  return highlights;
}

async function buildExecutiveSummary(metaClient: MetaApiClient, args: any) {
  const {
    object_id,
    level,
    geography_level,
    date_preset,
    time_range,
    fields,
    limit,
    top_n,
    min_spend,
  } = args;

  const summaryParams: Record<string, any> = {
    level,
    limit: 100,
    fields: ensurePrimaryResultFields(fields || DEFAULT_ANALYSIS_FIELDS),
  };
  if (date_preset) summaryParams.date_preset = date_preset;
  else if (time_range) summaryParams.time_range = time_range;
  else summaryParams.date_preset = "last_7d";

  const resolvedGeoLevel = geography_level || "country";
  const childScope = getChildEntityScope(level);
  const entityConfig = getWinnerConfig(childScope, resolvedGeoLevel);
  const placementConfig = getWinnerConfig("placements", resolvedGeoLevel);
  const deviceConfig = getWinnerConfig("devices", resolvedGeoLevel);
  const geoConfig = getWinnerConfig("geo", resolvedGeoLevel);

  const baseDateParams =
    date_preset ? { date_preset } : time_range ? { time_range } : { date_preset: "last_7d" };

  const [
    summaryResult,
    conversion_action,
    entityResult,
    placementResult,
    deviceResult,
    geoResult,
  ] = await Promise.all([
    metaClient.getInsights(object_id, summaryParams),
    resolveConversionContext(metaClient, object_id, level),
    metaClient.getInsights(object_id, buildScopedInsightsParams(entityConfig, fields, limit, baseDateParams)),
    metaClient.getInsights(object_id, buildScopedInsightsParams(placementConfig, fields, limit, baseDateParams)),
    metaClient.getInsights(object_id, buildScopedInsightsParams(deviceConfig, fields, limit, baseDateParams)),
    metaClient.getInsights(object_id, buildScopedInsightsParams(geoConfig, fields, limit, baseDateParams)),
  ]);

  const funnel = buildFunnelAnalysis(summaryResult.data, conversion_action);
  const primary_result = extractPrimaryResult(summaryResult.data, conversion_action);
  const topN = top_n || 5;
  const minSpend = min_spend || 0;

  const top_entities = rankWinnerRows(entityResult.data, conversion_action, entityConfig, "results", topN, 0);
  const weak_entities = rankLoserRows(
    entityResult.data,
    conversion_action,
    entityConfig,
    "cost_per_result",
    topN,
    minSpend,
  );
  const top_placements = rankWinnerRows(
    placementResult.data,
    conversion_action,
    placementConfig,
    "results",
    topN,
    0,
  );
  const weak_placements = rankLoserRows(
    placementResult.data,
    conversion_action,
    placementConfig,
    "cost_per_result",
    topN,
    minSpend,
  );
  const top_devices = rankWinnerRows(deviceResult.data, conversion_action, deviceConfig, "results", topN, 0);
  const weak_devices = rankLoserRows(
    deviceResult.data,
    conversion_action,
    deviceConfig,
    "cost_per_result",
    topN,
    minSpend,
  );
  const top_geo = rankWinnerRows(geoResult.data, conversion_action, geoConfig, "results", topN, 0);
  const weak_geo = rankLoserRows(geoResult.data, conversion_action, geoConfig, "cost_per_result", topN, minSpend);

  return {
    analysis_type: "account_executive_summary",
    object_id,
    level,
    conversion_action,
    overview: calculateSummaryMetrics(summaryResult.data),
    primary_result,
    funnel,
    entity_scope: childScope,
    winners: {
      entities: top_entities,
      placements: top_placements,
      devices: top_devices,
      geo: top_geo,
    },
    losers: {
      entities: weak_entities,
      placements: weak_placements,
      devices: weak_devices,
      geo: weak_geo,
    },
    highlights: buildExecutiveHighlights({
      childScope,
      primary_result,
      top_entities,
      weak_entities,
      top_devices,
      weak_devices,
      top_geo,
      weak_geo,
      top_placements,
    }),
    query_parameters: {
      object_id,
      level,
      geography_level: resolvedGeoLevel,
      date_preset,
      time_range,
      limit: limit || 100,
      top_n: topN,
      min_spend: minSpend,
    },
  };
}

function buildOptimizationBrief(summary: any) {
  const scaleActions = [
    ...summary.winners.entities.slice(0, 2).map((row: any) =>
      `Scale ${row.label}: ${row.primary_result?.results || 0} results at ${
        row.primary_result?.cost_per_result ?? "N/A"
      } cost per result.`,
    ),
    ...summary.winners.devices
      .filter((row: any) => (row.primary_result?.results || 0) > 0)
      .slice(0, 1)
      .map((row: any) => `Lean into ${row.label}: strongest device volume with ${row.primary_result?.results} results.`),
    ...summary.winners.geo
      .filter((row: any) => (row.primary_result?.results || 0) > 0)
      .slice(0, 1)
      .map((row: any) => `Prioritize ${row.label}: best geo contribution with ${row.primary_result?.results} labeled results.`),
  ].slice(0, 4);

  const cutActions = [
    ...summary.losers.devices
      .filter((row: any) => (row.primary_result?.results || 0) === 0)
      .slice(0, 2)
      .map((row: any) => `Cut or cap ${row.label}: spent ${row.spend} with zero labeled results.`),
    ...summary.losers.placements
      .filter((row: any) => (row.primary_result?.results || 0) === 0)
      .slice(0, 2)
      .map((row: any) => `Reduce ${row.label}: spent ${row.spend} with no labeled conversion output.`),
    ...summary.losers.entities
      .filter((row: any) => (row.primary_result?.cost_per_result ?? 0) > 0)
      .slice(0, 1)
      .map((row: any) => `Watch ${row.label}: weakest entity efficiency at ${row.primary_result?.cost_per_result} cost per result.`),
  ].slice(0, 4);

  const testActions = [
    summary.winners.placements[0]
      ? `Replicate the ${summary.winners.placements[0].label} message/creative pattern in new variants.`
      : null,
    summary.winners.geo[0] && summary.losers.geo[0]
      ? `Test geo-specific budget shifts from ${summary.losers.geo[0].label} into ${summary.winners.geo[0].label}.`
      : null,
    summary.winners.devices[0] && summary.losers.devices[0]
      ? `Build device-specific creative or landing-page tests for ${summary.winners.devices[0].label} vs ${summary.losers.devices[0].label}.`
      : null,
    `Test conversion-rate lift between click -> LPV -> lead, where current flow is ${summary.funnel.overall.landing_page_view_rate}% LPV rate and ${summary.funnel.overall.lead_rate_from_click}% lead rate from click.`,
  ].filter(Boolean) as string[];

  const markdown = [
    `## Optimization Brief`,
    ``,
    `**Primary conversion:** ${summary.primary_result?.label || "Primary conversion"}`,
    `**Results:** ${summary.primary_result?.results || 0}`,
    `**Cost per result:** ${summary.primary_result?.cost_per_result ?? "N/A"}`,
    `**Spend:** ${summary.overview.total_spend}`,
    ``,
    `### Scale`,
    ...scaleActions.map((item: string) => `- ${item}`),
    ``,
    `### Cut`,
    ...cutActions.map((item: string) => `- ${item}`),
    ``,
    `### Test`,
    ...testActions.map((item: string) => `- ${item}`),
    ``,
    `### Key Highlights`,
    ...summary.highlights.map((item: string) => `- ${item}`),
  ].join("\n");

  return {
    recommendations: {
      scale: scaleActions,
      cut: cutActions,
      test: testActions,
    },
    markdown,
  };
}

async function resolveWinnerConversionContext(metaClient: MetaApiClient, objectId: string, scope: string) {
  const candidateLevels =
    scope === "campaigns" ? ["account", "campaign"] : ["campaign", "adset", "ad", "account"];

  for (const candidate of candidateLevels) {
    const context = await resolveConversionContext(metaClient, objectId, candidate);
    if (context) return context;
  }

  return null;
}

function getWinnerConfig(scope: string, geographyLevel: string) {
  switch (scope) {
    case "campaigns":
      return {
        level: "campaign",
        fields: ["campaign_id", "campaign_name"],
        breakdowns: undefined,
        identifyRow: (insight: any) => ({
          id: insight.campaign_id,
          name: insight.campaign_name || insight.campaign_id,
          type: "campaign",
          label: insight.campaign_name || insight.campaign_id,
        }),
      };
    case "adsets":
      return {
        level: "adset",
        fields: ["campaign_id", "campaign_name", "adset_id", "adset_name"],
        breakdowns: undefined,
        identifyRow: (insight: any) => ({
          id: insight.adset_id,
          name: insight.adset_name || insight.adset_id,
          type: "adset",
          label: insight.adset_name || insight.adset_id,
          parent_campaign_id: insight.campaign_id,
          parent_campaign_name: insight.campaign_name,
        }),
      };
    case "ads":
      return {
        level: "ad",
        fields: ["campaign_id", "campaign_name", "adset_id", "adset_name", "ad_id", "ad_name"],
        breakdowns: undefined,
        identifyRow: (insight: any) => ({
          id: insight.ad_id,
          name: insight.ad_name || insight.ad_id,
          type: "ad",
          label: insight.ad_name || insight.ad_id,
          parent_adset_id: insight.adset_id,
          parent_adset_name: insight.adset_name,
          parent_campaign_id: insight.campaign_id,
          parent_campaign_name: insight.campaign_name,
        }),
      };
    case "placements":
      return {
        level: "campaign",
        fields: [],
        breakdowns: ["publisher_platform", "platform_position"],
        identifyRow: (insight: any) => ({
          id: `${insight.publisher_platform || "unknown"}::${insight.platform_position || "unknown"}`,
          name: `${insight.publisher_platform || "unknown"} / ${insight.platform_position || "unknown"}`,
          type: "placement",
          label: `${insight.publisher_platform || "unknown"} / ${insight.platform_position || "unknown"}`,
          breakdown_values: extractBreakdownValues(insight, ["publisher_platform", "platform_position"]),
        }),
      };
    case "devices":
      return {
        level: "campaign",
        fields: [],
        breakdowns: ["impression_device"],
        identifyRow: (insight: any) => ({
          id: insight.impression_device || "unknown",
          name: insight.impression_device || "unknown",
          type: "device",
          label: insight.impression_device || "unknown",
          breakdown_values: extractBreakdownValues(insight, ["impression_device"]),
        }),
      };
    case "demographics":
      return {
        level: "campaign",
        fields: [],
        breakdowns: ["age", "gender"],
        identifyRow: (insight: any) => ({
          id: `${insight.age || "unknown"}::${insight.gender || "unknown"}`,
          name: `${insight.age || "unknown"} / ${insight.gender || "unknown"}`,
          type: "demographic",
          label: `${insight.age || "unknown"} / ${insight.gender || "unknown"}`,
          breakdown_values: extractBreakdownValues(insight, ["age", "gender"]),
        }),
      };
    case "geo":
      return {
        level: "campaign",
        fields: [],
        breakdowns: [geographyLevel],
        identifyRow: (insight: any) => ({
          id: insight[geographyLevel] || "unknown",
          name: insight[geographyLevel] || "unknown",
          type: "geo",
          label: insight[geographyLevel] || "unknown",
          breakdown_values: extractBreakdownValues(insight, [geographyLevel]),
        }),
      };
    default:
      return {
        level: "campaign",
        fields: ["campaign_id", "campaign_name"],
        breakdowns: undefined,
        identifyRow: (insight: any) => ({
          id: insight.campaign_id,
          name: insight.campaign_name || insight.campaign_id,
          type: "campaign",
          label: insight.campaign_name || insight.campaign_id,
        }),
      };
  }
}

function rankWinnerRows(
  insights: AdInsights[],
  conversionContext: any,
  winnerConfig: any,
  sortBy: string,
  topN: number,
  minSpend: number,
) {
  const rows = insights
    .map((insight: any) => {
      const identity = winnerConfig.identifyRow(insight);
      const primary_result = extractPrimaryResult([insight], conversionContext);
      return {
        ...identity,
        impressions: parseFloat(insight.impressions || "0"),
        clicks: parseFloat(insight.clicks || "0"),
        spend: round2(parseFloat(insight.spend || "0")),
        ctr: parseFloat(insight.ctr || "0"),
        cpc: insight.cpc ? parseFloat(insight.cpc) : null,
        cpm: insight.cpm ? parseFloat(insight.cpm) : null,
        primary_result,
        date_start: insight.date_start,
        date_stop: insight.date_stop,
      };
    })
    .filter((row) => row.spend >= minSpend);

  const sorted = rows.sort((a, b) => compareWinnerRows(a, b, sortBy));
  return sorted.slice(0, topN);
}

function rankLoserRows(
  insights: AdInsights[],
  conversionContext: any,
  loserConfig: any,
  sortBy: string,
  topN: number,
  minSpend: number,
) {
  const rows = insights
    .map((insight: any) => {
      const identity = loserConfig.identifyRow(insight);
      const primary_result = extractPrimaryResult([insight], conversionContext);
      const results = primary_result?.results || 0;
      return {
        ...identity,
        impressions: parseFloat(insight.impressions || "0"),
        clicks: parseFloat(insight.clicks || "0"),
        spend: round2(parseFloat(insight.spend || "0")),
        ctr: parseFloat(insight.ctr || "0"),
        cpc: insight.cpc ? parseFloat(insight.cpc) : null,
        cpm: insight.cpm ? parseFloat(insight.cpm) : null,
        primary_result,
        waste_score: results === 0 ? round2(parseFloat(insight.spend || "0")) : 0,
        date_start: insight.date_start,
        date_stop: insight.date_stop,
      };
    })
    .filter((row) => row.spend >= minSpend);

  const sorted = rows.sort((a, b) => compareLoserRows(a, b, sortBy));
  return sorted.slice(0, topN);
}

function compareWinnerRows(a: any, b: any, sortBy: string) {
  if (sortBy === "cost_per_result") {
    const aHasResults = (a.primary_result?.results || 0) > 0;
    const bHasResults = (b.primary_result?.results || 0) > 0;
    if (aHasResults && !bHasResults) return -1;
    if (!aHasResults && bHasResults) return 1;
    const aValue = a.primary_result?.cost_per_result ?? Number.POSITIVE_INFINITY;
    const bValue = b.primary_result?.cost_per_result ?? Number.POSITIVE_INFINITY;
    return aValue - bValue;
  }

  if (sortBy === "spend") {
    return b.spend - a.spend;
  }

  if (sortBy === "ctr") {
    return (b.ctr || 0) - (a.ctr || 0);
  }

  return (b.primary_result?.results || 0) - (a.primary_result?.results || 0);
}

function compareLoserRows(a: any, b: any, sortBy: string) {
  if (sortBy === "results") {
    const resultsDelta = (a.primary_result?.results || 0) - (b.primary_result?.results || 0);
    if (resultsDelta !== 0) return resultsDelta;
    return (b.spend || 0) - (a.spend || 0);
  }

  if (sortBy === "spend") {
    return (b.spend || 0) - (a.spend || 0);
  }

  if (sortBy === "ctr") {
    return (a.ctr || 0) - (b.ctr || 0);
  }

  const aHasResults = (a.primary_result?.results || 0) > 0;
  const bHasResults = (b.primary_result?.results || 0) > 0;
  if (!aHasResults && bHasResults) return -1;
  if (aHasResults && !bHasResults) return 1;

  const aValue = a.primary_result?.cost_per_result ?? -1;
  const bValue = b.primary_result?.cost_per_result ?? -1;
  if (aValue === -1 && bValue !== -1) return -1;
  if (aValue !== -1 && bValue === -1) return 1;
  if (aValue !== bValue) return bValue - aValue;
  return (b.spend || 0) - (a.spend || 0);
}

function getActionValue(insight: AdInsights, actionTypes: string[]) {
  const typeSet = new Set(actionTypes);
  return (insight.actions || []).reduce((sum, action) => {
    if (!typeSet.has(action.action_type)) return sum;
    return sum + parseFloat(action.value || "0");
  }, 0);
}

function safeRate(numerator: number, denominator: number) {
  if (!denominator) return 0;
  return round2((numerator / denominator) * 100);
}

function safeCost(spend: number, denominator: number) {
  if (!denominator) return null;
  return round2(spend / denominator);
}

function round2(value: number) {
  return Math.round(value * 100) / 100;
}

function calculateSummaryMetrics(insights: AdInsights[]): any {
  if (insights.length === 0) {
    return {
      total_impressions: 0,
      total_clicks: 0,
      total_spend: 0,
      average_ctr: 0,
      average_cpc: 0,
      average_cpm: 0,
      total_reach: 0,
      average_frequency: 0,
    };
  }

  const totals = insights.reduce(
    (acc, insight) => {
      acc.impressions += parseFloat(insight.impressions || "0");
      acc.clicks += parseFloat(insight.clicks || "0");
      acc.spend += parseFloat(insight.spend || "0");
      acc.reach += parseFloat(insight.reach || "0");
      return acc;
    },
    { impressions: 0, clicks: 0, spend: 0, reach: 0 },
  );

  const averageCtr = totals.impressions > 0 ? (totals.clicks / totals.impressions) * 100 : 0;
  const averageCpc = totals.clicks > 0 ? totals.spend / totals.clicks : 0;
  const averageCpm = totals.impressions > 0 ? (totals.spend / totals.impressions) * 1000 : 0;
  const averageFrequency = totals.reach > 0 ? totals.impressions / totals.reach : 0;

  return {
    total_impressions: Math.round(totals.impressions),
    total_clicks: Math.round(totals.clicks),
    total_spend: Math.round(totals.spend * 100) / 100,
    average_ctr: Math.round(averageCtr * 100) / 100,
    average_cpc: Math.round(averageCpc * 100) / 100,
    average_cpm: Math.round(averageCpm * 100) / 100,
    total_reach: Math.round(totals.reach),
    average_frequency: Math.round(averageFrequency * 100) / 100,
    date_range: {
      start: insights[0]?.date_start,
      end: insights[insights.length - 1]?.date_stop,
    },
  };
}

function calculatePerformanceRankings(comparisons: any[], metrics: string[]): any {
  const rankings: any = {};

  for (const metric of metrics) {
    const validComparisons = comparisons.filter((c) => c.metrics && !c.error);
    if (validComparisons.length === 0) continue;

    const sorted = validComparisons
      .map((c) => ({
        object_id: c.object_id,
        object_name: c.object_name,
        value: getMetricValue(c.metrics, metric),
      }))
      .filter((item) => item.value !== null)
      .sort((a, b) => {
        const isCostMetric = metric.includes("cpc") || metric.includes("cpm") || metric.includes("spend");
        return isCostMetric ? (a.value || 0) - (b.value || 0) : (b.value || 0) - (a.value || 0);
      });

    rankings[metric] = sorted.map((item, index) => ({
      rank: index + 1,
      object_id: item.object_id,
      object_name: item.object_name,
      value: item.value,
    }));
  }

  return rankings;
}

function getMetricValue(metrics: any, metricName: string): number | null {
  const value = metrics[`total_${metricName}`] || metrics[`average_${metricName}`] || metrics[metricName];
  return value !== undefined ? parseFloat(value) : null;
}

function calculateAttributionMetrics(insights: AdInsights[]): any {
  const attributionSummary: any = {
    total_conversions: 0,
    attribution_windows: {},
    cost_per_conversion: 0,
    conversion_rate: 0,
  };

  insights.forEach((insight) => {
    if (insight.actions) {
      insight.actions.forEach((action) => {
        if (action.action_type === "purchase" || action.action_type === "complete_registration") {
          attributionSummary.total_conversions += parseFloat(action.value);
        }
      });
    }
  });

  const totalSpend = insights.reduce((sum, insight) => sum + parseFloat(insight.spend || "0"), 0);
  const totalClicks = insights.reduce((sum, insight) => sum + parseFloat(insight.clicks || "0"), 0);

  if (attributionSummary.total_conversions > 0) {
    attributionSummary.cost_per_conversion = totalSpend / attributionSummary.total_conversions;
  }
  if (totalClicks > 0) {
    attributionSummary.conversion_rate = (attributionSummary.total_conversions / totalClicks) * 100;
  }

  return attributionSummary;
}

function convertToCSV(data: any[]): string {
  if (data.length === 0) return "";

  const headers = new Set<string>();
  data.forEach((row) => Object.keys(row).forEach((key) => headers.add(key)));

  const headerArray = Array.from(headers);
  const csvRows = [headerArray.join(",")];

  data.forEach((row) => {
    const values = headerArray.map((header) => {
      const value = (row as any)[header];
      if (value === null || value === undefined) return "";
      if (typeof value === "object") return JSON.stringify(value);
      return String(value).replace(/"/g, '""');
    });
    csvRows.push(values.map((v) => `"${v}"`).join(","));
  });

  return csvRows.join("\n");
}

