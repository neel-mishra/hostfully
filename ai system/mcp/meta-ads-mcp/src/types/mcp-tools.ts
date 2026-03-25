import { z } from "zod";

// Campaign Management Schemas
// NOTE: We intentionally annotate these as `any` to avoid TypeScript OOMs
// caused by deep Zod type inference on large schema graphs.
export const ListCampaignsSchema: any = z.object({
  account_id: z.string().describe("Meta Ad Account ID"),
  status: z
    .enum(["ACTIVE", "PAUSED", "DELETED", "ARCHIVED"])
    .optional()
    .describe("Filter by campaign status"),
  limit: z
    .number()
    .min(1)
    .max(100)
    .default(25)
    .describe("Number of campaigns to return"),
  after: z.string().optional().describe("Pagination cursor for next page"),
});

export const CreateCampaignSchema: any = z.object({
  account_id: z.string().describe("Meta Ad Account ID"),
  name: z.string().min(1).describe("Campaign name"),
  objective: z
    .enum([
      "OUTCOME_APP_PROMOTION",
      "OUTCOME_AWARENESS",
      "OUTCOME_ENGAGEMENT",
      "OUTCOME_LEADS",
      "OUTCOME_SALES",
      "OUTCOME_TRAFFIC",
    ])
    .describe(
      "Campaign objective using Outcome-Driven Ad Experience (ODAE) format",
    ),
  status: z
    .enum(["ACTIVE", "PAUSED"])
    .default("PAUSED")
    .describe("Initial campaign status"),
  daily_budget: z
    .number()
    .positive()
    .optional()
    .describe("Daily budget in account currency cents"),
  lifetime_budget: z
    .number()
    .positive()
    .optional()
    .describe("Lifetime budget in account currency cents"),
  start_time: z.string().optional().describe("Campaign start time (ISO 8601)"),
  stop_time: z.string().optional().describe("Campaign stop time (ISO 8601)"),
  special_ad_categories: z
    .array(
      z.enum([
        "NONE",
        "EMPLOYMENT",
        "HOUSING",
        "CREDIT",
        "SOCIAL_ISSUES_ELECTIONS_POLITICS",
      ]),
    )
    .optional()
    .describe("Special ad categories (required for regulated industries)"),
  bid_strategy: z
    .enum(["LOWEST_COST_WITHOUT_CAP", "LOWEST_COST_WITH_BID_CAP", "COST_CAP"])
    .optional()
    .describe("Bid strategy for the campaign"),
  bid_cap: z
    .number()
    .positive()
    .optional()
    .describe("Bid cap amount in account currency cents"),
  budget_optimization: z
    .boolean()
    .optional()
    .describe("Enable campaign budget optimization across ad sets"),
});

export const UpdateCampaignSchema: any = z.object({
  campaign_id: z.string().describe("Campaign ID to update"),
  name: z.string().optional().describe("New campaign name"),
  status: z
    .enum(["ACTIVE", "PAUSED", "ARCHIVED"])
    .optional()
    .describe("New campaign status"),
  daily_budget: z
    .number()
    .positive()
    .optional()
    .describe("New daily budget in account currency cents"),
  lifetime_budget: z
    .number()
    .positive()
    .optional()
    .describe("New lifetime budget in account currency cents"),
  start_time: z.string().optional().describe("New campaign start time (ISO 8601)"),
  stop_time: z.string().optional().describe("New campaign stop time (ISO 8601)"),
});

export const DeleteCampaignSchema: any = z.object({
  campaign_id: z.string().describe("Campaign ID to delete"),
});

// Ad Set Management Schemas
export const ListAdSetsSchema: any = z.object({
  campaign_id: z.string().optional().describe("Filter by campaign ID"),
  account_id: z.string().optional().describe("Filter by account ID"),
  status: z
    .enum(["ACTIVE", "PAUSED", "DELETED", "ARCHIVED"])
    .optional()
    .describe("Filter by ad set status"),
  limit: z.number().min(1).max(100).default(25).describe("Limit results"),
  after: z.string().optional().describe("Pagination cursor"),
});

