import fetch from "node-fetch";
import { AuthManager } from "./utils/auth.js";
import { globalRateLimiter } from "./utils/rate-limiter.js";
import { MetaApiErrorHandler, retryWithBackoff } from "./utils/error-handler.js";
import {
  PaginationHelper,
  type PaginatedResult,
  type PaginationParams,
} from "./utils/pagination.js";
import type {
  Ad,
  AdAccount,
  AdCreative,
  AdInsights,
  AdSet,
  BatchRequest,
  BatchResponse,
  Campaign,
  CustomAudience,
  MetaApiResponse,
} from "./types/meta-api.js";

export class MetaApiClient {
  private auth: AuthManager;
  private requestTimeoutMs: number;
  private debugEnabled: boolean;

  constructor(
    auth?: AuthManager,
    options: { requestTimeoutMs?: number; debug?: boolean } = {},
  ) {
    this.auth = auth || AuthManager.fromEnvironment();
    const envTimeoutMs = Number(process.env.META_MCP_REQUEST_TIMEOUT_MS);
    const optionTimeoutMs =
      typeof options.requestTimeoutMs === "number" && Number.isFinite(options.requestTimeoutMs)
        ? options.requestTimeoutMs
        : undefined;
    this.requestTimeoutMs = optionTimeoutMs ?? (Number.isFinite(envTimeoutMs) ? envTimeoutMs : 30000);
    this.debugEnabled =
      typeof options.debug === "boolean"
        ? options.debug
        : process.env.META_MCP_DEBUG === "1" || (process.env.DEBUG?.includes("meta-mcp") ?? false);
  }

  get authManager(): AuthManager {
    return this.auth;
  }

  private debug(...args: unknown[]): void {
    if (this.debugEnabled) console.log(...args);
  }

  private normalizeStatusFilter(status?: string | string[]): string | undefined {
    if (!status) return undefined;
    return JSON.stringify(Array.isArray(status) ? status : [status]);
  }

  private appendQueryParams(url: string, params: Record<string, string>): string {
    const separator = url.includes("?") ? "&" : "?";
    return `${url}${separator}${new URLSearchParams(params).toString()}`;
  }

  private async makeRequest<T = any>(
    endpoint: string,
    method: "GET" | "POST" | "DELETE" = "GET",
    body?: any,
    accountId?: string,
    isWriteCall: boolean = false,
  ): Promise<T> {
    let url = `${this.auth.getBaseUrl()}/${this.auth.getApiVersion()}/${endpoint}`;
    const appSecretProof = this.auth.getAppSecretProof();
    if (appSecretProof) {
      url = this.appendQueryParams(url, { appsecret_proof: appSecretProof });
    }

    if (accountId) {
      await globalRateLimiter.checkRateLimit(accountId, isWriteCall);
    }

    return retryWithBackoff(async () => {
      const headers = this.auth.getAuthHeaders();

      const requestOptions: any = { method, headers };

      if (body && method !== "GET") {
        if (typeof body === "string") {
          requestOptions.body = body;
          headers["Content-Type"] = "application/x-www-form-urlencoded";
        } else {
          requestOptions.body = JSON.stringify(body);
          headers["Content-Type"] = "application/json";
        }
      }

      const controller = this.requestTimeoutMs > 0 ? new AbortController() : undefined;
      let timeoutId: ReturnType<typeof setTimeout> | undefined;

      if (controller) {
        requestOptions.signal = controller.signal;
        timeoutId = setTimeout(() => controller.abort(), this.requestTimeoutMs);
      }

      try {
        this.debug("MetaApiClient request", { method, url });
        const response = await fetch(url, requestOptions);
        return MetaApiErrorHandler.handleResponse<T>(response as any);
      } catch (error) {
        if (error instanceof Error && error.name === "AbortError") {
          error.message = `Request timed out after ${this.requestTimeoutMs}ms: ${method} ${endpoint}`;
        }
        throw error;
      } finally {
        if (timeoutId) clearTimeout(timeoutId);
      }
    }, `${method} ${endpoint}`);
  }

