# Google Search Console & GA4 Setup

**One set of credentials** powers all Google Search Console usage in this workspace. Set `GSC_SITE_URL` and `GOOGLE_APPLICATION_CREDENTIALS` in the workspace `.env` (or in the Cloud Agent Environment for automations); every script and automation that uses GSC will then use live data. If either is unset, they fall back to mock data or sitemap-only behavior.

**Consumers of GSC credentials:**
- **search_ranking_agent.py** — search analytics (query/page performance)
- **automations/lib/gsc_api.py** — search-analytics, sitemaps-list, sitemap-urls (used by automations 05, 08 and by seo_auditor)
- **seo_auditor.py** — URL inventory from GSC sitemaps when credentials are set
- **Automation 05** (Weekly SEO Intelligence) — Step 2b pulls GSC search analytics
- **Automation 08** (Weekly CRO Audit) — Step 3b pulls GSC search analytics and sitemaps
- **SEO audit agents** (gtm + seo-aeo) — Phase 1 and Tools reference the API and gsc_api.py

---

## 1. Google Cloud project & APIs

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create or select a project (e.g. "TLDR Analytics").
3. Enable APIs:
   - **Search Console API**: [Enable](https://console.cloud.google.com/apis/library/searchconsole.googleapis.com)
   - **Google Analytics Data API**: [Enable](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com)

---

## 2. Service account (for both GSC and GA4)

1. In Cloud Console: **IAM & Admin** → **Service accounts** → **Create service account**.
2. Name it (e.g. `tldr-analytics-reader`), then **Create and continue**.
3. Skip optional steps; click **Done**.
4. Open the new service account → **Keys** → **Add key** → **Create new key** → **JSON** → save the file.
5. Move the JSON into your project (e.g. `TLDR/credentials/google-service-account.json`) and **do not commit it** (add to `.gitignore`).

---

## 3. Search Console (GSC)

1. In [Search Console](https://search.google.com/search-console), add the property for your site (e.g. `https://tldr.tech` or `sc-domain:tldr.tech`).
2. In Search Console: **Settings** → **Users and permissions** → **Add user**.
3. Add the **service account email** (e.g. `tldr-analytics-reader@your-project.iam.gserviceaccount.com`) with **Full** (or at least “Read”) permission.
4. In your `.env` set:
   - **GSC_SITE_URL** = the exact property URL (e.g. `https://tldr.tech` or `sc-domain:tldr.tech`).
   - **GOOGLE_APPLICATION_CREDENTIALS** = absolute path to the service account JSON (e.g. `/Users/you/.../TLDR/credentials/google-service-account.json`).

---

## 4. GA4

1. In [Google Analytics](https://analytics.google.com/), open your GA4 property.
2. **Admin** (gear) → **Property access management** → **Add users**.
3. Add the **service account email** with **Viewer** (or “Analyst” if you prefer).
4. Get the **Property ID**: Admin → Property settings → **Property ID** (numeric, e.g. `412345678`).
5. In your `.env` set:
   - **GA4_PROPERTY_ID** = that numeric ID (e.g. `412345678`).
   - **GOOGLE_APPLICATION_CREDENTIALS** = same path as in step 3 (one JSON for both GSC and GA4).

---

## 5. .env summary

```bash
# Optional — for live GSC/GA4 data (scripts use mock data if unset)
GSC_SITE_URL=https://tldr.tech
GA4_PROPERTY_ID=412345678
GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/google-service-account.json
```

- **GSC**: `GSC_SITE_URL` + `GOOGLE_APPLICATION_CREDENTIALS` — used by search_ranking_agent.py, gsc_api.py, seo_auditor.py, automations 05 and 08, and SEO audit agents.
- **GA4**: `GA4_PROPERTY_ID` + `GOOGLE_APPLICATION_CREDENTIALS` — used by traffic_analytics_agent.py.
- If any are missing, the scripts and automations still run and use mock data or fallbacks.
