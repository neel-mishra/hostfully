# Ideal Customer Profile (ICP): Hostfully

Hostfully sells subscription software to vacation rental and hospitality operators. Growth, product, and GTM content should reflect **who** is buying (portfolio scale, geography, billing), **what** they subscribe to (PMP and Guidebooks adoption), **how customers expand or contract** (upgrades/downgrades), **how durable** revenue is (cohort retention, CLV), and **which channels** feed the funnel. This document is the single source for that segmentation.

---

## How this ICP was informed (Jan–Mar 2026 exports)

| Topic | Primary source (internal) |
| :--- | :--- |
| **Rolling signups by portfolio tier (A–E)** | `6. Customer Segmentation (Last 6 months) - Feb 2026.xlsx` → **`Segment analysis`** (latest full **Salesforce** cut in downloads; replaces Mar-only snapshot) |
| **Product attach (PMP + Guidebooks)** | `7. Product Mix - Feb 2026.xlsx` → **`Calculation`** |
| **Cohort retention (logo vs MRR)** | `8b` / `8c. Retention rate count|MRR - Feb 2026.xlsx` (same layout as prior months) |
| **Customer lifetime value & term** | `6. Customer Lifetime Value (last 48 months) - Jan 2026.xlsx` → **`36 months`** |
| **Average MRR at signup vs today** | `7d. Average MRR by segment - Jan 2026.xlsx` → **`for report`** |
| **Expansion / contraction (Nov–Jan window)** | `9. Upgrades & Downgrades - Jan 2026.xlsx` → **`calculations`** |
| **Acquisition by channel (last 12 months)** | `4a. Marketing Channels Summary last 12 months - Jan 2026.xlsx` → **`Lead Source matching`** (aggregated by **Channel**) |
| **Churn cases (support lens)** | `8. Churn - Jan 2026.xlsx` → **`Pivot`** (segment rollup) |
| **Executive narrative** | *Customer Acquisition Analysis and Recommendations* (Jan / Feb 2026 docx); *Copy of… January 2026* where cited internally |
| **CS / bird-segment view (optional)** | `Hostfully Customer Segmentation 2026_03.xlsx` (Egglets / Hatchlings / Ducks / Geese / Albatrosses)—aligns to **property scale**, parallel to A–E |

If a docx number disagrees with an **xlsx**, **xlsx wins**.

---

## 1. Segmentation axis: property portfolio size (at signup)

Accounts are grouped by **claimed number of PMP properties at signup** (cohorts **A–E**). Figures below are **last 6 months** of PMP signups (custom subscription types excluded per internal filters), from **`6. Customer Segmentation (Last 6 months) - Feb 2026.xlsx`** → **`Segment analysis`**.

| Cohort | Properties | Worldwide accounts | Worldwide MRR | US accounts | US MRR | US share of cohort (count / MRR) | Avg MRR (WW) | Monthly | Yearly |
| :--- | :--- | ---: | ---: | ---: | ---: | :--- | ---: | ---: | ---: |
| **A** | 1–4 | 289 | $33,175.98 | 234 | $26,877.00 | 81.0% / 81.0% | $114.80 | 212 | 72 |
| **B** | 5–15 | 116 | $21,919.59 | 70 | $13,756.76 | 60.3% / 62.8% | $188.96 | 98 | 17 |
| **C** | 16–30 | 37 | $11,532.91 | 13 | $3,800.50 | 35.1% / 33.0% | $311.70 | 34 | 2 |
| **D** | 31–49 | 15 | $6,526.58 | 8 | $3,507.98 | 53.3% / 53.7% | $435.11 | 12 | 3 |
| **E** | 50+ | 13 | $9,643.50 | 5 | $4,474.00 | 38.5% / 46.4% | $741.81 | 10 | 0 |
| **All** | — | **470** | **$82,798.56** | **330** | **$52,416.24** | 70.2% / 63.3% | **$176.17** | **366** | **94** |

**Share of last-6-month signups (count):** A ~61.5%, B ~24.7%, C ~7.9%, D ~3.2%, E ~2.8%.  
**Share of last-6-month WW MRR:** A ~40%, B ~26%, C ~14%, D ~8%, E ~12% (rounded).

**Billing mix (subscription interval, all segments):** **366** monthly vs **94** yearly (**~78%** / **~20%**; remainder rounding)—same **`Segment analysis`** row.

