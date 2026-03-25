# Meta Ads: Campaign → Objective context file (planning)

**Goal:** One source-of-truth file that maps every Meta Ads campaign to exactly one campaign objective. The paid ads intelligence agent loads this file on each run and uses it to decide which conversion to measure per campaign—eliminating logic errors and API/fallback drift. Google Ads is unchanged.

**Constraint:** Each campaign has exactly one objective; the file only changes when adding new campaigns or assigning a new objective to an existing campaign.

---

## 1. Current state (problem)

Today the agent derives “primary conversion” for each campaign from:

1. **Hardcoded set** `CAMPAIGNS_PRIMARY_LEAD_EMAIL_VALID` (four campaign names → `lead_email-valid`)
2. **Meta API** `campaign.objective` (e.g. `LEADS` → standard `lead`)
3. **Optimization map** from ad sets (`custom_event_str` / `custom_event_type`) → e.g. `qualified_meeting_booked`, `2025_industry_study`, `COMPLETE_REGISTRATION`
4. **Fallback** infer from which of lead / qualified_meeting_booked / complete_registration has data in the period

This leads to:

- Logic spread across code, API, and fallbacks
- Renames or API changes can change behavior
- New campaigns can get the wrong objective until someone updates code
- No single place to audit “what we measure for each campaign”

---

## 2. Design: context file as single source of truth

### 2.1 File role

- **Authority:** For Meta Ads, the agent **only** uses this file to decide which conversion (action_type) to use for “Results” per campaign. No optimization map, no fallback inference (or fallback only for campaigns not yet in the file).
- **Scope:** Meta Ads only. Google Ads logic is unchanged.
- **Updates:** File is updated only when:
  - A **new campaign** is added in Meta and we assign it an objective, or
  - We **correct** the objective for an existing campaign.

### 2.2 Campaign identifier: use `campaign_id`

- **Primary key:** Meta `campaign_id` (string, e.g. `"6941195367868"`). Stable; does not change if the campaign is renamed.
- **Human context:** Store `campaign_name` in the file for readability and audits. Lookup is always by `campaign_id`; name is for documentation and optional “discover new campaigns” flows.
- **New campaigns:** When a new campaign appears in the API and is missing from the file, the agent can either (a) treat it as “no objective” and report 0 results for that campaign until the file is updated, or (b) have a one-time fallback (e.g. use existing logic) and log “campaign not in context file” so the file can be updated.

### 2.3 Objective vocabulary (allowed values)

The file’s `objective` field must be one of a fixed set that maps 1:1 to the Meta action_type used for reading results:

| Objective key (in file) | Meta action_type | Notes |
|-------------------------|-------------------|--------|
| `lead` | `lead` | Standard Meta Lead / Lead Gen |
| `website_complete_registration` | `offsite_conversion.fb_pixel_complete_registration` | Website Completed Registration |
| `qualified_meeting_booked` | `offsite_conversion.fb_pixel_custom.qualified_meeting_booked` | Custom pixel |
| `2025_industry_study` | `offsite_conversion.fb_pixel_custom.2025_industry_study` | Custom pixel |
| `lead_email-valid` | `offsite_conversion.fb_pixel_custom.lead_email-valid` | Custom pixel |
| *(future)* | `offsite_conversion.fb_pixel_custom.<event_name>` | Any new custom event |

Recommendation: store **short keys** in the file (e.g. `lead`, `lead_email-valid`, `2025_industry_study`) and map them in code to the full `action_type` used in the Meta insights API. That keeps the file readable and avoids typos in long strings.

### 2.4 File format and location

- **Format:** JSON (consistent with rest of project; easy to load and validate).
- **Location:**  
  `docs/paid ads intelligence/meta_campaign_objectives.json`  
  (or alongside the agent: `ai system/python scripts/paid ads intelligence agent/meta_campaign_objectives.json`).  
  Recommendation: under `docs/paid ads intelligence/` so it’s clearly shared context, not code.

**Proposed schema:**

