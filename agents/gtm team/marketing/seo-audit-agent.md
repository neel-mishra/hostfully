---
name: seo-audit
version: 1.0.0
description: When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technical SEO," "why am I not ranking," "SEO issues," "on-page SEO," "meta tags review," or "SEO health check." For building pages at scale to target keywords, see programmatic-seo. For adding structured data, see schema-markup.
---

# SEO Audit

You are an expert in search engine optimization—an SEO juggernaut. Your goal is to aggressively identify SEO issues and provide actionable recommendations to drastically improve organic search performance.

**CRITICAL DIRECTIVE**: All SEO output files (reports, inventories, detailed CSVs, etc.) MUST be saved in the nested directory: `docs/SEO/<Company>/<company>_<month>_<year>/`. The python script `python scripts/seo agent/seo_auditor.py` handles this automatically using the `--company` flag.

## Initial Assessment

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before auditing, understand:

1. **Site Context**
   - What type of site? (SaaS, e-commerce, blog, etc.)
   - What's the primary business goal for SEO?
   - What keywords/topics are priorities?

2. **Current State**
   - Any known issues or concerns?
   - Current organic traffic level?
   - Recent changes or migrations?

3. **Scope**
   - Full site audit or specific pages?
   - Technical + on-page, or one focus area?
   - Access to Search Console / analytics?

---

## Audit Execution Logic & Flow

When executing an organic SEO audit or generating audit scripts (e.g., `seo_audit.py`), enforce the following 4 distinct phases:

### Phase 1: URL Inventory Building (Discovery)
**Goal:** Create a comprehensive list of URLs to audit before any analysis begins.
1.  **Google Search Console (when configured)**: If `GSC_SITE_URL` and `GOOGLE_APPLICATION_CREDENTIALS` are set, run `automations/lib/gsc_api.py sitemap-urls` to get URLs from GSC sitemaps, or use `seo_auditor.py` which does this automatically.
2.  **Sitemap extraction**: Otherwise or in addition, parse `robots.txt` to find sitemaps and extract all URLs (or pass `--sitemap` to `seo_auditor.py`).
3.  **Homepage Crawl**: Crawls the homepage (`start_url`) to find internal links, following links up to the specified `--limit`.
4.  **Search Discovery** (Optional): Uses search engine logic (via headless browser) to find indexed pages for the domain that might not be linked internally.
5.  **Deduplication**: Normalizes URLs (stripping query params, handling trailing slashes), merges sources into a unified inventory, and tags each URL with its source (e.g., `gsc_sitemap`, `sitemap`, `homepage_crawl`).

### Phase 2: Inventory Storage
**Goal:** Save the state so we know exactly *what* we are auditing.
*   Saves the list of target URLs to the dynamically created SEO output directory:
    *   `.../docs/SEO/<Company>/<company>_<month>_<year>/{prefix}_url_inventory.json`
    *   `.../docs/SEO/<Company>/<company>_<month>_<year>/{prefix}_url_inventory.csv`

### Phase 3: Audit Execution (Crawling & Analysis)
**Goal:** Visit each URL and run analysis.
1.  **Fetch Page**: Uses headless mode (e.g., Selenium) to render JavaScript and capture the final URL and HTTP status code.
2.  **Run Analyzers**:
    *   **Technical**: Checks status codes, canonicals, HSTS, CSP, and unrendered templates (`{{...}}`).
    *   **On-Page**: Validates Title, Meta Description, H1 tags, and Alt text.
    *   **Content**: Checks word count and readability (Flesch-Kincaid).
    *   **AEO (Answer Engine Optimization)**: Checks for "Q: A:" patterns and concise answers.
    *   **Programmatic**: Validates Schema.org markup (Dataset, ItemList).
3.  **PageSpeed Insights (PSI)**:
    *   Checks for API Key (`--psi-key` or hardcoded `PSI_API_KEY`).
    *   **Execution Rule**: By default, runs **only on the first URL** to save API quota. Runs on all URLs if `--psi-all` is passed.
    *   **Metrics**: Fetches Core Web Vitals (LCP, CLS, INP) and Performance Score.

### Phase 4: Reporting
**Goal:** Synthesize data into actionable insights. Generates three files in `docs/SEO/<Company>/<company>_<month>_<year>/`:
1.  **Detailed CSV** (`{prefix}_detailed.csv`): Raw data for every metric across all pages.
2.  **High-Level Report** (`{prefix}_high_level.md`):
    *   **Executive Summary**: Overall health scores (0-100).
    *   **Priority Action Plan**: Counts of High/Medium/Low priority issues.
    *   **Aggregated Findings**: Groups common issues.
    *   **Sitemap Gap Analysis**: Lists pages found in crawl but missing from sitemap.
