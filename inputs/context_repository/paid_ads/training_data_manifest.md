# Training data manifest (Mar 2026 onward)

This file tracks where “training” (retrieval context) inputs were pulled from and where derived artifacts were written.

## Live pulls executed (this session)

### Meta (ad-level, with placement/device breakdowns)

- Account: `act_602183263243751` (Hostfully)
- Date range: `2026-03-01` → `2026-03-25`
- Output: large JSON (includes daily breakdown + conversion action mapping)
  - Local path (agent output): `/Users/neelmishra/.cursor/projects/Users-neelmishra-antigravity-synthetic-growth-Hostfully/agent-tools/dc1c3ec0-7235-4c2e-b02e-823d1514e36d.txt`

### Google Ads (time breakdown + RSA asset view)

- Customer: `2565189582`
- Lookback: 30 days (contains some pre-Mar rows; we filter to `>= 2026-03-01`)
- Outputs:
  - time breakdown (date/week/month): returned as tool output (not persisted)
  - RSA asset performance (headlines/descriptions/images): `/Users/neelmishra/.cursor/projects/Users-neelmishra-antigravity-synthetic-growth-Hostfully/agent-tools/9e308e3c-5e92-437c-a3ee-9f0db14fbd0d.txt`
  - sitelink performance: pulled via GAQL query (tool `get_sitelink_performance` currently errors due to an unrecognized field)

## Derived context outputs (to be populated after Salesforce ROI joins)

- Meta winners: `docs/context_repository/paid_ads/winning_angles/meta_mar2026_onward.md`
- Google winners: `docs/context_repository/paid_ads/winning_angles/google_mar2026_onward.md`

