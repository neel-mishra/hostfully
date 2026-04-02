# Paid Ads Standardized Analyses Playbook

Use this playbook to run recurring paid ads analyses with a fixed structure, fixed measurement definitions, and consistent output format across channels.

---

## Global Operating Contract

### Purpose

When prompted with a standardized analysis name, the agent should run the exact same analysis framework every time (unless the user explicitly requests deviations).

### Global Prompt Pattern

Use this prompt pattern:

`Run <analysis_name> for <channel> for <time_range> on <account_scope>.`

Examples:

- `Run the 5 check optimization analysis for Meta Ads for March 2026 on Hostfully.`
- `Run the 5 check optimization analysis for Google Ads for March 2026 on all US accounts.`

### Account Scope Rules

- If user specifies one account, run only that account.
- If user says "portfolio" or "all accounts", run all available accounts for that channel.
- If account scope is missing, default to all active accounts in that channel and state the default in the output header.

### Standard Output Header (Required)

Every standardized analysis output must start with:

- Analysis name
- Channel
- Date range
- Accounts included
- Currency handling notes (single currency or mixed currency)
- Data source used (live API/MCP + endpoint/tool names)
- Run timestamp

### Standard QA Block (Required)

Always include:

- Coverage check: entities with spend > 0 vs total entities pulled
- Missing/unknown naming IDs count
- Any API limitations or breakdown constraints
- Any heuristic assumptions used

---

## Standard Analysis Catalog

This section defines reusable analysis names that can be triggered quickly.

### Active Standard Analyses

1. `5 check optimization analysis` (Global: Meta + Google)
2. `meta creative performance analysis` (Meta only)
3. `google search terms analysis` (Google only)
4. `google keyword analysis` (Google only)

The first three analyses are fully specified below. The remaining analysis is kept as a placeholder for next expansion.

---

## Global Analysis Standard: 5 Check Optimization Analysis

### Intent

Provide a consistent optimization snapshot using five checks:

1. Delivery
2. CPA
3. Frequency
4. Fatigue
5. Efficiency

### Required Grain Outputs

The analysis must output exactly three tables:

1. Campaign-level table
2. Campaign + Ad Set/Ad Group table
3. Campaign + Ad Set/Ad Group + Ad/Asset table

Note: naming should map by channel:

- Meta: Campaign, Ad Set, Ad
- Google: Campaign, Ad Group, Ad (or Asset Group for PMax where relevant)

### Required Metric Columns

Each table must include:

- Spend
- Lead-like results (or primary conversion count if lead-only is unavailable)
- Delivery
- CPA
- Frequency
- Fatigue
- Efficiency

### Cross-Channel Definitions (Canonical)

- **Delivery**
  - `No Delivery`: spend = 0
  - `Low`: low spend/impression volume relative to period distribution
  - `Moderate`: middle volume band
  - `Strong`: upper volume band
- **CPA**
  - spend / primary conversion count
  - If conversions = 0, set CPA = `-`
- **Frequency**
  - impressions / reach (or best available channel proxy when direct reach unavailable)
- **Fatigue**
  - Derived from elevated frequency + weakening engagement indicators
  - Must be labeled: `Low`, `Elevated`, or `High`
- **Efficiency**
  - Composite efficiency label from cost + engagement + conversion productivity
  - Must be labeled: `Low`, `Medium`, or `High`

### Output Structure (Canonical)

1. Header block (standard)
2. Definitions used for the five checks
3. Table 1: Campaigns
4. Table 2: Campaign + Ad Set/Ad Group
5. Table 3: Campaign + Ad Set/Ad Group + Ad/Asset
6. Key findings:
   - Top opportunities to scale
   - Entities to refresh due to fatigue
   - Entities to reduce/pause due to poor efficiency

---

## Channel-Specific Standards

## Meta Ads Standards

Use for Meta/Facebook/Instagram ads data.

### Meta: 5 Check Optimization Analysis (Standardized Prompt Spec)

