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
│       └── creative-briefs/
│           └── {mmmyy}/
│               ├── _index.md                              ← month-level briefs index
│               └── {ad-name}-v{N}_{keyword}_{mmmyy}.md   ← individual designer briefs
```

### What lives where

| Document | Agent | Frequency | Path |
|----------|-------|-----------|------|
| Campaign Structure | paid-ads-structure-agent | One per campaign (stable) | `{campaign-name}_campaign-structure.md` |
| Ad Creative / Copy | ad-creative-agent | One per monthly rotation | `{campaign-name}_ad-creative_{mmmyy}.md` |
| Visual Creative Briefs | visual-creative-brief-agent | One per visual concept | `creative-briefs/{mmmyy}/{brief}.md` |

### Navigation flow

1. Pick a **channel** folder
2. Pick a **campaign** folder → open `_index.md` for the master overview
3. From the campaign index, jump to:
   - The **campaign structure** (bidding, audiences, tracking)
   - Any **ad creative rotation** by month (copy, headlines, visual concepts)
   - The **creative briefs** folder for any month (designer-ready production specs)
4. Each creative brief links back to its parent ad creative and campaign structure

## Campaigns

| Campaign | Channel | Status | Structure | Latest Creative | Creative Briefs |
|----------|---------|--------|-----------|-----------------|----------------|
| [US-CA Meta Leads — Reader Acquisition](meta/us-ca_meta_leads_reader-acquisition_mar26/_index.md) | Meta | Draft | Pending | Pending | [Mar 2026 (5 briefs)](meta/us-ca_meta_leads_reader-acquisition_mar26/creative-briefs/mar26/_index.md) |

## Status Key

| Status | Meaning |
|--------|---------|
| Pending | Companion agent has not yet run |
| Draft | File created, not yet reviewed |
| In Review | Awaiting stakeholder approval |
| Approved | Approved for launch |
| Live | Campaign running in-platform |
| Retired | Campaign no longer active |