  private buildQueryString(params: Record<string, any>): string {
    const urlParams = new URLSearchParams();

    for (const [key, value] of Object.entries(params)) {
      if (value !== undefined && value !== null) {
        if (Array.isArray(value) || typeof value === "object") {
          urlParams.set(key, JSON.stringify(value));
        } else {
          urlParams.set(key, String(value));
        }
      }
    }

    return urlParams.toString();
  }

  // Account Methods
  async getAdAccounts(): Promise<AdAccount[]> {
    const allAccounts: AdAccount[] = [];
    let nextUrl: string | undefined =
      "me/adaccounts?fields=id,name,account_status,balance,currency,timezone_name,business&limit=100";

    while (nextUrl) {
      const response: MetaApiResponse<AdAccount> = await this.makeRequest(nextUrl);
      allAccounts.push(...response.data);

      if (response.paging?.next) {
        const nextPageUrl = new URL(response.paging.next);
        nextUrl = nextPageUrl.pathname.substring(1) + nextPageUrl.search;
      } else {
        nextUrl = undefined;
      }
    }

    return allAccounts;
  }

  // Campaign Methods
  async getCampaigns(
    accountId: string,
    params: PaginationParams & { status?: string | string[]; fields?: string[] } = {},
  ): Promise<PaginatedResult<Campaign>> {
    const formattedAccountId = this.auth.getAccountId(accountId);
    const { status, fields, ...paginationParams } = params;

    const queryParams: Record<string, any> = {
      fields:
        fields?.join(",") ||
        "id,name,objective,status,effective_status,created_time,updated_time,start_time,stop_time,budget_remaining,daily_budget,lifetime_budget",
      ...paginationParams,
    };

    const statusFilter = this.normalizeStatusFilter(status);
    if (statusFilter) queryParams.effective_status = statusFilter;

    const query = this.buildQueryString(queryParams);
    const response = await this.makeRequest<MetaApiResponse<Campaign>>(
      `${formattedAccountId}/campaigns?${query}`,
      "GET",
      null,
      formattedAccountId,
    );

    return PaginationHelper.parsePaginatedResponse(response);
  }

  async getCampaign(campaignId: string): Promise<Campaign> {
    return this.makeRequest(
      `${campaignId}?fields=id,name,objective,status,effective_status,created_time,updated_time,start_time,stop_time,budget_remaining,daily_budget,lifetime_budget,account_id`,
    );
  }

  async createCampaign(
    accountId: string,
    campaignData: {
      name: string;
      objective: string;
      status?: string;
      daily_budget?: number;
      lifetime_budget?: number;
      start_time?: string;
      stop_time?: string;
      special_ad_categories?: string[];
      bid_strategy?: string;
      bid_cap?: number;
      is_budget_optimization_enabled?: boolean;
    },
  ): Promise<{ id: string }> {
    const formattedAccountId = this.auth.getAccountId(accountId);
    const body = this.buildQueryString(campaignData);

    return this.makeRequest(
      `${formattedAccountId}/campaigns`,
      "POST",
      body,
      formattedAccountId,
      true,
    );
  }

  async updateCampaign(
    campaignId: string,
    updates: {
      name?: string;
      status?: string;
      daily_budget?: number;
      lifetime_budget?: number;
      start_time?: string;
      stop_time?: string;
    },
  ): Promise<{ success: boolean }> {
    const body = this.buildQueryString(updates);
    return this.makeRequest(campaignId, "POST", body, undefined, true);
  }

  async deleteCampaign(campaignId: string): Promise<{ success: boolean }> {
    return this.makeRequest(campaignId, "DELETE", null, undefined, true);
  }