export const CreateAdSetSchema: any = z.object({
  account_id: z.string().describe("Meta Ad Account ID"),
  campaign_id: z.string().describe("Campaign ID"),
  name: z.string().min(1).describe("Ad set name"),
  status: z.enum(["ACTIVE", "PAUSED"]).default("PAUSED"),
  daily_budget: z.number().positive().optional(),
  lifetime_budget: z.number().positive().optional(),
  billing_event: z
    .string()
    .optional()
    .describe("Billing event (e.g. IMPRESSIONS, LINK_CLICKS)"),
  optimization_goal: z
    .string()
    .optional()
    .describe("Optimization goal (e.g. LINK_CLICKS, CONVERSIONS)"),
  bid_amount: z.number().positive().optional().describe("Bid amount in cents"),
  start_time: z.string().optional().describe("Start time (ISO 8601)"),
  end_time: z.string().optional().describe("End time (ISO 8601)"),
  targeting: z
    .record(z.any())
    .describe("Targeting spec (Meta AdTargeting object)"),
  promoted_object: z
    .record(z.any())
    .optional()
    .describe("Promoted object spec"),
});

export const UpdateAdSetSchema: any = z.object({
  adset_id: z.string().describe("Ad set ID to update"),
  name: z.string().optional(),
  status: z.enum(["ACTIVE", "PAUSED", "ARCHIVED"]).optional(),
  daily_budget: z.number().positive().optional(),
  lifetime_budget: z.number().positive().optional(),
  bid_amount: z.number().positive().optional(),
  targeting: z.record(z.any()).optional(),
});

// Ads Schemas
export const ListAdsSchema: any = z.object({
  adset_id: z.string().optional().describe("Filter by ad set ID"),
  campaign_id: z.string().optional().describe("Filter by campaign ID"),
  account_id: z.string().optional().describe("Filter by account ID"),
  status: z
    .enum(["ACTIVE", "PAUSED", "DELETED", "ARCHIVED"])
    .optional()
    .describe("Filter by ad status"),
  limit: z.number().min(1).max(100).default(25).describe("Limit results"),
  after: z.string().optional().describe("Pagination cursor"),
});

export const CreateAdSchema: any = z.object({
  account_id: z.string().describe("Meta Ad Account ID"),
  adset_id: z.string().describe("Ad set ID"),
  name: z.string().min(1).describe("Ad name"),
  status: z.enum(["ACTIVE", "PAUSED"]).default("PAUSED"),
  creative: z
    .record(z.any())
    .describe("Creative spec (or reference to creative_id)"),
});

export const UpdateAdSchema: any = z.object({
  ad_id: z.string().describe("Ad ID to update"),
  name: z.string().optional(),
  status: z.enum(["ACTIVE", "PAUSED", "ARCHIVED"]).optional(),
});

// Analytics Schemas
export const GetInsightsSchema: any = z.object({
  object_id: z.string().describe("Campaign/Ad Set/Ad/Account ID"),
  level: z
    .enum(["account", "campaign", "adset", "ad"])
    .default("campaign")
    .describe("Insights level"),
  date_preset: z
    .string()
    .optional()
    .describe("Meta date preset (e.g. last_7d, last_30d)"),
  time_range: z
    .record(z.string())
    .optional()
    .describe("Custom time range: { since: YYYY-MM-DD, until: YYYY-MM-DD }"),
  fields: z.array(z.string()).optional().describe("Fields to request"),
  breakdowns: z.array(z.string()).optional().describe("Breakdowns to request"),
  limit: z.number().min(1).max(1000).optional().describe("Result limit"),
});

export const ComparePerformanceSchema: any = z.object({
  object_ids: z.array(z.string()).min(1).max(10),
  level: z.enum(["campaign", "adset", "ad"]).default("campaign"),
  date_preset: z.string().optional(),
  time_range: z.record(z.string()).optional(),
  metrics: z.array(z.string()).min(1).describe("Metric field names"),
});

export const ExportInsightsSchema: any = z.object({
  object_id: z.string(),
  level: z.enum(["account", "campaign", "adset", "ad"]).default("campaign"),
  format: z.enum(["json", "csv"]).default("json"),
  date_preset: z.string().optional(),
  time_range: z.record(z.string()).optional(),
  fields: z.array(z.string()).optional(),
  breakdowns: z.array(z.string()).optional(),
});

export const AnalyzePlacementsSchema: any = z.object({
  object_id: z.string().describe("Campaign/Ad Set/Ad/Account ID"),
  level: z.enum(["account", "campaign", "adset", "ad"]).default("campaign"),
  date_preset: z.string().optional().describe("Meta date preset (e.g. last_7d, last_30d)"),
  time_range: z
    .record(z.string())
    .optional()
    .describe("Custom time range: { since: YYYY-MM-DD, until: YYYY-MM-DD }"),
  limit: z.number().min(1).max(1000).optional().describe("Result limit"),
  fields: z.array(z.string()).optional().describe("Additional insight fields to request"),
});

