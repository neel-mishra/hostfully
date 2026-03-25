import { MetaApiClient } from "../meta-client.js";
import type { AdInsights } from "../types/meta-api.js";

export interface ConversionContext {
  label: string;
  action_type: string;
  optimization_goal?: string;
  source: string;
  labels?: string[];
}

export interface PrimaryResult {
  label: string;
  action_type: string;
  results: number;
  cost_per_result: number | null;
}

function parseMetricValue(value?: string): number {
  return parseFloat(value || "0");
}

function buildPrimaryConversionCandidates(conversionContext: ConversionContext): string[] {
  const candidates = new Set<string>();
  candidates.add(conversionContext.action_type);

  // Meta reports custom conversions with the specific conversion name appended.
  if (conversionContext.action_type === "offsite_conversion.fb_pixel_custom" && conversionContext.label) {
    candidates.add(`offsite_conversion.fb_pixel_custom.${conversionContext.label}`);
  }

  return Array.from(candidates);
}

function buildPrimaryActionCandidates(conversionContext: ConversionContext): string[] {
  const label = (conversionContext.label || "").toLowerCase();

  // Ads Manager often reports the "Results" column for lead-optimized campaigns
  // under normalized lead aliases instead of the raw offsite pixel event name.
  if (label === "lead" || conversionContext.action_type === "offsite_conversion.fb_pixel_lead") {
    return [
      "lead",
      "onsite_conversion.lead_grouped",
      "offsite_conversion.fb_pixel_lead",
      "onsite_web_lead",
      "offsite_complete_registration_add_meta_leads",
      "offsite_submit_application_add_meta_leads",
      "offsite_search_add_meta_leads",
      "offsite_content_view_add_meta_leads",
      "offsite_contact_website_add_meta_leads",
    ];
  }

  if (label === "purchase" || conversionContext.action_type === "offsite_conversion.fb_pixel_purchase") {
    return ["purchase", "offsite_conversion.fb_pixel_purchase"];
  }

  if (
    label === "complete_registration" ||
    conversionContext.action_type === "offsite_conversion.fb_pixel_complete_registration"
  ) {
    return [
      "complete_registration",
      "offsite_conversion.fb_pixel_complete_registration",
      "offsite_complete_registration_add_meta_leads",
    ];
  }

  return [conversionContext.action_type];
}

export function extractCreativeCopyPreview(creative: any): {
  headline?: string;
  body?: string;
  primary_text?: string;
} | null {
  if (!creative) return null;

  const objectStorySpec = creative.object_story_spec || {};
  const linkData = objectStorySpec.link_data || {};
  const videoData = objectStorySpec.video_data || {};
  const templateData = objectStorySpec.template_data || {};
  const assetFeedSpec = creative.asset_feed_spec || {};

  const headline =
    creative.title ||
    linkData.name ||
    videoData.title ||
    templateData.name ||
    assetFeedSpec.titles?.[0]?.text;

  const body =
    creative.body ||
    linkData.description ||
    videoData.description ||
    templateData.description ||
    assetFeedSpec.descriptions?.[0]?.text;

  const primary_text =
    linkData.message ||
    videoData.message ||
    templateData.message ||
    assetFeedSpec.bodies?.[0]?.text;

  if (!headline && !body && !primary_text) return null;

  return {
    ...(headline ? { headline } : {}),
    ...(body ? { body } : {}),
    ...(primary_text ? { primary_text } : {}),
  };
}

function buildConversionContextFromPromotedObject(
  promotedObject: any,
  optimizationGoal?: string,
): ConversionContext | null {
  if (!promotedObject) return null;

  if (promotedObject.custom_event_str) {
    return {
      label: promotedObject.custom_event_str,
      action_type: "offsite_conversion.fb_pixel_custom",
      optimization_goal: optimizationGoal,
      source: "adset.promoted_object.custom_event_str",
    };
  }

  if (promotedObject.custom_event_type && promotedObject.custom_event_type !== "OTHER") {
    const normalized = String(promotedObject.custom_event_type).toLowerCase();
    return {
      label: normalized,
      action_type: `offsite_conversion.fb_pixel_${normalized}`,
      optimization_goal: optimizationGoal,
      source: "adset.promoted_object.custom_event_type",
    };
  }

  return null;
}

