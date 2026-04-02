# Paid Ads Training Utilities

Utilities to ingest Salesforce exports and produce intermediate tables for building the paid-ads **winning angles** library.

## Salesforce ingest (Mar 2026 onward)

```bash
python "ai system/python scripts/paid-ads_training/salesforce_ingest.py" \
  --leads /path/to/salesforce_leads.xlsx \
  --opps /path/to/salesforce_opportunities.xlsx
```

Outputs (ignored by git): `outputs/training_data/paid_ads/salesforce/tables/`