  // Ad Set Methods
  async getAdSets(
    params: PaginationParams & {
      campaignId?: string;
      accountId?: string;
      status?: string | string[];
      fields?: string[];
    } = {},
  ): Promise<PaginatedResult<AdSet>> {
    const { campaignId, accountId, status, fields, ...paginationParams } = params;

    let endpoint: string;
    let rateLimitAccountId: string | undefined;

    if (campaignId) {
      endpoint = `${campaignId}/adsets`;
    } else if (accountId) {
      const formattedAccountId = this.auth.getAccountId(accountId);
      endpoint = `${formattedAccountId}/adsets`;
      rateLimitAccountId = formattedAccountId;
    } else {
      throw new Error("Either campaignId or accountId must be provided");
    }

    const queryParams: Record<string, any> = {
      fields:
        fields?.join(",") ||
        "id,name,campaign_id,status,effective_status,created_time,updated_time,start_time,end_time,daily_budget,lifetime_budget,bid_amount,billing_event,optimization_goal,targeting",
      ...paginationParams,
    };

    const statusFilter = this.normalizeStatusFilter(status);
    if (statusFilter) queryParams.effective_status = statusFilter;

    const query = this.buildQueryString(queryParams);
    const response = await this.makeRequest<MetaApiResponse<AdSet>>(
      `${endpoint}?${query}`,
      "GET",
      null,
      rateLimitAccountId,
    );
    return PaginationHelper.parsePaginatedResponse(response);
  }

  async createAdSet(
    accountId: string,
    adSetData: Record<string, any>,
  ): Promise<{ id: string }> {
    const formattedAccountId = this.auth.getAccountId(accountId);
    const body = this.buildQueryString(adSetData);
    return this.makeRequest(`${formattedAccountId}/adsets`, "POST", body, formattedAccountId, true);
  }

  async getAdSet(adSetId: string, fields?: string[]): Promise<AdSet> {
    return this.makeRequest(
      `${adSetId}?fields=${
        fields?.join(",") ||
        "id,name,campaign_id,status,effective_status,created_time,updated_time,start_time,end_time,daily_budget,lifetime_budget,bid_amount,billing_event,optimization_goal,targeting,promoted_object"
      }`,
    );
  }

  async updateAdSet(adSetId: string, updates: Record<string, any>): Promise<{ success: boolean }> {
    const body = this.buildQueryString(updates);
    return this.makeRequest(adSetId, "POST", body, undefined, true);
  }

  // Ad Methods
  async getAds(
    params: PaginationParams & {
      adsetId?: string;
      campaignId?: string;
      accountId?: string;
      status?: string | string[];
      fields?: string[];
    } = {},
  ): Promise<PaginatedResult<Ad>> {
    const { adsetId, campaignId, accountId, status, fields, ...paginationParams } = params;

    let endpoint: string;
    let rateLimitAccountId: string | undefined;

    if (adsetId) {
      endpoint = `${adsetId}/ads`;
    } else if (campaignId) {
      endpoint = `${campaignId}/ads`;
    } else if (accountId) {
      const formattedAccountId = this.auth.getAccountId(accountId);
      endpoint = `${formattedAccountId}/ads`;
      rateLimitAccountId = formattedAccountId;
    } else {
      throw new Error("Provide one of adsetId, campaignId, or accountId");
    }

    const queryParams: Record<string, any> = {
      fields:
        fields?.join(",") ||
        "id,name,adset_id,campaign_id,status,effective_status,created_time,updated_time,creative",
      ...paginationParams,
    };

    const statusFilter = this.normalizeStatusFilter(status);
    if (statusFilter) queryParams.effective_status = statusFilter;

    const query = this.buildQueryString(queryParams);
    const response = await this.makeRequest<MetaApiResponse<Ad>>(
      `${endpoint}?${query}`,
      "GET",
      null,
      rateLimitAccountId,
    );
    return PaginationHelper.parsePaginatedResponse(response);
  }

  async createAd(accountId: string, adData: Record<string, any>): Promise<{ id: string }> {
    const formattedAccountId = this.auth.getAccountId(accountId);
    const body = this.buildQueryString(adData);
    return this.makeRequest(`${formattedAccountId}/ads`, "POST", body, formattedAccountId, true);
  }

  async getAd(adId: string, fields?: string[]): Promise<Ad> {
    return this.makeRequest(
      `${adId}?fields=${
        fields?.join(",") ||
        "id,name,adset_id,campaign_id,status,effective_status,created_time,updated_time,creative{id,name,title,body,object_story_spec,asset_feed_spec}"
      }`,
    );
  }