function dedupeContexts(contexts: ConversionContext[]): ConversionContext[] {
  const seen = new Map<string, ConversionContext>();
  for (const context of contexts) {
    seen.set(`${context.label}::${context.action_type}`, context);
  }
  return Array.from(seen.values());
}

export async function resolveConversionContext(
  metaClient: MetaApiClient,
  objectId: string,
  level: string,
): Promise<ConversionContext | null> {
  try {
    if (level === "account") {
      const adSets = await fetchAllAccountAdSets(metaClient, objectId, { maxPages: 3, maxItems: 300 });
      const contexts = dedupeContexts(
        adSets
          .map((adSet: any) =>
            buildConversionContextFromPromotedObject(adSet.promoted_object, adSet.optimization_goal),
          )
          .filter(Boolean) as ConversionContext[],
      );

      if (contexts.length === 1) return contexts[0];
      if (contexts.length > 1) {
        return {
          label: contexts.map((c) => c.label).join(", "),
          labels: contexts.map((c) => c.label),
          action_type: contexts[0].action_type,
          optimization_goal: contexts[0].optimization_goal,
          source: "account.adsets.promoted_object",
        };
      }
      return null;
    }

    if (level === "campaign") {
      const adSets = await metaClient.getAdSets({
        campaignId: objectId,
        limit: 100,
        fields: ["id", "name", "optimization_goal", "promoted_object", "status"],
      });

      const contexts = dedupeContexts(
        adSets.data
          .map((adSet: any) =>
            buildConversionContextFromPromotedObject(adSet.promoted_object, adSet.optimization_goal),
          )
          .filter(Boolean) as ConversionContext[],
      );

      if (contexts.length === 1) return contexts[0];
      if (contexts.length > 1) {
        return {
          label: contexts.map((c) => c.label).join(", "),
          labels: contexts.map((c) => c.label),
          action_type: contexts[0].action_type,
          optimization_goal: contexts[0].optimization_goal,
          source: "campaign.adsets.promoted_object",
        };
      }
      return null;
    }

    if (level === "adset") {
      const adSet: any = await metaClient.getAdSet(objectId, [
        "id",
        "name",
        "campaign_id",
        "optimization_goal",
        "promoted_object",
        "status",
      ]);
      return buildConversionContextFromPromotedObject(adSet.promoted_object, adSet.optimization_goal);
    }

    if (level === "ad") {
      const ad: any = await metaClient.getAd(objectId, [
        "id",
        "name",
        "adset_id",
        "campaign_id",
        "creative{id,name,title,body,object_story_spec,asset_feed_spec}",
      ]);
      if (!ad.adset_id) return null;
      return resolveConversionContext(metaClient, ad.adset_id, "adset");
    }

    return null;
  } catch {
    return null;
  }
}