```json
{
  "version": "1",
  "updated": "2026-03-14",
  "description": "One objective per Meta Ads campaign. Used by paid ads intelligence agent for Results per campaign.",
  "objective_keys": {
    "lead": "lead",
    "website_complete_registration": "offsite_conversion.fb_pixel_complete_registration",
    "qualified_meeting_booked": "offsite_conversion.fb_pixel_custom.qualified_meeting_booked",
    "2025_industry_study": "offsite_conversion.fb_pixel_custom.2025_industry_study",
    "lead_email-valid": "offsite_conversion.fb_pixel_custom.lead_email-valid"
  },
  "campaigns": {
    "6941195367868": {
      "campaign_name": "Meta-Sales-Industry Report_Prospecting",
      "objective": "2025_industry_study"
    },
    "6954327557268": {
      "campaign_name": "au-uk_pms_prospecting_website-conv",
      "objective": "lead_email-valid"
    }
  }
}
```

- **Lookup:** Agent loads the file once per run; for each campaign, `primary_action_type = objective_keys[campaigns[campaign_id].objective]`. If `campaign_id` is missing, behavior is defined by policy (see 2.2).

### 2.5 Optional: name-based fallback for unknown campaigns

- If a campaign_id is **not** in the file, options:
  - **Strict:** Report 0 results for that campaign and log a warning (“Campaign X not in meta_campaign_objectives.json”).
  - **Lenient:** Fall back to current logic (optimization map + API objective + inference) and log that the campaign is missing from the file so it can be added.
- Recommendation: **Strict** so the file stays the single source of truth and gaps are visible and fixable.

---

## 3. Agent integration (how the agent references the file)

### 3.1 Load on each run

- At the start of the Meta data path (e.g. when `pull_full_meta_data` or `build_lead_analysis` is called), load the context file from the chosen path (e.g. workspace root + `docs/paid ads intelligence/meta_campaign_objectives.json`).
- If the file is missing or invalid: fail the run with a clear error (e.g. “Meta campaign objectives file not found or invalid”) so the file is not silently ignored.

### 3.2 Replace current primary-action logic

- **Remove** (or stop using for “primary”):
  - `CAMPAIGNS_PRIMARY_LEAD_EMAIL_VALID`
  - Use of `optimization_map` and `campaign.objective` to decide primary conversion for Results
  - Fallback that infers from allowed_breakdown (lead / qualified_meeting_booked / complete_registration)
- **New flow:**  
  `_primary_action_for_campaign(campaign, context)`  
  - Read `campaign_id = campaign.get("id")`.  
  - Look up `campaign_id` in `context["campaigns"]`.  
  - If not found: return `None` (and optionally log “campaign not in context file”; report 0 results for that campaign).  
  - If found: get `objective` (short key), then `primary_action_type = context["objective_keys"][objective]`.  
  - Return `primary_action_type`.  
- **Optimization map:** Can still be used for other purposes (e.g. diagnostics or reporting) but **not** for deciding which conversion to count as Results. That comes only from the context file.

### 3.3 Context as “context window”

- “References this file as a context window” is implemented by: (1) loading the file into memory at run start, and (2) using it as the only source for campaign_id → objective → action_type when computing Meta Results. No LLM “context window” is required for this; the agent code simply reads the JSON and does a dict lookup. If later you add an LLM that summarizes or explains the report, you can pass the same file path or contents into that step as context.

### 3.4 Math guarantees

- For each in-scope campaign, the agent:
  1. Gets `primary_action_type` from the context file only.
  2. Reads the count for that single action_type from the campaign’s period insights (`_read_conversion_count`).
  3. Adds that count to total results.
- No double-counting (one objective per campaign), no mixing of objectives (one conversion type per campaign). The only way the “math” can be wrong is if the file has the wrong objective for a campaign (human error), which is auditable and fixable in one place.

---

## 4. Populating and maintaining the file

### 4.1 Initial population

1. **Export current campaign list:** Run the agent (or a small script) for a recent period to get all Meta campaign IDs and names from the API.
2. **Assign objectives:** For each campaign, set `objective` using:
   - Existing overrides (e.g. the four `lead_email-valid` campaigns, Industry Report → `2025_industry_study`)
   - Optimization map / API objective for the rest (Leads → `lead`, etc.)
