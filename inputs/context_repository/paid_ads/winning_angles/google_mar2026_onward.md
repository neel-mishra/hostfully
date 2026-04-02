## Google Ads — Winning angles (Mar 2026 onward)

### ROI-heavy campaigns (from Salesforce, Mar 2026 onward)
Top by `roi_priority_weight = pipeline + 2× closed_won`:

utm_source                   utm_campaign_norm  pipeline_amount  closed_won_amount  roi_priority_weight
    google                             Website           1488.0                0.0               1488.0
    google                                 NaN             64.8               64.8                194.4
    google Hostfully - Search - Brand - US/CAN              0.0                0.0                  0.0
    google                __PMAX_PLACEHOLDER__              0.0                0.0                  0.0

### Top-performing RSA text assets (30d lookback; filter to Mar 2026 onward downstream)

These are ranked by conversions then clicks from the MCP RSA asset view pull.

#### Headlines
- **HEADLINE**: “Hostfully” — clicks=745, conv=22.75, impr=1336
- **HEADLINE**: “Property Management Made Easy” — clicks=218, conv=13.00, impr=384
- **HEADLINE**: “Hostfully” — clicks=379, conv=8.00, impr=988
- **HEADLINE**: “Hostfully Property Management” — clicks=233, conv=5.00, impr=553
- **HEADLINE**: “Starting at $15/property” — clicks=159, conv=5.00, impr=297
- **HEADLINE**: “Vacation Rental Software” — clicks=133, conv=5.00, impr=245
- **HEADLINE**: “Hostfully Property Management” — clicks=283, conv=4.50, impr=520
- **HEADLINE**: “Hostfully” — clicks=119, conv=4.00, impr=253
- **HEADLINE**: “Property Management Software” — clicks=210, conv=3.25, impr=644
- **HEADLINE**: “Hostfully” — clicks=280, conv=3.00, impr=647
- **HEADLINE**: “Hostfully” — clicks=71, conv=3.00, impr=146
- **HEADLINE**: “Property Management Made Easy” — clicks=53, conv=3.00, impr=95
- **HEADLINE**: “Property Management Software” — clicks=150, conv=2.00, impr=291
- **HEADLINE**: “Property Management Software” — clicks=112, conv=2.00, impr=209
- **HEADLINE**: “Hostfully” — clicks=89, conv=2.00, impr=316
- **HEADLINE**: “Property Management Made Easy” — clicks=50, conv=2.00, impr=164
- **HEADLINE**: “Hostfully Channel Manager” — clicks=39, conv=2.00, impr=69
- **HEADLINE**: “Happiest Hosts Choose Us” — clicks=27, conv=2.00, impr=207
- **HEADLINE**: “Vacation Rental Software” — clicks=24, conv=2.00, impr=53
- **HEADLINE**: “Save 4 Hours Per Day” — clicks=16, conv=2.00, impr=352
- **HEADLINE**: “All-in-One PMS Solution” — clicks=15, conv=2.00, impr=42
- **HEADLINE**: “Starting at $15/property” — clicks=33, conv=1.75, impr=192
- **HEADLINE**: “Short Term Rental Software” — clicks=27, conv=1.75, impr=115
- **HEADLINE**: “Property Managers & Owners” — clicks=70, conv=1.50, impr=119
- **HEADLINE**: “Hostfully Property Management” — clicks=34, conv=1.25, impr=157