  async updateAd(adId: string, updates: Record<string, any>): Promise<{ success: boolean }> {
    const body = this.buildQueryString(updates);
    return this.makeRequest(adId, "POST", body, undefined, true);
  }

  // Insights
  async getInsights(objectId: string, params: Record<string, any>): Promise<PaginatedResult<AdInsights>> {
    const query = this.buildQueryString(params);
    const response = await this.makeRequest<MetaApiResponse<AdInsights>>(
      `${objectId}/insights?${query}`,
      "GET",
      null,
      undefined,
      false,
    );
    return PaginationHelper.parsePaginatedResponse(response);
  }

  // Audiences
  async getCustomAudiences(
    accountId: string,
    params: PaginationParams & { fields?: string[] } = {},
  ): Promise<PaginatedResult<CustomAudience>> {
    const formattedAccountId = this.auth.getAccountId(accountId);
    const { fields, ...paginationParams } = params;
    const queryParams: Record<string, any> = {
      fields:
        fields?.join(",") ||
        "id,name,description,subtype,approximate_count_lower_bound,approximate_count_upper_bound,data_source,retention_days,creation_time,operation_status",
      ...paginationParams,
    };
    const query = this.buildQueryString(queryParams);
    const response = await this.makeRequest<MetaApiResponse<CustomAudience>>(
      `${formattedAccountId}/customaudiences?${query}`,
      "GET",
      null,
      formattedAccountId,
    );
    return PaginationHelper.parsePaginatedResponse(response);
  }

  async createCustomAudience(accountId: string, audienceData: Record<string, any>): Promise<{ id: string }> {
    const formattedAccountId = this.auth.getAccountId(accountId);
    const body = this.buildQueryString(audienceData);
    return this.makeRequest(`${formattedAccountId}/customaudiences`, "POST", body, formattedAccountId, true);
  }

  async createLookalikeAudience(accountId: string, audienceData: Record<string, any>): Promise<{ id: string }> {
    const formattedAccountId = this.auth.getAccountId(accountId);
    const body = this.buildQueryString(audienceData);
    return this.makeRequest(`${formattedAccountId}/customaudiences`, "POST", body, formattedAccountId, true);
  }

  async estimateAudienceSize(accountId: string, targeting: any, optimizationGoal?: string): Promise<any> {
    const formattedAccountId = this.auth.getAccountId(accountId);
    const body = this.buildQueryString({
      targeting_spec: targeting,
      ...(optimizationGoal ? { optimization_goal: optimizationGoal } : {}),
    });
    return this.makeRequest(`${formattedAccountId}/delivery_estimate`, "POST", body, formattedAccountId, true);
  }

  // Creatives
  async listAdCreatives(
    accountId: string,
    params: PaginationParams & { fields?: string[] } = {},
  ): Promise<PaginatedResult<AdCreative>> {
    const formattedAccountId = this.auth.getAccountId(accountId);
    const { fields, ...paginationParams } = params;
    const queryParams: Record<string, any> = {
      fields: fields?.join(",") || "id,name,title,body,image_url,object_story_spec,url_tags,call_to_action_type",
      ...paginationParams,
    };
    const query = this.buildQueryString(queryParams);
    const response = await this.makeRequest<MetaApiResponse<AdCreative>>(
      `${formattedAccountId}/adcreatives?${query}`,
      "GET",
      null,
      formattedAccountId,
    );
    return PaginationHelper.parsePaginatedResponse(response);
  }

  async createAdCreative(accountId: string, creativeData: Record<string, any>): Promise<{ id: string }> {
    const formattedAccountId = this.auth.getAccountId(accountId);
    const body = this.buildQueryString(creativeData);
    return this.makeRequest(`${formattedAccountId}/adcreatives`, "POST", body, formattedAccountId, true);
  }

  // Batch
  async batchRequest(accountId: string, requests: BatchRequest[]): Promise<BatchResponse[]> {
    const formattedAccountId = this.auth.getAccountId(accountId);
    const body = this.buildQueryString({ batch: requests });
    return this.makeRequest(`${formattedAccountId}`, "POST", body, formattedAccountId, true);
  }
}