---

## 2. Geography (customer count and MRR)

**`Segment analysis`** country pivot (Feb 2026 export):

- **United States:** **330 / 470** accounts (**~70%**), **~63%** of WW MRR (**$52,416 / $82,799**)—**All segments** row.
- **By account count (Count %):** US **~72.7%**, Great Britain **~4.0%**, Canada **~3.5%**, Mexico **~2.6%**, UAE **~2.4%**, Spain **~1.5%**, France **~1.5%**, Portugal **~1.1%**, South Africa **~0.9%**, Costa Rica **~0.9%**, Switzerland **~0.9%**, etc.
- **By MRR (MRR %):** US **~66.3%**, Spain **~4.9%**, Mexico **~3.0%**, Great Britain **~4.0%**, Canada **~3.6%**, UAE **~2.7%**, Portugal **~1.5%**, Australia **~1.7%**, etc.—use **MRR %** when discussing revenue concentration.

---

## 3. Product footprint (PMP + Guidebooks)

From **`7. Product Mix - Feb 2026.xlsx`** → **`Calculation`**: among **2,211** Property Management Platform clients, **754** also use Guidebooks (**34%** of PMP). Those **754** are **36%** of all **2,078** Guidebook clients. **PMP-first** remains the default land; **PMP + Guidebooks** signals expansion and guest-experience depth.

---

## 4. Lifetime value and MRR drift (Jan 2026 cuts)

**Customer lifetime value (36-month view, blended other recurring revenue in model):**  
`6. Customer Lifetime Value (last 48 months) - Jan 2026.xlsx` → **`36 months`**

| Segment | Accounts (count) | Avg ORBI MRR | Avg other recurring | Avg term (mo) | **CLV** |
| :--- | ---: | ---: | ---: | ---: | ---: |
| A) 1–4 | 1,054 | $155.97 | $66.98 | 19 | **$4,322** |
| B) 5–15 | 567 | $261.88 | $112.60 | 22 | **$8,155** |
| C) 16–30 | 219 | $396.07 | $170.33 | 21 | **$11,620** |
| D) 31–49 | 53 | $487.51 | $209.66 | 23 | **$16,144** |
| E) 50+ | 64 | $760.82 | $327.13 | 24 | **$25,886** |
| **Total / blend** | **1,957** | **$242.28** | **$104.14** | **20** | **~$7,288** (blended total row) |

**Current vs signup MRR (Jan 2026):** `7d. Average MRR by segment - Jan 2026.xlsx` — blended **avg first PMP MRR** **$196.90** vs **avg current PMP MRR** **$167.30** across **451** accounts in drilldown (mix and downgrades pull **current** below **signup** on average).

---

## 5. Expansion and contraction (recent window)

**`9. Upgrades & Downgrades - Jan 2026.xlsx`** → **`calculations`** (expansion tracking ~ **Nov 2025 – Jan 2026** in raw):

- **A) 1–4:** ~**62.8%** upgrades, ~**33.0%** no change, ~**4.3%** downgrades (by customer rows in pivot).
- **B) 5–15:** ~**47.9%** upgrades, ~**44.2%** no change, ~**7.9%** downgrades.
- **C) 16–30:** ~**47.9%** upgrades, ~**33.3%** no change, ~**18.8%** downgrades.
- **D) 31–49:** ~**60%** upgrades, ~**12%** no change, ~**28%** downgrades (small **n**).
- **E) 50+:** ~**66%** upgrades, ~**14%** no change, ~**20%** downgrades (small **n**).

**Interpretation:** Larger portfolios show **more upgrade motion** but also **non-trivial downgrades**—messaging should pair **expansion** with **risk-aware** success practices.

---

## 6. Marketing channels (closed-won signups, last 12 months)

**`4a. Marketing Channels Summary last 12 months - Jan 2026.xlsx`** → **`Lead Source matching`**, rolled up by mapped **Channel** (Signups / MRR Generated):