#### Descriptions
- **DESCRIPTION**: “The leading property management software for Airbnb, VRBO, and other rental properties.” — clicks=633, conv=21.75, impr=1219
- **DESCRIPTION**: “Choose the vacation rental manager that gives you the most flexibility at the best price.” — clicks=329, conv=13.25, impr=640
- **DESCRIPTION**: “Connect to 120+ industry partners for property cleaning, insurance & marketing automation.” — clicks=438, conv=7.50, impr=929
- **DESCRIPTION**: “The leading property management software for Airbnb, VRBO, and other rental properties.” — clicks=256, conv=5.00, impr=596
- **DESCRIPTION**: “Choose the vacation rental manager that gives you the most flexibility at the best price.” — clicks=217, conv=5.00, impr=505
- **DESCRIPTION**: “The leading property management software for Airbnb, VRBO, and other letting properties.” — clicks=121, conv=5.00, impr=299
- **DESCRIPTION**: “Optimize your short-term rentals with Hostfully’s property management software for hosts.” — clicks=207, conv=4.00, impr=531
- **DESCRIPTION**: “The leading property management software for Airbnb, VRBO, and other rental properties.” — clicks=176, conv=4.00, impr=499
- **DESCRIPTION**: “Choose the holiday letting software that gives you the most flexibility at the best price.” — clicks=47, conv=4.00, impr=143
- **DESCRIPTION**: “Connect to 120+ industry partners for property cleaning, insurance & marketing automation.” — clicks=174, conv=3.33, impr=351
- **DESCRIPTION**: “"Fast, Modern Vacation Rental Software with Outstanding Customer Support."” — clicks=81, conv=3.00, impr=170
- **DESCRIPTION**: “The leading property management software for Airbnb, VRBO, and other rental properties.” — clicks=111, conv=2.25, impr=578
- **DESCRIPTION**: “Choose the vacation rental manager that gives you the most flexibility at the best price.” — clicks=185, conv=2.00, impr=388
- **DESCRIPTION**: “Thousands of vacation rental owners use Hostfully to automate, increase profit, and scale.” — clicks=167, conv=2.00, impr=378
- **DESCRIPTION**: “Thousands of vacation rental owners use Hostfully to automate, save time, increase revenue” — clicks=157, conv=2.00, impr=356
- **DESCRIPTION**: “Connect to 120+ industry partners for property cleaning, insurance & marketing automation.” — clicks=53, conv=2.00, impr=322
- **DESCRIPTION**: “The leading property management software for Airbnb, VRBO, and other rental properties.” — clicks=47, conv=2.00, impr=94
- **DESCRIPTION**: “Thousands of holiday letting owners use Hostfully to automate, save time, increase revenue” — clicks=24, conv=2.00, impr=127
- **DESCRIPTION**: “Thousands of vacation rental owners use Hostfully to automate, save time, increase revenue” — clicks=29, conv=1.25, impr=179
- **DESCRIPTION**: “Maximize revenue and simplify your short-term rental management with Hostfully PMS.” — clicks=72, conv=1.00, impr=163
- **DESCRIPTION**: “The leading property management software for Airbnb, VRBO, and other rental properties.” — clicks=58, conv=1.00, impr=1877
- **DESCRIPTION**: “Choose the vacation rental manager that gives you the most flexibility at the best price.” — clicks=58, conv=1.00, impr=301
- **DESCRIPTION**: “Optimize your short-term rentals with Hostfully’s rental management software.” — clicks=34, conv=1.00, impr=1101
- **DESCRIPTION**: “Choose the vacation rental manager that gives you the most flexibility at the best price.” — clicks=27, conv=1.00, impr=37
- **DESCRIPTION**: “Optimize your short-term lets with Hostfully’s rental management software.” — clicks=24, conv=1.00, impr=668

### Notes / gaps
- ROI join is exact-match on `utm_campaign_norm` ⇄ `campaign.name` for now. We’ll improve mapping using `gclid` joins and campaign normalization rules (`__PMAX_PLACEHOLDER__`).

### Google extension asset findings (Mar 2026, GAQL)

#### Sitelinks (ad_group_asset = SITELINK)

- **Channel Manager**  
  - Description: "No more double bookings." / "Manage across Airbnb, VRBO, & more."  
  - Aggregated performance (2026-03-01 to 2026-03-25): **565 clicks**, **12 conversions**, **$4,129.26 cost**  
  - This is the clear sitelink winner in the period.

- **Vacation Rental Report**  
  - Description: "11 tactics to grow your revenue." / "Get your free hospitality report."  
  - Aggregated performance (2026-03-01 to 2026-03-25): **77 clicks**, **0 conversions**, **$353.77 cost**

#### Callouts

- No rows returned for `ad_group_asset.field_type = CALLOUT` in this date range/account pull.

#### Structured snippets

- No rows returned for `ad_group_asset.field_type = STRUCTURED_SNIPPET` in this date range/account pull.

### Refinement pass (confidence + blended scoring)
- Confidence thresholds applied: `impressions >= 1000` and `clicks >= 20`.
- Explicit blended score now applied in the joined table: `0.85 * ROI_norm + 0.15 * Perf_norm`.
- Perf component uses conversion efficiency + engagement signal:
  - `Perf_norm = 0.7 * norm(conversions/clicks) + 0.3 * norm(ctr)`.
- Refined output table written to: `outputs/training_data/paid_ads/joined/google_assets_refined_scored.csv`.
- Prompt-ready top angles list written to: `docs/context_repository/paid_ads/winning_angles/top10_reusable_angles_mar2026_onward.md`.


### Learnings refresh (2026-03-31) — full-granularity intelligence pass

- Campaign/ad group/ad analysis shows spend concentration in brand search and PMax; maintain separate guardrails by channel type instead of blended Google-wide thresholds.
- Query-level diagnostics surfaced high-spend zero-conversion terms; convert these into recurring negative-keyword and bid-down automation checks.
- Keyword match-type performance remains uneven; exact/phrase protection should be expanded for top converting query clusters.
- RSA component distribution and performance labels reinforce selective asset rotation: preserve high-signal headline/description families and retire low-signal variants quickly.
- Use campaign-level pacing and query-level efficiency together when training prompts, so recommendations remain both budget-aware and intent-aware.
