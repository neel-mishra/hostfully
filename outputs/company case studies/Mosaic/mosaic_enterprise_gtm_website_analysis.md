# Mosaic Website Analysis: Messaging, ICP Objections, and Conversion Surfaces

Purpose: turn the scraped Mosaic web context into a usable "message map" for growth execution. This is not a redesign request; it is a mapping of:
* what Mosaic already claims well,
* what objections those claims resolve for B2C and B2B,
* and which conversion surfaces should capture intent.

---

## 1. Scraped Mosaic context (what we can ground on)

### `https://mosaic.so/enterprise`
Key claims:
* Organization-wide access control: RBAC, shared workspaces, centralized asset library
* Activity and audit logs
* Integrations:
  * MAM/storage integration (auto-ingest from cloud storage, push completed edits back to DAM)
  * NLE export/roundtrip: export timeline XML to Premiere Pro, DaVinci Resolve, Final Cut Pro
* Custom automations:
  * full API access
  * event-driven triggers
  * custom workflows (white-glove implementation)
* Security/compliance:
  * SOC 2 Type II positioning
  * Google Cloud infrastructure
  * zero data retention / ephemeral storage option
  * no training on customer data
* Outcome metrics:
  * time saved: 40 hrs/week on average
  * content output: 10x more videos produced
  * videos processed: 500k+ and counting

Conversion surfaces present:
* `Book a Demo`
* `Get Started` (primary entry for creators)

### `https://mosaic.so/product`
Key claims:
* Infinite interactive canvas (node-based workflow building, parallel edits, timeline editor)
* Multimodal visual understanding (concepts, actions, emotions, shot types, spoken word)
* Agentic editing examples (rough cut, prompt-based generation, visual intelligence)
* Exports and integration readiness (timeline XML into professional tools)

Conversion surfaces present:
* `Book a Demo` (for teams)
* `Get Started` (for creators)

### `https://mosaic.so/product/automation`
Key claims:
* "Your ContentFactory" positioning: build pipelines that run on autopilot
* Event-driven triggers and batch processing
* Automated delivery and notifications (email/Slack/webhooks)
* Explicit link to API and enterprise automation capabilities

Outcome metrics present on the page:
* time saved 40 hrs/week
* content output 10x more
* videos processed 500k+

### `https://mosaic.so/templates`
Key claims:
* Templates across common formats:
  * talking heads, rough cuts, vlogs, podcasts, sizzle reels, clips, montages, keynotes, webinars
  * plus A/B testing and content engine
* Implication: faster activation via format-specific workflows

Conversion surfaces present:
* `Get Started` / `Explore Mosaic` entry points

### `https://mosaic.so/agent`
Key claims:
* Agentic "orchestrator" experience: prompt any video into existence (Video Edits, Motion Graphics)
* Strong emphasis on autonomous prompting and result generation

Conversion surfaces present:
* `Join the Waitlist`
* `Book a Demo` (teams)

### `https://docs.mosaic.so/api`
Key claims:
* Base URL and authentication model (API key prefixed with `mk_`)
* Core concepts:
  * Agent templates and agent runs (track via run id)
  * Triggers (automate execution from external events, like new YouTube videos)
  * Webhooks (real-time status updates)
  * Asset management (upload and fetch signed view URLs)
  * Credits and plans

Conversion surfaces present:
* API intro and endpoint exploration
* Implication for B2B: Mosaic is programmable, not just a UI tool

---

## 1.1 Competitive snapshot for slide table

For the deck's competitive landscape, use only node-based creation/editing competitors and keep table columns as:
**Competitor | Focus | Mosaic advantage**

* **FLORA** | Multi-model creative environment with unified canvas workflows | Mosaic advantage: stronger enterprise video operations narrative (automation + integrations + governance).
* **Weavy** | Node-based artistic creation + editing platform | Mosaic advantage: clearer production-pipeline and security/governance positioning.
* **Krea (Nodes)** | Node workflow builder for image/video generation and model chaining | Mosaic advantage: more explicit team-grade onboarding and repeatable operational workflows.
* **Kaiber Superstudio** | Infinite-canvas flow creation across video/image/motion | Mosaic advantage: stronger end-to-end workflow implementation and pipeline reliability story.
* **ComfyUI** | Open-source node graph for advanced generative workflows | Mosaic advantage: lower enterprise adoption friction through managed UX and GTM-ready governance narrative.

---

## 2. Objection -> message mapping (B2C)

### Objection A: "Will this work for my content format?"
Relevant on-site proof:
* Templates gallery lists format-specific workflows (podcasts, talking heads, webinars, clips)
* Product page shows prompt-based rough cuts and structured workflow outcomes

Best conversion surfaces:
* `templates` -> `Get Started`
* `product` -> `Get Started` (canvas exploration)