export const AnalyzeDevicesSchema: any = z.object({
  object_id: z.string().describe("Campaign/Ad Set/Ad/Account ID"),
  level: z.enum(["account", "campaign", "adset", "ad"]).default("campaign"),
  date_preset: z.string().optional().describe("Meta date preset (e.g. last_7d, last_30d)"),
  time_range: z
    .record(z.string())
    .optional()
    .describe("Custom time range: { since: YYYY-MM-DD, until: YYYY-MM-DD }"),
  limit: z.number().min(1).max(1000).optional().describe("Result limit"),
  fields: z.array(z.string()).optional().describe("Additional insight fields to request"),
});

export const AnalyzeDemographicsSchema: any = z.object({
  object_id: z.string().describe("Campaign/Ad Set/Ad/Account ID"),
  level: z.enum(["account", "campaign", "adset", "ad"]).default("campaign"),
  date_preset: z.string().optional().describe("Meta date preset (e.g. last_7d, last_30d)"),
  time_range: z
    .record(z.string())
    .optional()
    .describe("Custom time range: { since: YYYY-MM-DD, until: YYYY-MM-DD }"),
  limit: z.number().min(1).max(1000).optional().describe("Result limit"),
  fields: z.array(z.string()).optional().describe("Additional insight fields to request"),
});

export const AnalyzeGeoSchema: any = z.object({
  object_id: z.string().describe("Campaign/Ad Set/Ad/Account ID"),
  level: z.enum(["account", "campaign", "adset", "ad"]).default("campaign"),
  geography_level: z
    .enum(["country", "region", "dma"])
    .default("country")
    .describe("Geographic granularity to analyze"),
  date_preset: z.string().optional().describe("Meta date preset (e.g. last_7d, last_30d)"),
  time_range: z
    .record(z.string())
    .optional()
    .describe("Custom time range: { since: YYYY-MM-DD, until: YYYY-MM-DD }"),
  limit: z.number().min(1).max(1000).optional().describe("Result limit"),
  fields: z.array(z.string()).optional().describe("Additional insight fields to request"),
});

export const AnalyzeFunnelSchema: any = z.object({
  object_id: z.string().describe("Campaign/Ad Set/Ad/Account ID"),
  level: z.enum(["account", "campaign", "adset", "ad"]).default("campaign"),
  date_preset: z.string().optional().describe("Meta date preset (e.g. last_7d, last_30d)"),
  time_range: z
    .record(z.string())
    .optional()
    .describe("Custom time range: { since: YYYY-MM-DD, until: YYYY-MM-DD }"),
  limit: z.number().min(1).max(1000).optional().describe("Result limit"),
  fields: z.array(z.string()).optional().describe("Additional insight fields to request"),
});

export const AnalyzeWinnersSchema: any = z.object({
  object_id: z.string().describe("Parent Campaign/Ad Set/Ad/Account ID"),
  scope: z
    .enum(["campaigns", "adsets", "ads", "placements", "devices", "demographics", "geo"])
    .describe("What to rank"),
  geography_level: z
    .enum(["country", "region", "dma"])
    .default("country")
    .optional()
    .describe("Geo granularity when scope is geo"),
  date_preset: z.string().optional().describe("Meta date preset (e.g. last_7d, last_30d)"),
  time_range: z
    .record(z.string())
    .optional()
    .describe("Custom time range: { since: YYYY-MM-DD, until: YYYY-MM-DD }"),
  fields: z.array(z.string()).optional().describe("Additional insight fields to request"),
  limit: z.number().min(1).max(1000).optional().describe("Meta row limit"),
  top_n: z.number().min(1).max(50).default(10).optional().describe("How many winners to return"),
  min_spend: z.number().min(0).optional().describe("Minimum spend filter before ranking"),
  sort_by: z
    .enum(["results", "cost_per_result", "spend", "ctr"])
    .default("results")
    .optional()
    .describe("Ranking metric"),
});

export const AnalyzeLosersSchema: any = z.object({
  object_id: z.string().describe("Parent Campaign/Ad Set/Ad/Account ID"),
  scope: z
    .enum(["campaigns", "adsets", "ads", "placements", "devices", "demographics", "geo"])
    .describe("What to rank"),
  geography_level: z
    .enum(["country", "region", "dma"])
    .default("country")
    .optional()
    .describe("Geo granularity when scope is geo"),
  date_preset: z.string().optional().describe("Meta date preset (e.g. last_7d, last_30d)"),
  time_range: z
    .record(z.string())
    .optional()
    .describe("Custom time range: { since: YYYY-MM-DD, until: YYYY-MM-DD }"),
  fields: z.array(z.string()).optional().describe("Additional insight fields to request"),
  limit: z.number().min(1).max(1000).optional().describe("Meta row limit"),
  top_n: z.number().min(1).max(50).default(10).optional().describe("How many losers to return"),
  min_spend: z.number().min(0).default(0).optional().describe("Minimum spend filter before ranking"),
  sort_by: z
    .enum(["results", "cost_per_result", "spend", "ctr"])
    .default("cost_per_result")
    .optional()
    .describe("Loss metric"),
});