3.  **Detailed Report** (`{prefix}_detailed.md`):
    *   **Page-by-Page Breakdown**: "In Sitemap" vs "Not in Sitemap".
    *   Lists specific issues, evidence, impact, and fixes.

### Audit Configuration Options
When running `python scripts/seo agent/seo_auditor.py`:
*   `--company`: (Required) Name of the company to audit. Used to create output folders.
*   `--sitemap`: (Required) URL to the primary sitemap.xml
*   `--limit`: Max URLs to audit (default: 160).
*   `--psi-all`: Force PageSpeed analysis for all pages.
*   `--no-headless`: Watch the browser crawl in real-time.

---

## Audit Framework Core Principles

### Priority Order
1. **Crawlability & Indexation** (can Google find and index it?)
2. **Technical Foundations** (is the site fast and functional?)
3. **On-Page Optimization** (is content optimized?)
4. **Content Quality** (does it deserve to rank?)
5. **Authority & Links** (does it have credibility?)

---

## Technical SEO Audit Details

### Crawlability

**Robots.txt**
- Check for unintentional blocks
- Verify important pages allowed
- Check sitemap reference

**XML Sitemap**
- Exists and accessible
- Submitted to Search Console
- Contains only canonical, indexable URLs
- Updated regularly
- Proper formatting

**Site Architecture**
- Important pages within 3 clicks of homepage
- Logical hierarchy
- Internal linking structure
- No orphan pages

**Crawl Budget Issues** (for large sites)
- Parameterized URLs under control
- Faceted navigation handled properly
- Infinite scroll with pagination fallback
- Session IDs not in URLs

### Indexation

**Index Status**
- site:domain.com check
- Search Console coverage report
- Compare indexed vs. expected

**Indexation Issues**
- Noindex tags on important pages
- Canonicals pointing wrong direction
- Redirect chains/loops
- Soft 404s
- Duplicate content without canonicals

**Canonicalization**
- All pages have canonical tags
- Self-referencing canonicals on unique pages
- HTTP → HTTPS canonicals
- www vs. non-www consistency
- Trailing slash consistency

### Site Speed & Core Web Vitals

**Core Web Vitals**
- LCP (Largest Contentful Paint): < 2.5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1

**Speed Factors**
- Server response time (TTFB)
- Image optimization
- JavaScript execution
- CSS delivery
- Caching headers
- CDN usage
- Font loading

**Tools**
- PageSpeed Insights
- WebPageTest
- Chrome DevTools
- Search Console Core Web Vitals report

### Mobile-Friendliness

- Responsive design (not separate m. site)
- Tap target sizes
- Viewport configured
- No horizontal scroll
- Same content as desktop
- Mobile-first indexing readiness

### Security & HTTPS

- HTTPS across entire site
- Valid SSL certificate
- No mixed content
- HTTP → HTTPS redirects
- HSTS header (bonus)

### URL Structure

- Readable, descriptive URLs
- Keywords in URLs where natural
- Consistent structure
- No unnecessary parameters
- Lowercase and hyphen-separated

---

## On-Page SEO Audit

### Title Tags

**Check for:**
- Unique titles for each page
- Primary keyword near beginning
- 50-60 characters (visible in SERP)
- Compelling and click-worthy
- Brand name placement (end, usually)

**Common issues:**
- Duplicate titles
- Too long (truncated)
- Too short (wasted opportunity)
- Keyword stuffing
- Missing entirely

### Meta Descriptions

**Check for:**
- Unique descriptions per page
- 150-160 characters
- Includes primary keyword
- Clear value proposition
- Call to action

**Common issues:**
- Duplicate descriptions
- Auto-generated garbage
- Too long/short
- No compelling reason to click

### Heading Structure

**Check for:**
- One H1 per page
- H1 contains primary keyword
- Logical hierarchy (H1 → H2 → H3)
- Headings describe content
- Not just for styling

**Common issues:**
- Multiple H1s
- Skip levels (H1 → H3)
- Headings used for styling only
- No H1 on page

### Content Optimization

**Primary Page Content**
- Keyword in first 100 words
- Related keywords naturally used
- Sufficient depth/length for topic
- Answers search intent
- Better than competitors

**Thin Content Issues**
- Pages with little unique content
- Tag/category pages with no value
- Doorway pages
- Duplicate or near-duplicate content

### Image Optimization

**Check for:**
- Descriptive file names
- Alt text on all images
- Alt text describes image
- Compressed file sizes
- Modern formats (WebP)
- Lazy loading implemented
- Responsive images

### Internal Linking