### Objection B: "How quickly can I get a usable result?"
Relevant on-site proof:
* "Agentic editing" and template-first experiences
* Content engine positioning (autopilot workflows)

Best conversion surfaces:
* `templates` and `agent` waitlist entry points
* Automation page (gives the "run it on autopilot" clarity)

### Objection C: "Will my workflow be reusable?"
Relevant on-site proof:
* Node-based canvas and workflow reuse implication (design once, run forever)
* Content engine triggers connect repeated runs to sources

Best conversion surfaces:
* `product/automation` and template packs

---

## 3. Objection -> message mapping (B2B: enterprise and agencies)

### Objection D: "Can our team govern access safely?"
Relevant on-site proof:
* RBAC, shared workspaces, centralized asset library
* Activity and audit logs

Best conversion surfaces:
* `/enterprise` (primary trust narrative) -> `Book a Demo`
* demo onboarding collateral that repeats RBAC and audit log explanations

### Objection E: "Does Mosaic fit our pipeline?"
Relevant on-site proof:
* MAM/storage integration and NLE export/roundtrip (Premiere/Resolve/Final Cut via XML exports)

Best conversion surfaces:
* `/enterprise` integrations sections
* product pages for roundtrip and timeline editor credibility

### Objection F: "Can we automate workflows and connect systems?"
Relevant on-site proof:
* event-driven triggers, webhooks, custom workflows
* API access and agent runs
* automation page "ContentFactory" positioning

Best conversion surfaces:
* `/enterprise` custom automations sections
* `docs.mosaic.so/api` for technical evaluators

### Objection G: "Is Mosaic safe for our data?"
Relevant on-site proof:
* SOC 2 Type II positioning
* zero data retention options
* no training on customer data

Best conversion surfaces:
* `/enterprise` security & compliance section
* additional "security collateral" content blocks to support procurement reviews (incorporate into demo follow-up)

---

## 4. Conversion surface recommendations for growth execution

These are "what we should retarget and measure" suggestions to align channel strategy with what the site already does well.

* B2C retargeting:
  * `templates` pages -> activated creator pages (measure activation and repeat runs)
  * `product` page -> "agent" waitlist conversion
  * `product/automation` page -> signup to content engine flows
* B2B retargeting:
  * `/enterprise` -> demo booking and technical meeting routes
  * API docs -> technical demo or trial onboarding routes
  * automation page -> custom workflow and implementation discussions

Tracking note for the playbook:
* prioritize event tracking for "meaningful intent" rather than only pageviews:
  * template chosen + run started (B2C)
  * enterprise surface engaged + API/automation intent (B2B)

---

## 5. How this website map ties back to the deck

* Slide 6 (Website & Digital Experience) uses these claims as the conversion narrative.
* Slide 7 (Marketing Channels) targets audiences to the surfaces that match objections.
* Slide 10 (CRM automation) uses intent tiers derived from these surfaces.
* Slide 13 (AI Ops) automates routing/scoring so the right audience reaches the right surface at the right time.
* Slide 14-15 (Risks + 3-month roadmap) uses security/integration coverage and instrumentation as early deliverables.

---

## 6. Acquisition, Activation, Retention (AAR) mapping from website surfaces

This section translates website behavior into lifecycle stages so growth reporting aligns with the new AAR slide.

### 6.1 Acquisition (entry quality by surface)
* B2C acquisition surfaces:
  * `templates`, `product`, and `agent` pages (creator-interest entry points)
* B2B acquisition surfaces:
  * `/enterprise`, `product/automation`, and `docs.mosaic.so/api` (team and technical evaluator entry points)
* acquisition quality heuristic:
  * treat visits as low-signal until they produce intent events (template run, API exploration depth, demo booking intent)

### 6.2 Activation (first value signals)
* B2C activation signals:
  * first template run and first usable output
  * repeated usage of a workflow in a short window
* B2B activation signals:
  * first successful workflow run in a team context
  * evidence of governance/integration readiness (enterprise page depth, automation/API follow-through)
* activation instrumentation recommendations:
  * track "time from first visit to first successful run"
  * separately track "time from enterprise visit to technical demo/onboarding start"

### 6.3 Retention (ongoing value and expansion)
* B2C retention signals:
  * repeat-run frequency
  * continued repurposing behavior
* B2B retention signals:
  * recurring workspace activity
  * collaborator growth
  * trigger/API expansion behavior
* retention lens:
  * if users do not progress from "feature curiosity" to "workflow repetition," messaging and onboarding need adjustment.

### 6.4 AAR notes for deck/ops alignment
* Website analytics, CRM routing, and AI Ops scoring should all tag events as Acquisition, Activation, or Retention.
* This tagging enables cleaner reporting for:
  * Slide 16 (AAR),
  * Slide 17 (Unit economics),
  * and Slide 18 (Defining success).