export const AnalyzeAccountSchema: any = z.object({
  object_id: z.string().describe("Account/Campaign/Ad Set/Ad ID"),
  level: z.enum(["account", "campaign", "adset", "ad"]).default("account"),
  geography_level: z
    .enum(["country", "region", "dma"])
    .default("country")
    .optional()
    .describe("Geo granularity for the executive summary"),
  date_preset: z.string().optional().describe("Meta date preset (e.g. last_7d, last_30d)"),
  time_range: z
    .record(z.string())
    .optional()
    .describe("Custom time range: { since: YYYY-MM-DD, until: YYYY-MM-DD }"),
  fields: z.array(z.string()).optional().describe("Additional overview fields to request"),
  limit: z.number().min(1).max(1000).optional().describe("Meta row limit for detail queries"),
  top_n: z.number().min(1).max(20).default(5).optional().describe("How many top items to surface per section"),
  min_spend: z.number().min(0).default(0).optional().describe("Minimum spend filter for loser analysis"),
});

export const GenerateOptimizationBriefSchema: any = z.object({
  object_id: z.string().describe("Account/Campaign/Ad Set/Ad ID"),
  level: z.enum(["account", "campaign", "adset", "ad"]).default("account"),
  geography_level: z
    .enum(["country", "region", "dma"])
    .default("country")
    .optional()
    .describe("Geo granularity for the brief"),
  date_preset: z.string().optional().describe("Meta date preset (e.g. last_7d, last_30d)"),
  time_range: z
    .record(z.string())
    .optional()
    .describe("Custom time range: { since: YYYY-MM-DD, until: YYYY-MM-DD }"),
  top_n: z.number().min(1).max(20).default(5).optional().describe("How many items to use per section"),
  min_spend: z.number().min(0).default(0).optional().describe("Minimum spend filter for weak segments"),
});

// Audience Schemas
export const ListAudiencesSchema: any = z.object({
  account_id: z.string().describe("Meta Ad Account ID"),
  type: z
    .enum(["custom", "lookalike", "saved"])
    .optional()
    .describe("Filter by audience type"),
  limit: z.number().min(1).max(100).default(25).optional(),
  after: z.string().optional(),
});

export const CreateCustomAudienceSchema: any = z.object({
  account_id: z.string(),
  name: z.string().min(1),
  description: z.string().optional(),
  subtype: z.string().default("CUSTOM"),
  customer_file_source: z.string().optional(),
  retention_days: z.number().min(1).max(365).optional(),
  rule: z.record(z.any()).optional(),
});

export const CreateLookalikeAudienceSchema: any = z.object({
  account_id: z.string(),
  name: z.string().min(1),
  origin_audience_id: z.string(),
  country: z.string().length(2).describe("Country code (e.g. US)"),
  ratio: z.number().min(0.01).max(0.2).default(0.01),
  description: z.string().optional(),
});

export const EstimateAudienceSizeSchema: any = z.object({
  account_id: z.string(),
  targeting: z.record(z.any()).describe("Targeting spec"),
  optimization_goal: z.string().optional(),
});

// Creative Schemas
export const ListCreativesSchema: any = z.object({
  account_id: z.string(),
  limit: z.number().min(1).max(100).default(25).optional(),
  after: z.string().optional(),
});

export const CreateAdCreativeSchema: any = z.object({
  account_id: z.string(),
  name: z.string().min(1),
  object_story_spec: z.record(z.any()).optional(),
  body: z.string().optional(),
  title: z.string().optional(),
  image_url: z.string().url().optional(),
  url_tags: z.string().optional(),
  call_to_action: z.record(z.any()).optional(),
});

// OAuth Schemas
export const GenerateAuthUrlSchema: any = z.object({
  scopes: z.array(z.string()).default(["ads_management"]),
  state: z.string().optional(),
});

export const ExchangeCodeSchema: any = z.object({
  code: z.string().min(1),
});

export const RefreshTokenSchema: any = z.object({
  short_lived_token: z.string().optional(),
});

export const GenerateSystemTokenSchema: any = z.object({
  system_user_id: z.string().min(1),
  scopes: z.array(z.string()).default(["ads_management"]),
  expiring_token: z.boolean().default(true),
});

