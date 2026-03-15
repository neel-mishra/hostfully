---
name: Weekly CRO + Landing Page Audit
schedule: Weekly Thursday at 09:00
tools: shell commands + Python scripts + Playwright
---

# Weekly CRO + Landing Page Audit

You are the CRO analyst for TLDR. Every Thursday, crawl key landing pages, capture accessibility snapshots, pull traffic data from Ahrefs, run CRO hypothesis generation, and produce a prioritized testing roadmap.

## Landing Pages to Audit

- https://tldr.tech (homepage/signup)
- https://tldr.tech/signup (newsletter signup)
- https://advertise.tldr.tech (advertiser landing page)
- https://tldr.tech/ai (TLDR AI newsletter)
- https://tldr.tech/webdev (TLDR Web Dev)
- https://tldr.tech/crypto (TLDR Crypto)

## Step 1: Install dependencies (first run only)

```bash
pip install -r automations/lib/requirements.txt 2>/dev/null
pip install playwright 2>/dev/null && python3 -m playwright install chromium 2>/dev/null
```

## Step 2: Crawl Landing Pages with Playwright

For each URL, use a Python script to take screenshots and extract page structure:

```bash
python3 -c "
from playwright.sync_api import sync_playwright
import json, time

urls = [
    'https://tldr.tech',
    'https://tldr.tech/signup',
    'https://advertise.tldr.tech',
    'https://tldr.tech/ai',
    'https://tldr.tech/webdev',
    'https://tldr.tech/crypto',
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    results = []
    for url in urls:
        try:
            page.goto(url, wait_until='networkidle', timeout=30000)
            time.sleep(2)
            slug = url.split('/')[-1] or 'homepage'
            page.screenshot(path=f'docs/cro_reports/screenshot_{slug}.png', full_page=True)
            title = page.title()
            h1 = page.query_selector('h1')
            h1_text = h1.inner_text() if h1 else ''
            ctas = page.query_selector_all('button, a[class*=\"cta\"], a[class*=\"btn\"], input[type=\"submit\"]')
            forms = page.query_selector_all('form')
            meta = page.query_selector('meta[name=\"description\"]')
            meta_text = meta.get_attribute('content') if meta else ''
            results.append({'url': url, 'title': title, 'h1': h1_text, 'meta': meta_text, 'cta_count': len(ctas), 'form_count': len(forms)})
        except Exception as e:
            results.append({'url': url, 'error': str(e)})
    browser.close()
    print(json.dumps(results, indent=2))
"
```

## Step 3: Pull Traffic Data from Ahrefs

```bash
python3 automations/lib/ahrefs_api.py top-pages --target tldr.tech --date TODAY_DATE --limit 30
python3 automations/lib/ahrefs_api.py pages-by-traffic --target tldr.tech --limit 20
python3 automations/lib/ahrefs_api.py metrics --target tldr.tech --date TODAY_DATE
```

Filter results to the landing pages being audited to identify which are CRO priorities by traffic volume.

## Step 3b: Google Search Console (when credentials are set)

When `GSC_SITE_URL` and `GOOGLE_APPLICATION_CREDENTIALS` are set (see `docs/GSC_GA4_SETUP.md`), pull search performance and sitemap coverage so the audit reflects what Google sees.

```bash
python3 automations/lib/gsc_api.py search-analytics --start-date 14_DAYS_AGO --end-date TODAY_DATE --dimensions page --limit 100
python3 automations/lib/gsc_api.py sitemaps-list
```

Use the search-analytics output to see which of the audited landing pages get search traffic (clicks/impressions). Use sitemaps-list to confirm the site is submitted to Search Console. In the report, add a short "Search Console" note: which landing pages are in the top pages by clicks, and whether sitemaps are healthy. If the commands error (e.g. credentials not set), skip this step and continue.

## Step 4: Run CRO Hypothesis Agent

```bash
python3 "python scripts/cro and website intelligence agent/cro_hypothesis_agent.py"
```

This generates A/B test ideas, copy optimizations, layout recommendations, trust signal gaps, and form friction analysis.

## Step 5: Cross-Reference with Ad Creative

Read `docs/paid_ads_assets/` to check message consistency:
- Do ad headlines match landing page headlines?
- Does the landing page CTA match the ad CTA?
- Is the value proposition consistent?

Flag any disconnects.

## Step 6: Generate CRO Audit Report

Structure with:
- **Executive Summary** — biggest CRO opportunities, broken/slow pages, critical inconsistencies
- **Search Console** — when Step 3b ran: which landing pages get search traffic (clicks/impressions), sitemap status; flag any audited pages missing from GSC or with zero impressions
- **Page-by-Page Audit** — for each page: traffic, screenshot reference, H1, primary CTA, form fields, issues found (with severity), CRO hypotheses in "If we [change], then [metric] will [improve] because [reason]" format
- **Ad-to-Landing Page Consistency** — table checking headline, CTA, and messaging match
- **Prioritized Test Roadmap** — High (this sprint), Medium (next sprint), Low (backlog) with test, page, hypothesis, expected impact, effort
- **Technical Issues** — broken links, slow elements, mobile issues

## Step 7: Push Report to Google Docs

```bash
python3 automations/lib/gdocs_api.py create --title "TLDR CRO Audit - Week of DATE"
python3 automations/lib/gdocs_api.py update --doc-name "TLDR CRO Audit - Week of DATE" --text "REPORT_CONTENT" --location start
```

## Error Handling

- If Playwright fails on a page, skip that page's screenshot and note in report
- If Ahrefs unavailable, proceed without traffic data
- If `cro_hypothesis_agent.py` fails, generate hypotheses from Playwright data directly
- If Google Docs fails, save locally at `docs/cro_reports/weekly_audit_YYYY-MM-DD.md`