export function extractPrimaryResult(
  insights: AdInsights[],
  conversionContext?: ConversionContext | null,
): PrimaryResult | null {
  const actionTotals = new Map<string, number>();
  const conversionTotals = new Map<string, number>();
  const costTotals = new Map<string, number>();
  const totalSpend = insights.reduce((sum, insight) => sum + parseMetricValue(insight.spend), 0);

  for (const insight of insights) {
    for (const action of insight.actions || []) {
      actionTotals.set(
        action.action_type,
        (actionTotals.get(action.action_type) || 0) + parseMetricValue(action.value),
      );
    }

    for (const conversion of insight.conversions || []) {
      conversionTotals.set(
        conversion.action_type,
        (conversionTotals.get(conversion.action_type) || 0) + parseMetricValue(conversion.value),
      );
    }

    for (const cost of insight.cost_per_action_type || []) {
      costTotals.set(cost.action_type, parseMetricValue(cost.value));
    }
  }

  if (conversionContext?.action_type) {
    const conversionCandidates = buildPrimaryConversionCandidates(conversionContext);
    const exactConversionType = conversionCandidates.find((candidate) => conversionTotals.has(candidate));
    const actionCandidates = buildPrimaryActionCandidates(conversionContext);
    const exactActionType = actionCandidates.find((candidate) => actionTotals.has(candidate));
    const exactResults = exactConversionType
      ? conversionTotals.get(exactConversionType) || 0
      : exactActionType
        ? actionTotals.get(exactActionType) || 0
        : actionTotals.get(conversionContext.action_type) || 0;
    const exactCostType = exactConversionType
      ? actionCandidates.find((candidate) => costTotals.has(candidate))
      : exactActionType || actionCandidates.find((candidate) => costTotals.has(candidate));

    return {
      label: conversionContext.label,
      action_type: exactConversionType || exactActionType || conversionContext.action_type,
      results: exactResults,
      // Meta only exposes generic cost rows for custom conversions, so derive cost from spend
      // whenever we match an exact primary conversion to avoid blended custom-conversion CPAs.
      cost_per_result:
        exactConversionType && exactResults > 0
          ? Math.round((totalSpend / exactResults) * 100) / 100
          : (exactCostType ? costTotals.get(exactCostType) : undefined) ||
            costTotals.get(conversionContext.action_type) ||
            null,
    };
  }

  const fallbackPriority = [
    "purchase",
    "offsite_conversion.fb_pixel_purchase",
    "lead",
    "offsite_conversion.fb_pixel_lead",
    "onsite_web_lead",
    "complete_registration",
    "offsite_conversion.fb_pixel_complete_registration",
    "offsite_complete_registration_add_meta_leads",
    "offsite_conversion.fb_pixel_custom",
  ];

  for (const actionType of fallbackPriority) {
    if (actionTotals.has(actionType)) {
      return {
        label: actionType,
        action_type: actionType,
        results: actionTotals.get(actionType) || 0,
        cost_per_result: costTotals.get(actionType) || null,
      };
    }
  }

  return null;
}

export async function getPrimaryResultLast7d(
  metaClient: MetaApiClient,
  objectId: string,
  level: "campaign" | "adset" | "ad",
  conversionContext?: ConversionContext | null,
): Promise<PrimaryResult | null> {
  try {
    const result = await metaClient.getInsights(objectId, {
      level,
      date_preset: "last_7d",
      fields: ["actions", "conversions", "cost_per_action_type", "spend"],
      limit: 25,
    });
    return extractPrimaryResult(result.data, conversionContext);
  } catch {
    return null;
  }
}

export async function fetchAllAccountAdSets(
  metaClient: MetaApiClient,
  accountId: string,
  options: { maxPages?: number; maxItems?: number } = {},
): Promise<any[]> {
  const adSets: any[] = [];
  let after: string | undefined;
  let pageCount = 0;
  const maxPages = options.maxPages ?? 2;
  const maxItems = options.maxItems ?? 200;

  do {
    const result = await metaClient.getAdSets({
      accountId,
      limit: 100,
      after,
      fields: ["id", "name", "campaign_id", "optimization_goal", "promoted_object", "targeting", "status"],
    });
    adSets.push(...result.data);
    pageCount += 1;
    after = result.paging?.cursors?.after;
    if (!result.hasNextPage || pageCount >= maxPages || adSets.length >= maxItems) break;
  } while (after);

  if (adSets.length > maxItems) {
    adSets.splice(maxItems);
  }

  return adSets;
}