3. **Write** `meta_campaign_objectives.json` with the schema above.
4. **Review:** Spot-check a few campaigns in Meta Ads Manager to confirm the chosen conversion matches the file.
5. **Switch agent** to use the file only; remove or bypass current primary-action logic.

### 4.2 When to update the file

- **New campaign in Meta:** Add an entry to `campaigns` with `campaign_id`, `campaign_name`, and the correct `objective` key.
- **Objective change for an existing campaign:** Update the `objective` for that `campaign_id` in the file.
- **Renamed campaign:** Update `campaign_name` in the file for readability; `campaign_id` and `objective` stay the same.
- **New conversion type:** Add a new key to `objective_keys` and use it in the relevant campaign(s).

### 4.3 Validation (optional but recommended)

- On load, validate:
  - Every `objective` in `campaigns` exists in `objective_keys`.
  - No duplicate `campaign_id`.
- If validation fails, abort the run with an error pointing to the file and the invalid entry.

---

## 5. File location and discovery

- **Recommended path:**  
  `docs/paid ads intelligence/meta_campaign_objectives.json`
- **Resolve path:** From the agent script, resolve relative to workspace root (e.g. `WORKSPACE_ROOT / "docs" / "paid ads intelligence" / "meta_campaign_objectives.json"`) so the same path works from CLI and from any CWD.
- **Discovery:** Document in the same folder (e.g. a short `README` or a comment in the implementation plan) that this file is the authority for Meta campaign → objective and must be updated when new campaigns are added or objectives change.

---

## 6. Summary

| Item | Decision |
|------|----------|
| **Scope** | Meta Ads only; Google Ads unchanged |
| **Authority** | Single JSON file maps campaign_id → objective key |
| **Campaign key** | Meta `campaign_id` (stable) |
| **Objective keys** | Short names in file; code maps to Meta action_type |
| **When file changes** | New campaigns or objective corrections only |
| **Agent behavior** | Load file once per run; use it as sole source for primary conversion per campaign; no optimization-map/fallback for Results |
| **Unknown campaigns** | Strict: 0 results + warning (recommended) |
| **Location** | `docs/paid ads intelligence/meta_campaign_objectives.json` |

This gives a single, auditable mapping so the agent always measures the correct conversion per campaign and avoids math errors from mixed logic and fallbacks.

---

## 7. Implemented mapping (from conversation corrections)

- **File:** `docs/paid ads intelligence/meta_campaign_objectives.json`
- **Agent:** Loads file in `build_lead_analysis()`; `_primary_action_for_campaign(..., meta_objectives)` uses it when present. Unknown campaigns: strict (0 results + stderr warning). File missing: fallback to optimization map + API + inference.

| campaign_id   | campaign_name                              | objective                    |
|---------------|---------------------------------------------|-----------------------------|
| 6891715059868 | Meta-Leads-PMS_Conversions-Manual           | lead                        |
| 6913423474668 | Meta-Leads-PMS_Conversions-Manual-Broad     | lead                        |
| 6894149906468 | Meta-Leads-Guidebook_Conversions            | lead                        |
| 6894156598868 | Meta-Sales-PMS_Conversions-Retargeting      | qualified_meeting_booked    |
| 6893093544468 | Meta-Sales-Webinar_Registrations            | website_complete_registration |
| 6896525103468 | [Leads] \| hostfully \| pt-br — meeting     | qualified_meeting_booked    |
| 6941195367868 | Meta-Sales-Industry Report_Prospecting     | 2025_industry_study         |
| 6954326744668 | au-uk_pms_prospecting_website-conv         | lead_email-valid            |
| 6954326449668 | au-uk_pms_retargeting_website-conv         | lead_email-valid            |
| 6954323673468 | ca-us_pms_retargeting_website-conv          | lead_email-valid            |
| 6954321351868 | ca-us_pms_prospecting_website-conv          | lead_email-valid            |
| 6922497287068 | Meta-Engagement-Boosted_Posts               | none                        |
| 6914921864468 | [Post Promovido] \| pt-br                   | none                        |
