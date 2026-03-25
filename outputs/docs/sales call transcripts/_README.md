# Sales Call Transcripts

Store advertiser sales call transcripts here for analysis by the **Sales Call Transcript Analyzer Agent**.

## Supported Formats

- `.md` — Markdown transcripts (preferred)
- `.txt` — Plain text transcripts
- `.json` — Structured exports from Gong, Fireflies, Otter.ai

## Naming Convention

```
{YYYY-MM-DD}_{advertiser_name}_{call_type}.{ext}
```

Examples:
- `2026-03-01_anthropic_discovery-call.md`
- `2026-02-15_shopify_renewal-review.md`
- `2026-01-20_plaid_qbr-call.json`

## Call Types

- `discovery-call` — Initial exploratory call
- `pitch` — Formal advertising pitch
- `renewal-review` — Contract renewal discussion
- `qbr-call` — Quarterly business review call
- `check-in` — Ad-hoc relationship check-in
- `objection-handling` — Follow-up addressing concerns

## How Transcripts Are Used

The Sales Call Transcript Analyzer reads all files in this folder and extracts:
- Objections raised by prospects/advertisers
- Competitor mentions (LinkedIn Ads, Meta, Paved, etc.)
- Budget signals and pricing discussions
- Deal stage indicators
- Feature requests and feedback

Output goes to `docs/sales_assets/call_analysis/`.