export async function fetchAllAccountAds(
  metaClient: MetaApiClient,
  accountId: string,
  options: { maxPages?: number; maxItems?: number } = {},
): Promise<any[]> {
  const ads: any[] = [];
  let after: string | undefined;
  let pageCount = 0;
  const maxPages = options.maxPages ?? 2;
  const maxItems = options.maxItems ?? 200;

  do {
    const result = await metaClient.getAds({
      accountId,
      limit: 100,
      after,
      fields: [
        "id",
        "name",
        "adset_id",
        "campaign_id",
        "status",
        "creative{id,name,title,body,object_story_spec,asset_feed_spec}",
      ],
    });
    ads.push(...result.data);
    pageCount += 1;
    after = result.paging?.cursors?.after;
    if (!result.hasNextPage || pageCount >= maxPages || ads.length >= maxItems) break;
  } while (after);

  if (ads.length > maxItems) {
    ads.splice(maxItems);
  }

  return ads;
}

export async function analyzeAudienceUsage(
  metaClient: MetaApiClient,
  accountId: string,
  audienceIds: string[],
): Promise<Record<string, any>> {
  const adSets = await fetchAllAccountAdSets(metaClient, accountId);
  const lookup = new Set(audienceIds);
  const byAudience: Record<string, any> = {};

  for (const audienceId of audienceIds) {
    byAudience[audienceId] = {
      linked_ad_set_count: 0,
      linked_campaign_ids: [] as string[],
      linked_conversion_actions: [] as string[],
    };
  }

  for (const adSet of adSets) {
    const targeting = adSet.targeting || {};
    const ids = [
      ...(targeting.custom_audiences || []),
      ...(targeting.excluded_custom_audiences || []),
      ...(targeting.lookalike_audiences || []),
    ]
      .map((item: any) => item.id)
      .filter(Boolean);

    const context = buildConversionContextFromPromotedObject(adSet.promoted_object, adSet.optimization_goal);
    for (const id of ids) {
      if (!lookup.has(id)) continue;
      byAudience[id].linked_ad_set_count += 1;
      if (adSet.campaign_id) byAudience[id].linked_campaign_ids.push(adSet.campaign_id);
      if (context?.label) byAudience[id].linked_conversion_actions.push(context.label);
    }
  }

  for (const audienceId of audienceIds) {
    byAudience[audienceId].linked_campaign_ids = Array.from(new Set(byAudience[audienceId].linked_campaign_ids));
    byAudience[audienceId].linked_conversion_actions = Array.from(
      new Set(byAudience[audienceId].linked_conversion_actions),
    );
  }

  return byAudience;
}

export async function analyzeCreativeUsage(
  metaClient: MetaApiClient,
  accountId: string,
  creativeIds: string[],
): Promise<Record<string, any>> {
  const ads = await fetchAllAccountAds(metaClient, accountId);
  const adSets = await fetchAllAccountAdSets(metaClient, accountId);
  const adSetMap = new Map(adSets.map((adSet: any) => [adSet.id, adSet]));
  const lookup = new Set(creativeIds);
  const byCreative: Record<string, any> = {};

  for (const creativeId of creativeIds) {
    byCreative[creativeId] = {
      linked_ad_count: 0,
      linked_ad_ids: [] as string[],
      linked_conversion_actions: [] as string[],
      copy_preview: null as any,
    };
  }

  for (const ad of ads) {
    const creativeId = ad.creative?.id;
    if (!creativeId || !lookup.has(creativeId)) continue;

    byCreative[creativeId].linked_ad_count += 1;
    byCreative[creativeId].linked_ad_ids.push(ad.id);
    if (!byCreative[creativeId].copy_preview) {
      byCreative[creativeId].copy_preview = extractCreativeCopyPreview(ad.creative);
    }

    const adSet = adSetMap.get(ad.adset_id);
    const context = buildConversionContextFromPromotedObject(adSet?.promoted_object, adSet?.optimization_goal);
    if (context?.label) {
      byCreative[creativeId].linked_conversion_actions.push(context.label);
    }
  }

  for (const creativeId of creativeIds) {
    byCreative[creativeId].linked_ad_ids = Array.from(new Set(byCreative[creativeId].linked_ad_ids));
    byCreative[creativeId].linked_conversion_actions = Array.from(
      new Set(byCreative[creativeId].linked_conversion_actions),
    );
  }

  return byCreative;
}