#### Trigger Phrases

- `run the 5 check optimization analysis for meta ads`
- `run 5-check on meta portfolio`
- `meta optimization 5 check`

#### Meta Measurement Rules

- Primary conversion should prefer lead-intent action types (for example: lead, complete_registration, qualified lead custom events) when available.
- Conversion reporting basis is **mandatory `conversion_time`** for Meta conversion metrics.
- Do not report Meta conversion totals from impression-time accounting.
- Frequency uses native Meta definition: impressions / reach.
- Fatigue should emphasize creative wear-out signals (high frequency + declining CTR/link engagement).
- Efficiency can include CTR, CPC, and conversion density (results per 1k impressions) in a composite label.

#### Meta Output Requirements

- Three required tables at:
  - Campaign
  - Campaign + Ad Set
  - Campaign + Ad Set + Ad
- Include account list and state if any account had zero delivery.
- Include an explicit reporting-basis line: `Meta conversion accounting: conversion_time`.
- Include conversion action declaration (for example: `lead_email-valid`, `qualified_meeting_booked`).
- Include a short action list:
  - `Scale`
  - `Hold`
  - `Refresh Creative`
  - `Reduce/Pause`

#### Reusable Meta Prompt Template

`Run the standardized 5 check optimization analysis for Meta Ads for <time_range> on <account_scope>. Use the canonical five checks (Delivery, CPA, Frequency, Fatigue, Efficiency), produce the three required tables (Campaign; Campaign+Ad Set; Campaign+Ad Set+Ad), and finish with prioritized optimization actions (Scale, Hold, Refresh Creative, Reduce/Pause).`

---

## Google Ads Standards

Use for Google Ads data.

### Google: 5 Check Optimization Analysis (Standardized Prompt Spec)

#### Trigger Phrases

- `run the 5 check optimization analysis for google ads`
- `run 5-check on google portfolio`
- `google optimization 5 check`

#### Google Measurement Rules

- Primary conversion should use the account's primary conversion action set for campaign optimization goals.
- Frequency should use available Google reach/frequency metrics when present; when unavailable, use a documented proxy and label it clearly.
- Fatigue should be inferred from rising frequency/impression concentration combined with softening CTR/CVR trends.
- Efficiency should combine conversion productivity and cost discipline (for example: CTR/CVR/CPC/CPA profile).

#### Google Output Requirements

- Three required tables at:
  - Campaign
  - Campaign + Ad Group (or Asset Group for PMax)
  - Campaign + Ad Group/Asset Group + Ad/Asset
- Include campaign type notes where structure differs (Search, Performance Max, Display, Video).
- Include a short action list:
  - `Scale`
  - `Hold`
  - `Refine Targeting/Terms`
  - `Reduce/Pause`

#### Reusable Google Prompt Template

`Run the standardized 5 check optimization analysis for Google Ads for <time_range> on <account_scope>. Use the canonical five checks (Delivery, CPA, Frequency, Fatigue, Efficiency), produce the three required tables (Campaign; Campaign+Ad Group/Asset Group; Campaign+Ad Group/Asset Group+Ad/Asset), and finish with prioritized optimization actions (Scale, Hold, Refine Targeting/Terms, Reduce/Pause).`

### Google-Only Analysis: Search Terms Analysis (Standardized Prompt Spec)

#### Trigger Phrases

- `run search terms analysis for google ads`
- `run standardized google search terms analysis`
- `analyze search terms for wasted spend and scaling`

#### Intent

Surface search term opportunities and waste at query level, then map actions to keyword/ad group/campaign controls.

#### Required Inputs

- Time range
- Account scope
- Campaign type scope (default: Search only; include PMax search categories only if available and explicitly labeled)
- Conversion goal definition (primary conversion set)

#### Core Measurement Parameters

- Spend
- Clicks
- Impressions
- CTR
- Conversions
- CPA
- Conversion rate
- Impression share metrics (if available)
- Match type context (exact/phrase/broad where applicable)