| Channel (rollup) | Signups (12m) | MRR Generated (12m) |
| :--- | ---: | ---: |
| Website chat | 333 | $722,274 |
| Website form | 263 | $602,137 |
| Affiliate or Referral | 482 | $342,222 |
| Recorded demos | 108 | $230,863 |
| Thought Leadership / Education | 88 | $135,659 |
| Cold Calls / Lists | 39 | $116,954 |
| Advertising | 47 | $79,017 |
| Other organic sources | 45 | $64,764 |
| Events | 11 | $36,683 |
| Accelerator | 2 | $2,993 |

**Note:** MRR Generated reflects **won opportunity amounts** in the export, not ARR—use for **relative channel strength**, not GAAP revenue.

**Opportunities closed won (product split, same workbook `Opportunities` sheet):** Lead sources such as **Qualified.com**, **Hostfully Website**, **Existing Client**, **Livestorm** appear with splits across **PMS**, **GB**, **PMS + GB**, **PMS + Devices**—use when writing **product-specific** campaigns.

---

## 7. Retention (12-month cohorts)

**Definition:** Clients who subscribed in the **last 12 months**, cohorts by **subscription start month**; retention = **% still active** at months 1–4 after start.

- **Logo / count:** **`8b. Retention rate count - Feb 2026.xlsx`** — sheets **`Count (all segments)`**, **`Count (1-4)`**, … **`Count (50+)`**.
- **MRR-weighted:** **`8c. Retention rate MRR - Feb 2026.xlsx`** — parallel sheet names; **MRR** retention can diverge from **logo** when customers **downgrade**.

**Reading tips:** Prefer **mature cohorts** (e.g. mid-2025) for stable M4 reads; **E) 50+** has **small n**; label **logo vs MRR** explicitly.

---

## 8. Parallel: Customer Success “bird” segments (Mar 2026 workbook)

**`Hostfully Customer Segmentation 2026_03.xlsx`** uses branded tiers (**Egglets, Hatchlings, Ducks, Geese, Albatrosses**) mapped to **property scale** (same spirit as A–E). Example **all-time** base row: **~2,063** active PMP clients, **~$504,927** active MRR, **~245** avg MRR, **29,842** properties (**`All time`** sheet). Use this file for **CS / retention storytelling**; use **Section 1** table for **Salesforce cohort** consistency in GTM copy.

---

## 9. Operator personas (by tier)

- **A — Small portfolio (1–4):** Highest volume, lower avg MRR, US-heavy; fast onboarding, Starter/Pro.
- **B — Growing (5–15):** Large MRR share; automation + inbox scale; strong upgrade motion.
- **C–D — Mid-scale (16–49):** Higher avg MRR; reporting and workflow control; watch downgrade rate.
- **E — Large (50+):** Highest avg MRR and CLV; sales-led; **small-n** in cohort retention.

---

## 10. Anti-ICP

- Operators with **no** operational volume expecting full PMS ROI; **consumer** travel plays without managed inventory; **one-off** tests with no implementation commitment.
- Do not quote **E) 50+** or **D) 31–49** percentages without noting **sample size** or cohort maturity.

---

### AI Agent Context Rule

1. **Portfolio tier (A–E)** + proof (CLV, MRR, upgrade rate) from this doc.
2. **Region:** US vs international; count vs MRR emphasis for geo.
3. **Product scope:** PMP-only vs **PMP + Guidebooks**; devices when relevant (`Opportunities` split).
4. **Retention:** State **logo (`8b`)** vs **MRR (`8c`)** explicitly.
5. **Channels:** Match campaign to **Website / referral / demo / content** strength from §6.

---

### Data provenance

**Last refreshed:** March 30, 2026 (synthesis of Jan–Feb 2026 xlsx + Mar 2026 CS workbook + acquisition memos).

**Primary files:**  
`6. Customer Segmentation (Last 6 months) - Feb 2026.xlsx`; `7. Product Mix - Feb 2026.xlsx`; `8b`/`8c` Retention **Feb 2026**; `6. Customer Lifetime Value (last 48 months) - Jan 2026.xlsx`; `7d. Average MRR by segment - Jan 2026.xlsx`; `9. Upgrades & Downgrades - Jan 2026.xlsx`; `4a. Marketing Channels Summary last 12 months - Jan 2026.xlsx`; `8. Churn - Jan 2026.xlsx`; `Hostfully Customer Segmentation 2026_03.xlsx`; Customer Acquisition Analysis docx (Jan/Feb 2026).  
Do not paste **account-level** rows into customer-facing copy.