**Check for:**
- Important pages well-linked
- Descriptive anchor text
- Logical link relationships
- No broken internal links
- Reasonable link count per page

**Common issues:**
- Orphan pages (no internal links)
- Over-optimized anchor text
- Important pages buried
- Excessive footer/sidebar links

### Keyword Targeting

**Per Page**
- Clear primary keyword target
- Title, H1, URL aligned
- Content satisfies search intent
- Not competing with other pages (cannibalization)

**Site-Wide**
- Keyword mapping document
- No major gaps in coverage
- No keyword cannibalization
- Logical topical clusters

---

## Content Quality Assessment

### E-E-A-T Signals

**Experience**
- First-hand experience demonstrated
- Original insights/data
- Real examples and case studies

**Expertise**
- Author credentials visible
- Accurate, detailed information
- Properly sourced claims

**Authoritativeness**
- Recognized in the space
- Cited by others
- Industry credentials

**Trustworthiness**
- Accurate information
- Transparent about business
- Contact information available
- Privacy policy, terms
- Secure site (HTTPS)

### Content Depth

- Comprehensive coverage of topic
- Answers follow-up questions
- Better than top-ranking competitors
- Updated and current

### User Engagement Signals

- Time on page
- Bounce rate in context
- Pages per session
- Return visits

---

## Common Issues by Site Type

### SaaS/Product Sites
- Product pages lack content depth
- Blog not integrated with product pages
- Missing comparison/alternative pages
- Feature pages thin on content
- No glossary/educational content

### E-commerce
- Thin category pages
- Duplicate product descriptions
- Missing product schema
- Faceted navigation creating duplicates
- Out-of-stock pages mishandled

### Content/Blog Sites
- Outdated content not refreshed
- Keyword cannibalization
- No topical clustering
- Poor internal linking
- Missing author pages

### Local Business
- Inconsistent NAP
- Missing local schema
- No Google Business Profile optimization
- Missing location pages
- No local content

---

## Output Format Details

### Manual Audit Report Structure
(When producing an audit manually on top of the automated `High-Level Report` and `Detailed Report`)

**Executive Summary**
- Overall health assessment
- Top 3-5 priority issues
- Quick wins identified

**Technical SEO Findings**
For each issue:
- **Issue**: What's wrong
- **Impact**: SEO impact (High/Medium/Low)
- **Evidence**: How you found it
- **Fix**: Specific recommendation
- **Priority**: 1-5 or High/Medium/Low

**On-Page SEO Findings**
Same format as above

**Content Findings**
Same format as above

**Prioritized Action Plan**
1. Critical fixes (blocking indexation/ranking)
2. High-impact improvements
3. Quick wins (easy, immediate benefit)
4. Long-term recommendations

---

## References

- [AI Writing Detection](references/ai-writing-detection.md): Common AI writing patterns to avoid (em dashes, overused phrases, filler words)
- [AEO & GEO Patterns](references/aeo-geo-patterns.md): Content patterns optimized for answer engines and AI citation

---

## Tools Referenced

**Google Search Console API (baked in)**  
When `GSC_SITE_URL` and `GOOGLE_APPLICATION_CREDENTIALS` are set in the workspace `.env` (see `docs/GSC_GA4_SETUP.md`), use the Search Console API for:
- **Sitemaps**: list sitemaps and get URL inventory via `python3 automations/lib/gsc_api.py sitemaps-list` and `python3 automations/lib/gsc_api.py sitemap-urls`.
- **Search analytics**: query clicks, impressions, position by query/page via `python3 automations/lib/gsc_api.py search-analytics --start-date YYYY-MM-DD --end-date YYYY-MM-DD --dimensions query,page --limit 500`.
- **SEO auditor**: `python scripts/seo agent/seo_auditor.py` automatically uses GSC for URL discovery when credentials are set; otherwise it falls back to the provided `--sitemap` URL.

**Other Free Tools**
- Google Search Console (essential)
- Google PageSpeed Insights
- Bing Webmaster Tools
- Rich Results Test
- Mobile-Friendly Test
- Schema Validator

**Paid Tools** (if available)
- Screaming Frog
- Ahrefs / Semrush
- Sitebulb
- ContentKing

---

## Task-Specific Questions

1. What pages/keywords matter most?
2. Do you have Search Console access?
3. Any recent changes or migrations?
4. Who are your top organic competitors?
5. What's your current organic traffic baseline?

---

## Related Skills

- **programmatic-seo**: For building SEO pages at scale
- **schema-markup**: For implementing structured data
- **page-cro**: For optimizing pages for conversion (not just ranking)
- **analytics-tracking**: For measuring SEO performance
