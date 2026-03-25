# Where Search Console API & Pomelli Fit in This Workspace

How [Search Console API](https://developers.google.com/webmaster-tools/about) and [Pomelli by Google Labs](https://labs.google.com/pomelli/about/) can be used in automations, scripts, and agents.

---

## 1. Google Search Console API

The [Search Console API](https://developers.google.com/webmaster-tools/about) gives programmatic access to:

- **Properties & sitemaps** — view, add, remove
- **Search analytics** — query clicks, impressions, CTR, position by query/page
- **URL Inspection** — test how Google sees and indexes individual pages

### Already using it

| Item | Use |
|------|-----|
| **search_ranking_agent.py** | Uses GSC Search Analytics (when `GSC_SITE_URL` + `GOOGLE_APPLICATION_CREDENTIALS` are set) to get query/page data and classify striking-distance keywords. Falls back to mock data if not configured. |
| **docs/GSC_GA4_SETUP.md** | Setup for GSC (and GA4) credentials and env vars. |

### Where to add or extend usage

| Area | Current behavior | How to leverage Search Console API |
|------|------------------|------------------------------------|
| **Automation 05 — Weekly SEO Intelligence** | Uses Ahrefs only for organic keywords/top pages. | **Add a GSC step**: call Search Analytics for `tldr.tech` (queries + pages) and merge with Ahrefs data. GSC is the source of truth for what Google actually shows; Ahrefs is estimates. Use `ai system/automations/lib/` or a small `gsc_api.py` that uses the same service account as `search_ranking_agent.py`. |
| **Automation 08 — Weekly CRO Audit** | Playwright crawl + Ahrefs traffic + CRO hypothesis. | **Add sitemap/coverage**: use the API to list sitemaps and (if available) coverage or URL inspection for the landing page list. Ensures “submitted to Search Console” and “no indexing issues” are part of the audit. Reference: [Query your search traffic](https://developers.google.com/webmaster-tools/search-console-api-original#query_your_search_traffic). |
| **seo_auditor.py** | Builds URL inventory by fetching `sitemap.xml` over HTTP and parsing `<loc>`. | **Optional GSC path**: use the API to [list sitemaps](https://developers.google.com/webmaster-tools/search-console-api-original#sitemaps) for the property and/or get submitted URLs. More reliable than scraping sitemap XML and aligns with what’s in Search Console. Keep current sitemap fetch as fallback when GSC isn’t configured. |
| **ai system/agents/seo-aeo/seo-audit-agent.md** | Same as above. | Same as above — reference the API for coverage and URL inspection. |

### Env / code you already have

- **GSC_SITE_URL** and **GOOGLE_APPLICATION_CREDENTIALS** (see `docs/GSC_GA4_SETUP.md`).
- **search_ranking_agent.py** already initializes `searchconsole` v1 with a service account; any new GSC script can reuse the same credentials and scopes (`webmasters.readonly`).

---

## 2. Pomelli by Google Labs

[Pomelli](https://labs.google.com/pomelli/about/) is an AI marketing tool (Google Labs / DeepMind) that:

- Analyzes a **website** to extract brand (colors, fonts, image style, tone).
- Generates **campaign ideas** and **marketing assets** (social, email, etc.) that match that brand.
- Supports **natural-language editing** and a **“photoshoot”** style for product images.

It’s a **product** (free beta in select countries), not an API in this workspace. Use it as a **manual or semi-manual input** into your flows.

### Where to leverage Pomelli

| Area | How to use Pomelli |
|------|--------------------|
| **Meta / paid creative agents** | **meta_creative_agent.py**, **ai system/agents/gtm team/marketing/paid ads/ad-creative-agent.md**, **ai system/agents/gtm team/marketing/paid ads/visual-creative-brief-agent.md**: add a note that for TLDR (or a client site), “Run Pomelli on [tldr.tech] to refresh brand extraction (colors, fonts, tone). Use output as reference for on-brand creative briefs and asset ideas.” Run Pomelli periodically and paste brand summary or example assets into context or into `commands/identity/` (e.g. a short `pomelli_brand_snapshot.md`) so agents stay on-brand. |
| **Content ideation / creative direction** | **content_ideation_agent.py**, **creative_direction_agent.py**: document that Pomelli’s “campaign ideas” and style can be used as inspiration for content briefs and visual direction. Option: add a step in **Automation 02 (Weekly Content Execution)** or content planning: “Optional: run Pomelli for tldr.tech and add this week’s campaign ideas into the content pipeline or briefs.” |
| **Automation 03 — Monthly Competitive Ads** | In the “creative brief” or “competitive brief” step, add: “Optional: use Pomelli (labs.google.com/pomelli) on tldr.tech to get updated on-brand campaign ideas and compare with competitor ad themes.” |
| **Landing page / CRO** | **landing_page_agent.py**, **cro_hypothesis_agent.py**, **Automation 08**: Pomelli’s site analysis can inform “on-brand” messaging and visual consistency for landing pages. Add to agent instructions: “For brand consistency, consider running Pomelli on the site and aligning headlines/CTAs with the extracted tone and style.” |

### No API (yet)

Pomelli is used via the web app. There is no public API in this repo. Integration is:

- **Document in agent/automation prompts** as an optional step.
- **Optionally** store outputs (e.g. brand snapshot, campaign ideas) in `commands/identity/` or `docs/content_briefs/` and reference them from scripts/agents.

---

## Summary

| Resource | Best used in | Action |
|----------|--------------|--------|
| **Search Console API** | 05 SEO Intelligence, 08 CRO Audit, seo_auditor.py, SEO audit agents | Add GSC steps (search analytics, sitemaps, URL inspection); document API in agent specs; reuse existing GSC credentials. |
| **Pomelli** | Meta/creative agents, content ideation, Automation 02/03, landing/CRO | Document as optional “run Pomelli on site, use output for brand and campaign ideas”; optionally store snapshots for agent context. |
