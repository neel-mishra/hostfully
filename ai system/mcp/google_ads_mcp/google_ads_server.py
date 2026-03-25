from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from mcp.server.fastmcp import FastMCP
from pydantic import Field

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("google_ads_mcp")

if load_dotenv:
    load_dotenv()
    load_dotenv(Path(__file__).with_name(".env"))


SCOPES = ["https://www.googleapis.com/auth/adwords"]
API_VERSION = os.environ.get("GOOGLE_ADS_API_VERSION", "v23")
BASE_URL = f"https://googleads.googleapis.com/{API_VERSION}"
DEFAULT_TIMEOUT_SECONDS = int(os.environ.get("GOOGLE_ADS_TIMEOUT_SECONDS", "60"))


mcp = FastMCP(
    "google-ads-mcp",
    dependencies=[
        "mcp[cli]",
        "requests",
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "python-dotenv",
    ],
)


def env(name: str, default: str = "") -> str:
    return os.environ.get(name, default)


def format_customer_id(customer_id: Any) -> str:
    cleaned = "".join(ch for ch in str(customer_id or "") if ch.isdigit())
    return cleaned.zfill(10)


def _maybe_login_customer_id() -> str:
    return format_customer_id(env("GOOGLE_ADS_LOGIN_CUSTOMER_ID")) if env("GOOGLE_ADS_LOGIN_CUSTOMER_ID") else ""


def parse_list(value: str) -> List[str]:
    if not value:
        return []
    normalized = value.replace("\n", ",")
    return [item.strip() for item in normalized.split(",") if item.strip()]


def build_date_condition(days: int, field: str = "segments.date") -> str:
    if days <= 0:
        raise ValueError("days must be greater than 0")
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=days - 1)
    return f"{field} BETWEEN '{start_date.isoformat()}' AND '{end_date.isoformat()}'"


def to_geo_targets(values: str) -> List[str]:
    geo_targets = []
    for item in parse_list(values):
        if item.startswith("geoTargetConstants/"):
            geo_targets.append(item)
        else:
            geo_targets.append(f"geoTargetConstants/{item}")
    return geo_targets


def to_language_resource(value: str) -> str:
    if not value:
        return "languageConstants/1000"
    if value.startswith("languageConstants/"):
        return value
    return f"languageConstants/{value}"


def get_credentials():
    auth_type = env("GOOGLE_ADS_AUTH_TYPE", "service_account").lower()
    if auth_type == "service_account":
        return get_service_account_credentials()
    return get_oauth_credentials()


def get_service_account_credentials():
    credentials_path = env("GOOGLE_ADS_CREDENTIALS_PATH")
    if not credentials_path:
        raise ValueError("GOOGLE_ADS_CREDENTIALS_PATH is required for service_account auth")
    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Service account credentials not found: {credentials_path}")

    creds = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=SCOPES,
    )
    impersonation_email = env("GOOGLE_ADS_IMPERSONATION_EMAIL")
    if impersonation_email:
        creds = creds.with_subject(impersonation_email)
    return creds


def get_oauth_credentials():
    credentials_path = env("GOOGLE_ADS_CREDENTIALS_PATH")
    if not credentials_path:
        raise ValueError("GOOGLE_ADS_CREDENTIALS_PATH is required for oauth auth")

    token_path = Path(credentials_path)
    creds: Optional[Credentials] = None
    client_config: Optional[Dict[str, Any]] = None

    if token_path.exists():
        data = json.loads(token_path.read_text())
        if "installed" in data or "web" in data:
            client_config = data
        else:
            creds = Credentials.from_authorized_user_info(data, SCOPES)

    if creds and creds.expired and creds.refresh_token:
        try:
            creds.refresh(Request())
        except RefreshError:
            creds = None

    if not creds or not creds.valid:
        if not client_config:
            client_id = env("GOOGLE_ADS_CLIENT_ID")
            client_secret = env("GOOGLE_ADS_CLIENT_SECRET")
            if not client_id or not client_secret:
                raise ValueError(
                    "GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET are required when "
                    "no OAuth client config JSON is present"
                )
            client_config = {
                "installed": {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": ["http://localhost"],
                }
            }

        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json())

    return creds