#### Classification Rules (Required)

- `Scale Candidate`: high conversion efficiency and acceptable volume
- `Protect/Exactify`: strong converting query currently on loose match; candidate for exact keyword buildout
- `Negative Candidate`: high spend, weak/no conversion signal
- `Watchlist`: mixed signal, insufficient confidence, or short-term volatility

#### Required Output Structure

1. Standard header + QA block
2. Definitions and thresholds used
3. Table A: Top converting search terms (scaling list)
4. Table B: Wasteful search terms (negative list)
5. Table C: Query-to-action map with:
   - Recommended action (`Add Exact`, `Add Phrase`, `Add Negative`, `Bid Down`, `No Change`)
   - Destination ad group/campaign
   - Expected impact note
6. Prioritized action plan:
   - Immediate negatives
   - Exact/phrase buildouts
   - Budget shifts tied to query clusters

#### Reusable Google Search Terms Prompt Template

`Run the standardized Google search terms analysis for <time_range> on <account_scope>. Focus on Search campaigns by default. Return converting terms, wasteful terms, and a query-to-action map with explicit recommendations (Add Exact, Add Phrase, Add Negative, Bid Down, No Change), using CPA/CVR/CTR/spend evidence and confidence flags.`

### Google-Only Analysis Placeholders (To Standardize Next)

- `google keyword analysis`

---

## Meta-Only Analysis: Creative Performance Analysis (Standardized Prompt Spec)

#### Trigger Phrases

- `run meta creative performance analysis`
- `run standardized creative analysis for meta`
- `analyze meta creative winners and fatigue`

#### Intent

Evaluate creative-level performance on Meta and translate findings into scaling, refresh, and testing actions.

#### Required Inputs

- Time range
- Account scope
- Objective scope (lead gen/sales/engagement or all)
- Creative taxonomy availability (format, hook, angle, CTA, visual style) if present

#### Core Measurement Parameters

- Spend
- Impressions
- Reach
- Frequency
- CTR (link CTR where available)
- CPC
- Results (primary conversion)
- CPA
- Results per 1k impressions

#### Creative Diagnostics (Required)

- `Winner`: efficient CPA + strong engagement + stable frequency
- `Scalable`: efficient enough with headroom (low/moderate fatigue)
- `Fatiguing`: elevated/high frequency with weakening CTR or rising CPA
- `Underperformer`: weak conversion efficiency and no supporting engagement signal
- `Learning/Insufficient`: low delivery or low signal confidence

#### Required Output Structure

1. Standard header + QA block
2. Creative scoring/label definitions used
3. Table A: Creative leaderboard (Campaign + Ad Set + Ad/Creative)
4. Table B: Fatigue watchlist with refresh urgency
5. Table C: Concept-level rollup (if metadata available: hook/angle/format/CTA)
6. Action plan:
   - `Scale now` creatives
   - `Refresh this week` creatives
   - `Pause/reduce` creatives
   - `Next tests` (new angle/hook proposals)

#### Reusable Meta Creative Prompt Template

`Run the standardized Meta creative performance analysis for <time_range> on <account_scope>. Evaluate creative-level winners, scalable assets, fatigue risk, and underperformers using spend, CTR, CPC, frequency, results, CPA, and results per 1k impressions. Return the leaderboard, fatigue watchlist, concept rollup, and prioritized actions (Scale now, Refresh this week, Pause/reduce, Next tests).`

### Meta-Only Analysis Placeholders (To Standardize Next)

- `meta audience fatigue analysis`

---

## Implementation Notes For Agents

- If user requests a standardized analysis by name, prioritize this playbook over ad hoc formatting.
- If user asks for extra breakdowns, append them without removing canonical tables.
- If channel-specific metrics are missing, use documented proxies and explicitly label assumptions.
- Always keep ordering and naming of the five checks consistent to preserve comparability over time.

