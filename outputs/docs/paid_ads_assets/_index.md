# Paid Ads Campaign Assets

All paid ads outputs live here — campaign structure, ad creative/copy, and visual creative briefs. Everything for a campaign is organized in one folder so you can navigate from structure → copy → designer briefs without jumping across directories.

## Channels

| Channel | Folder | Description |
|---------|--------|-------------|
| LinkedIn | [linkedin/](linkedin/) | B2B campaigns — lead gen, brand awareness, ABM |
| Meta | [meta/](meta/) | Facebook/Instagram — reader acquisition, retargeting |
| Google | [google/](google/) | Search, Display, PMAX, YouTube, Demand Gen |
| TikTok | [tiktok/](tiktok/) | In-feed, Spark Ads, TopView |
| X | [x/](x/) | Image, video, carousel, conversation targeting |

## Folder Structure

```
docs/paid_ads_assets/
├── _index.md                                              ← this file
├── {channel}/
│   └── {campaign-name}/
│       ├── _index.md                                      ← campaign master index
│       ├── {campaign-name}_campaign-structure.md           ← paid-ads-structure-agent (one per campaign)
│       ├── {campaign-name}_ad-creative_{mmmyy}.md         ← ad-creative-agent (one per creative rotation)
│       ├── creative-briefs/
│       │   └── {mmmyy}/
│       │       ├── _index.md                              ← month-level briefs index
│       │       └── {ad-name}-v{N}_{keyword}_{mmmyy}.md   ← individual designer briefs
│       └── creative-deliverables/
│           └── {mmmyy}/
│               ├── _index.md                              ← month-level deliverables index
│               ├── {ad-name}-v{N}_canva-deliverables_{mmmyy}.md  ← Canva/Figma handoffs
│               └── canva_mcp_sync_plan.json               ← optional MCP sync contract
```

### What lives where

| Document | Agent | Frequency | Path |
|----------|-------|-----------|------|
| Campaign Structure | paid-ads-structure-agent | One per campaign (stable) | `{campaign-name}_campaign-structure.md` |
| Ad Creative / Copy | ad-creative-agent | One per monthly rotation | `{campaign-name}_ad-creative_{mmmyy}.md` |
| Visual Creative Briefs | visual-creative-brief-agent | One per visual concept | `creative-briefs/{mmmyy}/{brief}.md` |
| Creative deliverables | operator / Canva MCP | Per built concept or batch | `creative-deliverables/{mmmyy}/*` (exports, edit links, `canva_mcp_sync_plan.json`) |

### Navigation flow

1. Pick a **channel** folder
2. Pick a **campaign** folder → open `_index.md` for the master overview
3. From the campaign index, jump to:
   - The **campaign structure** (bidding, audiences, tracking)
   - Any **ad creative rotation** by month (copy, headlines, visual concepts)
   - The **creative briefs** folder for any month (designer-ready production specs)
   - The **creative-deliverables** folder for built assets (Canva exports, sync plans)
4. Each creative brief links back to its parent ad creative and campaign structure; deliverable docs link back to their source brief

## Campaigns

| Campaign | Channel | Status | Structure | Latest Creative | Creative Briefs |
|----------|---------|--------|-----------|-----------------|----------------|
| [Hostfully PMS Paid Campaign (Q2 2026)](hostfully_pms_paid_campaign_q2_2026.md) | Multi-channel (Google/Meta/LinkedIn) | Draft | [Campaign plan](hostfully_pms_paid_campaign_q2_2026.md) | Pending | Pending |
| [US-CA Meta Leads — Reader Acquisition](meta/us-ca_meta_leads_reader-acquisition_mar26/_index.md) | Meta | Draft | Pending | Pending | [Mar 2026 briefs](meta/us-ca_meta_leads_reader-acquisition_mar26/creative-briefs/mar26/_index.md) · [Mar 2026 deliverables](meta/us-ca_meta_leads_reader-acquisition_mar26/creative-deliverables/mar26/_index.md) |
| [US LinkedIn B2B Cold Lead Gen](linkedin/us_linkedin_b2b-cold_lead-gen_mar26/_index.md) | LinkedIn | Draft | [Campaign structure](linkedin/us_linkedin_b2b-cold_lead-gen_mar26/campaign-structure/us_linkedin_b2b-cold_lead-gen_mar26_campaign-structure.md) | [Mar 2026 ad creative](linkedin/us_linkedin_b2b-cold_lead-gen_mar26/ad-creative/us_linkedin_b2b-cold_lead-gen_mar26_ad-creative_mar26.md) | [Mar 2026 briefs](linkedin/us_linkedin_b2b-cold_lead-gen_mar26/creative-briefs/mar26/_index.md) · [Mar 2026 deliverables](linkedin/us_linkedin_b2b-cold_lead-gen_mar26/creative-deliverables/mar26/_index.md) |
| [US LinkedIn Leads — Hostfully PMS](linkedin/us_linkedin_leads_hostfully-pms_apr26/_index.md) | LinkedIn | Draft | [Campaign structure](linkedin/us_linkedin_leads_hostfully-pms_apr26/campaign-structure/us_linkedin_leads_hostfully-pms_apr26_campaign-structure.md) | [Apr 2026 ad creative](linkedin/us_linkedin_leads_hostfully-pms_apr26/ad-creative/us_linkedin_leads_hostfully-pms_apr26_ad-creative_apr26.md) | [Apr 2026 briefs](linkedin/us_linkedin_leads_hostfully-pms_apr26/creative-briefs/apr26/_index.md) · [Apr 2026 deliverables](linkedin/us_linkedin_leads_hostfully-pms_apr26/creative-deliverables/apr26/_index.md) |

## Status Key

| Status | Meaning |
|--------|---------|
| Pending | Companion agent has not yet run |
| Draft | File created, not yet reviewed |
| In Review | Awaiting stakeholder approval |
| Approved | Approved for launch |
| Live | Campaign running in-platform |
| Retired | Campaign no longer active |