def get_headers(creds) -> Dict[str, str]:
    developer_token = env("GOOGLE_ADS_DEVELOPER_TOKEN")
    if not developer_token:
        raise ValueError("GOOGLE_ADS_DEVELOPER_TOKEN is not set")

    if isinstance(creds, service_account.Credentials):
        creds.refresh(Request())
    elif not creds.valid:
        if creds.expired and getattr(creds, "refresh_token", None):
            creds.refresh(Request())
        else:
            raise ValueError("OAuth credentials are invalid and cannot be refreshed")

    headers = {
        "Authorization": f"Bearer {creds.token}",
        "developer-token": developer_token,
        "content-type": "application/json",
    }

    login_customer_id = _maybe_login_customer_id()
    if login_customer_id:
        headers["login-customer-id"] = login_customer_id

    return headers


def rest_get(path: str) -> Dict[str, Any]:
    creds = get_credentials()
    response = requests.get(
        f"{BASE_URL}/{path}",
        headers=get_headers(creds),
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def rest_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    creds = get_credentials()
    response = requests.post(
        f"{BASE_URL}/{path}",
        headers=get_headers(creds),
        json=payload,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    return response.json()


def rest_post_allow_non_json(path: str, payload: Dict[str, Any]) -> Any:
    creds = get_credentials()
    response = requests.post(
        f"{BASE_URL}/{path}",
        headers=get_headers(creds),
        json=payload,
        timeout=DEFAULT_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    content_type = response.headers.get("content-type", "")
    if "application/json" in content_type:
        return response.json()
    return response.text


def search(customer_id: str, query: str) -> Dict[str, Any]:
    return rest_post(
        f"customers/{format_customer_id(customer_id)}/googleAds:search",
        {"query": query},
    )


def search_stream(customer_id: str, query: str) -> List[Dict[str, Any]]:
    data = rest_post_allow_non_json(
        f"customers/{format_customer_id(customer_id)}/googleAds:searchStream",
        {"query": query},
    )
    if isinstance(data, str):
        return json.loads(data)
    if isinstance(data, list):
        return data
    return [data]


def flatten_record(value: Any, prefix: str = "") -> Dict[str, str]:
    flattened: Dict[str, str] = {}
    if isinstance(value, dict):
        for key, child in value.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            flattened.update(flatten_record(child, new_prefix))
    elif isinstance(value, list):
        if all(isinstance(item, dict) and "text" in item for item in value):
            flattened[prefix] = " | ".join(str(item.get("text", "")) for item in value)
        else:
            flattened[prefix] = json.dumps(value, ensure_ascii=True)
    else:
        flattened[prefix] = "" if value is None else str(value)
    return flattened


def format_table(results: List[Dict[str, Any]], title: str) -> str:
    if not results:
        return f"{title}\nNo rows returned."

    rows = [flatten_record(result) for result in results]
    columns: List[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                columns.append(key)
                seen.add(key)

    widths = {column: len(column) for column in columns}
    for row in rows:
        for column in columns:
            widths[column] = max(widths[column], len(row.get(column, "")))

    header = " | ".join(f"{column:{widths[column]}}" for column in columns)
    lines = [title, "-" * len(header), header, "-" * len(header)]

    for row in rows:
        lines.append(" | ".join(f"{row.get(column, ''):{widths[column]}}" for column in columns))
    return "\n".join(lines)


def format_json(data: Dict[str, Any], title: str) -> str:
    return f"{title}\n{json.dumps(data, indent=2)}"


def format_csv(results: List[Dict[str, Any]], title: str) -> str:
    if not results:
        return f"{title}\n"
    rows = [flatten_record(result) for result in results]
    columns: List[str] = []
    seen = set()
    for row in rows:
        for key in row:
            if key not in seen:
                columns.append(key)
                seen.add(key)
    csv_lines = [",".join(columns)]
    for row in rows:
        csv_lines.append(",".join(row.get(column, "").replace(",", ";") for column in columns))
    return f"{title}\n" + "\n".join(csv_lines)


def render_search_results(data: Dict[str, Any], title: str, output_format: str = "table") -> str:
    results = data.get("results", [])
    if output_format == "json":
        return format_json(data, title)
    if output_format == "csv":
        return format_csv(results, title)
    return format_table(results, title)


def execute_query(customer_id: str, query: str, output_format: str = "table") -> str:
    data = search(customer_id, query)
    return render_search_results(
        data,
        f"Query results for account {format_customer_id(customer_id)}",
        output_format,
    )


def query_error(prefix: str, error: Exception) -> str:
    if isinstance(error, requests.HTTPError) and error.response is not None:
        try:
            payload = error.response.json()
            details = payload.get("error", {}).get("details", [])
            if details and isinstance(details, list):
                google_ads_failure = details[0]
                errors = google_ads_failure.get("errors", [])
                for e in errors:
                    code = e.get("errorCode", {}).get("authorizationError")
                    msg = e.get("message", "")
                    if code == "METRIC_ACCESS_DENIED" and "auction_insight_" in msg:
                        return (
                            f"{prefix}: METRIC_ACCESS_DENIED for Auction Insights metrics.\n\n"
                            "Google does not grant API access to these Auction Insights metrics for every developer token. "
                            "This is an API permission/eligibility restriction, not a bug in the MCP.\n\n"
                            "Workarounds:\n"
                            "- Use Search Impression Share metrics (supported broadly):\n"
                            "  metrics.search_impression_share, metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share\n"
                            "- Or view Auction Insights directly in the Google Ads UI.\n\n"
                            "If you need API access, you typically must request it via Google Ads API support (they decide per account/token)."
                        )
        except Exception:
            pass
        return f"{prefix}: HTTP {error.response.status_code} - {error.response.text}"
    return f"{prefix}: {error}"


@mcp.tool()
async def list_accounts() -> str:
    try:
        data = rest_get("customers:listAccessibleCustomers")
        resource_names = data.get("resourceNames", [])
        if not resource_names:
            return "No accessible Google Ads accounts found."
        lines = ["Accessible Google Ads accounts:"]
        for resource_name in resource_names:
            lines.append(f"- {format_customer_id(resource_name.split('/')[-1])}")
        return "\n".join(lines)
    except Exception as error:
        return query_error("Error listing accounts", error)


@mcp.tool()
async def get_account_currency(
    customer_id: str = Field(description="Google Ads customer ID"),
) -> str:
    query = """
    SELECT
      customer.id,
      customer.currency_code,
      customer.time_zone,
      customer.descriptive_name
    FROM customer
    LIMIT 1
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting account currency", error)


@mcp.tool()
async def execute_gaql_query(
    customer_id: str = Field(description="Google Ads customer ID"),
    query: str = Field(description="Valid GAQL query"),
) -> str:
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error executing GAQL query", error)


@mcp.tool()
async def run_gaql(
    customer_id: str = Field(description="Google Ads customer ID"),
    query: str = Field(description="Valid GAQL query"),
    format: str = Field(default="table", description="table, json, or csv"),
) -> str:
    try:
        return execute_query(customer_id, query, format.lower())
    except Exception as error:
        return query_error("Error running GAQL", error)


@mcp.tool()
async def list_resources(
    customer_id: str = Field(description="Google Ads customer ID"),
) -> str:
    query = """
    SELECT
      google_ads_field.name,
      google_ads_field.category,
      google_ads_field.data_type
    FROM google_ads_field
    WHERE google_ads_field.category = 'RESOURCE'
    ORDER BY google_ads_field.name
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error listing resources", error)


@mcp.tool()
async def list_fields(
    customer_id: str = Field(description="Google Ads customer ID"),
    resource_name: str = Field(description="Resource to inspect, for example keyword_view"),
    category_filter: str = Field(
        default="",
        description="Optional google_ads_field.category filter like ATTRIBUTE, SEGMENT, METRIC, or RESOURCE",
    ),
) -> str:
    where_parts = [f"google_ads_field.selectable = true", f"google_ads_field.name LIKE '{resource_name}.%'"]
    if category_filter:
        where_parts.append(f"google_ads_field.category = '{category_filter.upper()}'")
    query = f"""
    SELECT
      google_ads_field.name,
      google_ads_field.category,
      google_ads_field.data_type,
      google_ads_field.filterable,
      google_ads_field.sortable
    FROM google_ads_field
    WHERE {' AND '.join(where_parts)}
    ORDER BY google_ads_field.category, google_ads_field.name
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error listing fields", error)


def build_report_query_text(
    resource_name: str,
    metrics: str,
    segments: str = "",
    attributes: str = "",
    where_clause: str = "",
    order_by: str = "",
    limit: int = 50,
) -> str:
    select_fields = parse_list(attributes) + parse_list(segments) + parse_list(metrics)
    if not select_fields:
        raise ValueError("At least one metric, segment, or attribute is required")
    query = "SELECT\n  " + ",\n  ".join(select_fields)
    query += f"\nFROM {resource_name}"
    if where_clause:
        query += f"\nWHERE {where_clause}"
    if order_by:
        query += f"\nORDER BY {order_by}"
    query += f"\nLIMIT {limit}"
    return query


@mcp.tool()
async def build_report_query(
    resource_name: str = Field(description="GAQL resource name, for example keyword_view"),
    metrics: str = Field(description="Comma-separated metrics"),
    segments: str = Field(default="", description="Comma-separated segments"),
    attributes: str = Field(default="", description="Comma-separated non-metric fields"),
    where_clause: str = Field(default="", description="Optional GAQL WHERE clause without the word WHERE"),
    order_by: str = Field(default="", description="Optional ORDER BY clause without the words ORDER BY"),
    limit: int = Field(default=50, description="Query row limit"),
) -> str:
    try:
        return build_report_query_text(resource_name, metrics, segments, attributes, where_clause, order_by, limit)
    except Exception as error:
        return query_error("Error building GAQL query", error)


@mcp.tool()
async def get_campaign_performance(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    limit: int = Field(default=50, description="Maximum rows"),
) -> str:
    query = f"""
    SELECT
      campaign.id,
      campaign.name,
      campaign.status,
      campaign.advertising_channel_type,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.average_cpc,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value
    FROM campaign
    WHERE {build_date_condition(days)}
    ORDER BY metrics.cost_micros DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting campaign performance", error)


@mcp.tool()
async def get_ad_performance(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    limit: int = Field(default=50, description="Maximum rows"),
) -> str:
    query = f"""
    SELECT
      ad_group_ad.ad.id,
      ad_group_ad.ad.name,
      ad_group_ad.status,
      campaign.name,
      ad_group.name,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value
    FROM ad_group_ad
    WHERE {build_date_condition(days)}
    ORDER BY metrics.impressions DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting ad performance", error)


@mcp.tool()
async def get_search_term_performance(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    campaign_id: str = Field(default="", description="Optional campaign ID filter"),
    ad_group_id: str = Field(default="", description="Optional ad group ID filter"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    where_parts = [build_date_condition(days)]
    if campaign_id:
        where_parts.append(f"campaign.id = {int(format_customer_id(campaign_id))}")
    if ad_group_id:
        where_parts.append(f"ad_group.id = {int(format_customer_id(ad_group_id))}")
    query = f"""
    SELECT
      campaign.name,
      ad_group.name,
      search_term_view.search_term,
      search_term_view.status,
      segments.keyword.info.match_type,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value
    FROM search_term_view
    WHERE {' AND '.join(where_parts)}
    ORDER BY metrics.cost_micros DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting search term performance", error)


@mcp.tool()
async def get_campaign_search_terms(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    campaign_id: str = Field(default="", description="Optional campaign ID filter"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    where_parts = [build_date_condition(days)]
    if campaign_id:
        where_parts.append(f"campaign.id = {int(format_customer_id(campaign_id))}")
    query = f"""
    SELECT
      campaign.id,
      campaign.name,
      campaign_search_term_view.search_term,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value
    FROM campaign_search_term_view
    WHERE {' AND '.join(where_parts)}
    ORDER BY metrics.cost_micros DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting campaign search terms", error)


@mcp.tool()
async def get_keyword_performance(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    campaign_id: str = Field(default="", description="Optional campaign ID filter"),
    ad_group_id: str = Field(default="", description="Optional ad group ID filter"),
    match_type: str = Field(default="", description="Optional keyword match type filter"),
    status: str = Field(default="", description="Optional criterion status filter"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    where_parts = [build_date_condition(days)]
    if campaign_id:
        where_parts.append(f"campaign.id = {int(format_customer_id(campaign_id))}")
    if ad_group_id:
        where_parts.append(f"ad_group.id = {int(format_customer_id(ad_group_id))}")
    if match_type:
        where_parts.append(f"ad_group_criterion.keyword.match_type = '{match_type.upper()}'")
    if status:
        where_parts.append(f"ad_group_criterion.status = '{status.upper()}'")
    query = f"""
    SELECT
      campaign.name,
      ad_group.name,
      ad_group_criterion.criterion_id,
      ad_group_criterion.keyword.text,
      ad_group_criterion.keyword.match_type,
      ad_group_criterion.status,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.average_cpc,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value
    FROM keyword_view
    WHERE {' AND '.join(where_parts)}
    ORDER BY metrics.cost_micros DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting keyword performance", error)


@mcp.tool()
async def get_search_term_to_keyword_mapping(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    query = f"""
    SELECT
      campaign.name,
      ad_group.name,
      search_term_view.search_term,
      segments.keyword.ad_group_criterion,
      segments.keyword.info.match_type,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions
    FROM search_term_view
    WHERE {build_date_condition(days)}
    ORDER BY metrics.cost_micros DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error mapping search terms to keywords", error)


@mcp.tool()
async def get_auction_insights(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    campaign_id: str = Field(default="", description="Optional campaign ID filter"),
    ad_group_id: str = Field(default="", description="Optional ad group ID filter"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    where_parts = [build_date_condition(days)]
    if campaign_id:
        where_parts.append(f"campaign.id = {int(format_customer_id(campaign_id))}")
    if ad_group_id:
        where_parts.append(f"ad_group.id = {int(format_customer_id(ad_group_id))}")
    query = f"""
    SELECT
      campaign.name,
      ad_group.name,
      segments.auction_insight_domain,
      metrics.auction_insight_search_impression_share,
      metrics.auction_insight_search_overlap_rate,
      metrics.auction_insight_search_outranking_share,
      metrics.auction_insight_search_position_above_rate,
      metrics.auction_insight_search_top_impression_percentage,
      metrics.auction_insight_search_absolute_top_impression_percentage
    FROM keyword_view
    WHERE {' AND '.join(where_parts)}
    ORDER BY metrics.auction_insight_search_impression_share DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting auction insights", error)


@mcp.tool()
async def get_search_impression_share(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    campaign_id: str = Field(default="", description="Optional campaign ID filter"),
    limit: int = Field(default=50, description="Maximum rows"),
) -> str:
    """
    Fallback for Auction Insights when auction_insight_* metrics are not API-enabled.

    Reports your own Search Impression Share and Lost IS (budget/rank), which are
    widely accessible via the API for Search campaigns.
    """
    where_parts = [build_date_condition(days)]
    if campaign_id:
        where_parts.append(f"campaign.id = {int(format_customer_id(campaign_id))}")
    query = f"""
    SELECT
      campaign.id,
      campaign.name,
      campaign.advertising_channel_type,
      metrics.search_impression_share,
      metrics.search_budget_lost_impression_share,
      metrics.search_rank_lost_impression_share,
      metrics.impressions,
      metrics.clicks,
      metrics.cost_micros,
      metrics.conversions
    FROM campaign
    WHERE {' AND '.join(where_parts)}
    ORDER BY metrics.impressions DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting search impression share", error)


@mcp.tool()
async def get_asset_inventory(
    customer_id: str = Field(description="Google Ads customer ID"),
    asset_type: str = Field(default="", description="Optional asset type filter like IMAGE, SITELINK, CALL, LEAD_FORM"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    where_clause = f"WHERE asset.type = '{asset_type.upper()}'" if asset_type else ""
    query = f"""
    SELECT
      asset.id,
      asset.name,
      asset.type,
      asset.resource_name,
      asset.final_urls,
      asset.image_asset.full_size.url,
      asset.text_asset.text,
      asset.youtube_video_asset.youtube_video_id
    FROM asset
    {where_clause}
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting asset inventory", error)


@mcp.tool()
async def get_asset_usage_map(
    customer_id: str = Field(description="Google Ads customer ID"),
    asset_type: str = Field(default="", description="Optional asset type filter"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    where_parts = []
    if asset_type:
        where_parts.append(f"asset.type = '{asset_type.upper()}'")
    query = f"""
    SELECT
      campaign.name,
      campaign_asset.field_type,
      asset.id,
      asset.name,
      asset.type,
      asset.resource_name
    FROM campaign_asset
    {'WHERE ' + ' AND '.join(where_parts) if where_parts else ''}
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting asset usage map", error)


@mcp.tool()
async def get_rsa_asset_performance(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    query = f"""
    SELECT
      campaign.name,
      ad_group.name,
      ad_group_ad.ad.id,
      ad_group_ad_asset_view.field_type,
      ad_group_ad_asset_view.performance_label,
      asset.id,
      asset.name,
      asset.text_asset.text,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.conversions
    FROM ad_group_ad_asset_view
    WHERE {build_date_condition(days)}
    ORDER BY metrics.impressions DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting RSA asset performance", error)


@mcp.tool()
async def get_rsa_combination_performance(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    query = f"""
    SELECT
      campaign.name,
      ad_group.name,
      ad_group_ad_asset_combination_view.resource_name,
      ad_group_ad_asset_combination_view.served_assets,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.conversions
    FROM ad_group_ad_asset_combination_view
    WHERE {build_date_condition(days)}
    ORDER BY metrics.impressions DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting RSA combination performance", error)


@mcp.tool()
async def get_sitelink_performance(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    query = f"""
    SELECT
      campaign.name,
      campaign_asset.field_type,
      asset.id,
      asset.name,
      asset.sitelink_asset.link_text,
      asset.sitelink_asset.final_urls,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.conversions
    FROM campaign_asset
    WHERE campaign_asset.field_type = 'SITELINK' AND {build_date_condition(days)}
    ORDER BY metrics.impressions DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting sitelink performance", error)


@mcp.tool()
async def get_lead_form_asset_performance(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    query = f"""
    SELECT
      campaign.name,
      campaign_asset.field_type,
      asset.id,
      asset.name,
      asset.lead_form_asset.call_to_action_type,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.conversions
    FROM campaign_asset
    WHERE campaign_asset.field_type = 'LEAD_FORM' AND {build_date_condition(days)}
    ORDER BY metrics.impressions DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting lead form asset performance", error)


@mcp.tool()
async def get_lead_form_submissions(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    query = f"""
    SELECT
      lead_form_submission_data.asset,
      lead_form_submission_data.campaign,
      lead_form_submission_data.ad_group,
      lead_form_submission_data.ad_group_ad,
      lead_form_submission_data.submission_date_time,
      lead_form_submission_data.gclid
    FROM lead_form_submission_data
    WHERE lead_form_submission_data.submission_date_time >= '{(datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%SZ")}'
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting lead form submissions", error)


@mcp.tool()
async def get_campaign_diagnostics(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
) -> str:
    query = f"""
    SELECT
      campaign.name,
      campaign.status,
      campaign.advertising_channel_type,
      campaign.bidding_strategy_type,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.average_cpc,
      metrics.cost_micros,
      metrics.conversions,
      metrics.conversions_value,
      metrics.search_impression_share,
      metrics.search_budget_lost_impression_share,
      metrics.search_rank_lost_impression_share
    FROM campaign
    WHERE {build_date_condition(days)}
    ORDER BY metrics.cost_micros DESC
    LIMIT 100
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting campaign diagnostics", error)


@mcp.tool()
async def get_device_breakdown(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    level: str = Field(default="campaign", description="campaign or ad_group"),
) -> str:
    resource = "campaign" if level == "campaign" else "ad_group"
    name_field = "campaign.name" if level == "campaign" else "ad_group.name"
    query = f"""
    SELECT
      {name_field},
      segments.device,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.average_cpc,
      metrics.cost_micros,
      metrics.conversions
    FROM {resource}
    WHERE {build_date_condition(days)}
    ORDER BY metrics.impressions DESC
    LIMIT 200
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting device breakdown", error)


@mcp.tool()
async def get_time_breakdown(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    granularity: str = Field(default="date", description="date, week, month, quarter, or year"),
) -> str:
    segment_map = {
        "date": "segments.date",
        "week": "segments.week",
        "month": "segments.month",
        "quarter": "segments.quarter",
        "year": "segments.year",
    }
    segment = segment_map.get(granularity.lower())
    if not segment:
        return "granularity must be one of: date, week, month, quarter, year"
    query = f"""
    SELECT
      campaign.name,
      {segment},
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.cost_micros,
      metrics.conversions
    FROM campaign
    WHERE {build_date_condition(days)}
    ORDER BY {segment}
    LIMIT 500
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting time breakdown", error)


@mcp.tool()
async def get_landing_page_performance(
    customer_id: str = Field(description="Google Ads customer ID"),
    days: int = Field(default=30, description="Lookback window in days"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    query = f"""
    SELECT
      landing_page_view.unexpanded_final_url,
      campaign.name,
      metrics.impressions,
      metrics.clicks,
      metrics.ctr,
      metrics.average_cpc,
      metrics.cost_micros,
      metrics.conversions
    FROM landing_page_view
    WHERE {build_date_condition(days)}
    ORDER BY metrics.clicks DESC
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error getting landing page performance", error)


@mcp.tool()
async def generate_keyword_ideas(
    customer_id: str = Field(description="Google Ads customer ID"),
    seed_keywords: str = Field(default="", description="Comma-separated keywords"),
    url: str = Field(default="", description="Optional landing page or site URL"),
    geo_targets: str = Field(default="2840", description="Comma-separated geo target IDs, defaults to US"),
    language: str = Field(default="1000", description="Language constant ID, defaults to English"),
    include_adult_keywords: bool = Field(default=False, description="Include adult keywords"),
    page_size: int = Field(default=25, description="Maximum ideas to return"),
) -> str:
    keywords = parse_list(seed_keywords)
    if not keywords and not url:
        return "Provide at least one seed keyword or a URL."

    payload: Dict[str, Any] = {
        "geoTargetConstants": to_geo_targets(geo_targets),
        "language": to_language_resource(language),
        "keywordPlanNetwork": "GOOGLE_SEARCH_AND_PARTNERS",
        "includeAdultKeywords": include_adult_keywords,
        "pageSize": page_size,
    }
    if keywords and url:
        payload["keywordAndUrlSeed"] = {"keywords": keywords, "url": url}
    elif keywords:
        payload["keywordSeed"] = {"keywords": keywords}
    else:
        payload["urlSeed"] = {"url": url}

    try:
        data = rest_post(f"customers/{format_customer_id(customer_id)}:generateKeywordIdeas", payload)
        return format_json(data, "Keyword ideas")
    except Exception as error:
        return query_error("Error generating keyword ideas", error)


@mcp.tool()
async def generate_keyword_historical_metrics(
    customer_id: str = Field(description="Google Ads customer ID"),
    keywords: str = Field(description="Comma-separated keywords"),
    geo_targets: str = Field(default="2840", description="Comma-separated geo target IDs, defaults to US"),
    language: str = Field(default="1000", description="Language constant ID, defaults to English"),
    network: str = Field(default="GOOGLE_SEARCH_AND_PARTNERS", description="Keyword plan network enum value"),
) -> str:
    keyword_list = parse_list(keywords)
    if not keyword_list:
        return "Provide at least one keyword."

    payload = {
        "keywords": keyword_list,
        "geoTargetConstants": to_geo_targets(geo_targets),
        "language": to_language_resource(language),
        "keywordPlanNetwork": network,
    }

    try:
        data = rest_post(f"customers/{format_customer_id(customer_id)}:generateKeywordHistoricalMetrics", payload)
        return format_json(data, "Keyword historical metrics")
    except Exception as error:
        return query_error("Error generating keyword historical metrics", error)


@mcp.tool()
async def generate_ad_group_themes(
    customer_id: str = Field(description="Google Ads customer ID"),
    keywords: str = Field(description="Comma-separated keywords"),
    url: str = Field(default="", description="Optional landing page URL"),
) -> str:
    keyword_list = parse_list(keywords)
    if not keyword_list:
        return "Provide at least one keyword."

    payload: Dict[str, Any] = {"keywords": keyword_list}
    if url:
        payload["url"] = url

    try:
        data = rest_post(f"customers/{format_customer_id(customer_id)}:generateAdGroupThemes", payload)
        return format_json(data, "Ad group themes")
    except Exception as error:
        return query_error("Error generating ad group themes", error)


@mcp.tool()
async def generate_keyword_forecast_metrics(
    customer_id: str = Field(description="Google Ads customer ID"),
    campaign_payload_json: str = Field(
        description="JSON string matching the REST CampaignToForecast payload for generateKeywordForecastMetrics",
    ),
) -> str:
    try:
        payload = {"campaign": json.loads(campaign_payload_json)}
    except json.JSONDecodeError as error:
        return f"Invalid JSON for campaign_payload_json: {error}"

    try:
        data = rest_post(f"customers/{format_customer_id(customer_id)}:generateKeywordForecastMetrics", payload)
        return format_json(data, "Keyword forecast metrics")
    except Exception as error:
        return query_error("Error generating keyword forecast metrics", error)


@mcp.tool()
async def list_keyword_plans(
    customer_id: str = Field(description="Google Ads customer ID"),
    limit: int = Field(default=100, description="Maximum rows"),
) -> str:
    query = f"""
    SELECT
      keyword_plan.id,
      keyword_plan.name,
      keyword_plan.forecast_period.date_interval,
      keyword_plan.resource_name
    FROM keyword_plan
    LIMIT {limit}
    """
    try:
        return execute_query(customer_id, query, "table")
    except Exception as error:
        return query_error("Error listing keyword plans", error)


@mcp.tool()
async def healthcheck() -> str:
    required = [
        "GOOGLE_ADS_AUTH_TYPE",
        "GOOGLE_ADS_CREDENTIALS_PATH",
        "GOOGLE_ADS_DEVELOPER_TOKEN",
    ]
    missing = [name for name in required if not env(name)]
    auth_type = env("GOOGLE_ADS_AUTH_TYPE", "service_account")
    lines = [f"Auth type: {auth_type}", f"API version: {API_VERSION}"]
    if missing:
        lines.append("Missing env vars: " + ", ".join(missing))
    else:
        lines.append("Required env vars are present.")
    login_customer_id = _maybe_login_customer_id()
    if login_customer_id:
        lines.append(f"Login customer ID: {login_customer_id}")
    if env("GOOGLE_ADS_IMPERSONATION_EMAIL"):
        lines.append("Impersonation email is set.")
    return "\n".join(lines)


@mcp.tool()
async def diagnostics() -> str:
    lines = [await healthcheck(), ""]

    try:
        creds = get_credentials()
        headers = get_headers(creds)
        safe_headers = {k: v for k, v in headers.items() if k.lower() != "authorization"}
        lines.append("Headers OK (Authorization omitted).")
        lines.append(f"Headers: {json.dumps(safe_headers, indent=2)}")
    except Exception as error:
        lines.append(query_error("Auth/header error", error))
        return "\n".join(lines)

    try:
        rest_get("customers:listAccessibleCustomers")
        lines.append("customers:listAccessibleCustomers OK")
    except Exception as error:
        lines.append(query_error("customers:listAccessibleCustomers failed", error))

    customer_id = env("GOOGLE_ADS_CUSTOMER_ID")
    if customer_id:
        q = "SELECT customer.id, customer.descriptive_name FROM customer LIMIT 1"
        try:
            search(format_customer_id(customer_id), q)
            lines.append("googleAds:search OK (customer query)")
        except Exception as error:
            lines.append(query_error("googleAds:search failed", error))

        q2 = "SELECT customer.id FROM customer LIMIT 1"
        try:
            search_stream(format_customer_id(customer_id), q2)
            lines.append("googleAds:searchStream OK (customer query)")
        except Exception as error:
            lines.append(query_error("googleAds:searchStream failed", error))
    else:
        lines.append("GOOGLE_ADS_CUSTOMER_ID not set; skipping GAQL endpoint checks.")

    return "\n".join(lines)


@mcp.resource("gaql://reference")
def gaql_reference() -> str:
    return """
# Google Ads Query Language quick reference

Basic structure:
SELECT field1, field2
FROM resource_name
WHERE condition
ORDER BY metric DESC
LIMIT 50

Common resources for this MCP:
- campaign
- ad_group
- ad_group_ad
- keyword_view
- search_term_view
- campaign_search_term_view
- asset
- campaign_asset
- ad_group_ad_asset_view
- ad_group_ad_asset_combination_view
- landing_page_view
- google_ads_field

Tips:
- Cost values are in micros.
- Use `list_resources()` and `list_fields()` to discover valid report fields.
- Use `build_report_query()` when you want help assembling a GAQL query.
"""


@mcp.prompt("google_ads_workflow")
def google_ads_workflow() -> str:
    return """
Recommended workflow:
1. Run `healthcheck()`.
2. Run `list_accounts()`.
3. Run `get_account_currency(customer_id=...)`.
4. Use one of the opinionated tools:
   - `get_campaign_performance`
   - `get_search_term_performance`
   - `get_keyword_performance`
   - `get_auction_insights`
   - `get_asset_inventory`
5. For custom analysis, use `list_resources`, `list_fields`, `build_report_query`, and `run_gaql`.
6. For planning, use the Keyword Planner tools.
"""


@mcp.prompt("gaql_help")
def gaql_help() -> str:
    return """
Examples:

Search terms:
SELECT campaign.name, ad_group.name, search_term_view.search_term, metrics.clicks, metrics.cost_micros
FROM search_term_view
WHERE segments.date BETWEEN '2026-03-01' AND '2026-03-18'
ORDER BY metrics.cost_micros DESC
LIMIT 50

Keywords:
SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text, ad_group_criterion.keyword.match_type, metrics.conversions
FROM keyword_view
WHERE segments.date BETWEEN '2026-03-01' AND '2026-03-18'
ORDER BY metrics.conversions DESC
LIMIT 50

Assets:
SELECT campaign.name, campaign_asset.field_type, asset.id, asset.name, metrics.clicks
FROM campaign_asset
WHERE segments.date BETWEEN '2026-03-01' AND '2026-03-18'
LIMIT 50
"""


if __name__ == "__main__":
    mcp.run(transport="stdio")
