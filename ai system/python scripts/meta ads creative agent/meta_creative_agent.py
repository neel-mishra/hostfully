"""
meta_creative_agent.py — Main Orchestrator

CLI entry point, interactive brief intake, LLM generation call,
output assembly, and file saving. Supports --dry-run mode.
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Add parent path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

import context_loader
import research
from canva_connector import (
    discover_canva_server,
    parse_creative_output_to_plan,
    persist_sync_plan,
    validate_canva_tooling,
)
from prompts import CampaignBrief, build_system_prompt, build_user_message
from validator import validate_output, format_validation_for_output


# ---------------------------------------------------------------------------
# API Key Resolution
# ---------------------------------------------------------------------------

def _resolve_api_key(cli_key: str | None) -> str:
    """
    Check (in order): CLI argument, GEMINI_API_KEY env var,
    then walk up directory tree looking for .env files.
    """
    # 1. CLI argument
    if cli_key:
        return cli_key

    # 2. Environment variable
    env_key = os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key

    # 3. Walk up directory tree for .env files
    current = Path(__file__).resolve().parent
    while current != current.parent:
        env_file = current / ".env"
        if env_file.exists():
            with open(env_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("GEMINI_API_KEY="):
                        key = line.split("=", 1)[1].strip().strip("'\"")
                        if key:
                            return key
        current = current.parent

    print("❌ No API key found. Provide via --api-key, GEMINI_API_KEY env var, or .env file.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# CLI Helpers
# ---------------------------------------------------------------------------

def _select(
    prompt: str,
    options: dict[str, str],
    allow_multiple: bool = False,
) -> str | list[str]:
    """Interactive single or multi-select from options."""
    print(f"\n{'─' * 60}")
    print(f"  {prompt}")
    print(f"{'─' * 60}")
    keys = list(options.keys())
    for i, (key, desc) in enumerate(options.items(), 1):
        print(f"  [{i}] {key} — {desc}")

    if allow_multiple:
        print(f"\n  Enter numbers separated by commas (e.g. 1,3,4) or 'all':")
    else:
        print(f"\n  Enter number (1-{len(keys)}):")

    while True:
        choice = input("  > ").strip()

        if allow_multiple:
            if choice.lower() == "all":
                return keys
            try:
                indices = [int(x.strip()) for x in choice.split(",")]
                if all(1 <= i <= len(keys) for i in indices):
                    return [keys[i - 1] for i in indices]
            except ValueError:
                pass
            print(f"  ⚠ Invalid selection. Enter numbers 1-{len(keys)} or 'all'.")
        else:
            try:
                idx = int(choice)
                if 1 <= idx <= len(keys):
                    return keys[idx - 1]
            except ValueError:
                pass
            print(f"  ⚠ Invalid selection. Enter a number 1-{len(keys)}.")


def _text_input(prompt: str, default: str = "") -> str:
    """Text input with optional default."""
    print(f"\n{'─' * 60}")
    print(f"  {prompt}")
    if default:
        print(f"  (Default: {default})")
    print(f"{'─' * 60}")
    value = input("  > ").strip()
    return value if value else default


def _int_input(prompt: str, default: int = 3, min_val: int = 1, max_val: int = 10) -> int:
    """Integer input with bounds and default."""
    print(f"\n{'─' * 60}")
    print(f"  {prompt} (default: {default}, range: {min_val}-{max_val})")
    print(f"{'─' * 60}")
    while True:
        value = input("  > ").strip()
        if not value:
            return default
        try:
            n = int(value)
            return max(min_val, min(max_val, n))
        except ValueError:
            print(f"  ⚠ Enter a number between {min_val} and {max_val}.")


# ---------------------------------------------------------------------------
# Interactive Intake
# ---------------------------------------------------------------------------

def collect_campaign_brief() -> tuple[CampaignBrief, list[str] | None]:
    """10-step interactive CLI intake. Returns (CampaignBrief, premium_brands_selection)."""

    print("\n" + "═" * 60)
    print("  🎨 META ADS CREATIVE AGENT — Campaign Brief Intake")
    print("═" * 60)

    # Step 1 — Campaign Goal
    goal = _select("Step 1/10 — Campaign Goal", {
        "lead_gen": "Drive demo signups and trial starts",
        "brand_awareness": "Build brand recognition and category authority",
        "competitive_displacement": "Win users from specific competitors",
        "demo_signups": "Get qualified prospects to book a demo",
        "trial_starts": "Drive free trial activations",
    })

    # Step 2 — Funnel Stage
    funnel_stage = _select("Step 2/10 — Funnel Stage", {
        "prospecting": "Cold audience — never heard of Hostfully",
        "awareness": "Know the AI marketing agent category, haven't evaluated us",
        "retargeting": "Visited our site / engaged with content",
        "bottom_of_funnel": "Comparing us to competitors, ready to decide",
    })

    # Step 3 — Target Audience
    target_audience = _text_input(
        "Step 3/10 — Target Audience (free text)",
        default="Digital marketers and agency owners managing Meta/Google ad campaigns looking for an AI-powered solution",
    )

    # Step 4 — Ad Placements
    placements = _select("Step 4/10 — Ad Placements (select multiple)", {
        "instagram_feed": "Instagram Feed 1:1 or 4:5",
        "instagram_stories": "Instagram Stories 9:16",
        "facebook_feed": "Facebook Feed 1:1 or 4:5",
        "facebook_reels": "Facebook Reels 9:16",
        "instagram_reels": "Instagram Reels 9:16",
    }, allow_multiple=True)

    # Step 5 — Visual Lever
    visual_lever = _select("Step 5/10 — Visual Lever", {
        "icp_based": "Lifestyle / Persona — center on the marketer",
        "ui_based": "Product / UI — Mia chat interface as hero",
        "combination": "Fusion — lifestyle + UI composed together",
    })

    # Step 6 — Messaging Pillar
    pillar_auto_map = {
        "lead_gen": "Pillar 2",
        "brand_awareness": "Pillar 1",
        "competitive_displacement": "Pillar 4",
        "demo_signups": "Pillar 2",
        "trial_starts": "Pillar 3",
    }

    pillar_choice = _select("Step 6/10 — Messaging Pillar", {
        "auto": "Auto-select based on campaign goal",
        "Pillar 1": "One Conversation Replaces Five Dashboards",
        "Pillar 2": "AI That Acts, Not Just Suggests",
        "Pillar 3": "Enterprise Intelligence, Startup Simplicity",
        "Pillar 4": "The Autonomous Marketing Teammate / Category Creation",
    })

    if pillar_choice == "auto":
        messaging_pillar = pillar_auto_map.get(goal, "Pillar 2")
        print(f"  → Auto-selected: {messaging_pillar}")
    else:
        messaging_pillar = pillar_choice

    # Step 7 — Number of Concepts
    num_concepts = _int_input("Step 7/10 — Number of Concepts to Generate")

    # Step 8 — Competitors to Research
    print(f"\n{'─' * 60}")
    print("  Step 8/10 — Competitors to Research")
    print(f"{'─' * 60}")

    # Group by tier
    tiers: dict[str, list[tuple[str, str]]] = {}
    for comp_key, comp_data in research.COMPETITOR_CATALOG.items():
        cat = comp_data["category"]
        tier_name = research.TIER_NAMES.get(cat, cat)
        if tier_name not in tiers:
            tiers[tier_name] = []
        tiers[tier_name].append((comp_key, comp_data["label"]))

    for tier_name, comps in tiers.items():
        print(f"\n  {tier_name}:")
        for key, label in comps:
            print(f"    • {key}: {label}")

    print(f"\n  Enter competitor names (comma-separated), a tier category")
    print(f"  (direct_agent, services, data_pipes, point_solution, measurement),")
    print(f"  or 'all' (default: all):")

    comp_input = input("  > ").strip()
    if not comp_input or comp_input.lower() == "all":
        competitors_researched = list(research.COMPETITOR_CATALOG.keys())
    elif comp_input.lower() in ("direct_agent", "services", "data_pipes", "point_solution", "measurement"):
        competitors_researched = [
            k for k, v in research.COMPETITOR_CATALOG.items()
            if v["category"] == comp_input.lower()
        ]
    else:
        competitors_researched = [c.strip().lower() for c in comp_input.split(",") if c.strip()]

    # Step 9 — Premium Brands
    brands_input = _text_input(
        "Step 9/10 — Premium Brands to Study (comma-separated or 'default' for full catalog)",
        default="default",
    )
    if brands_input.lower() == "default":
        premium_brands_selection = None  # Will use full catalog
        premium_brands_display = ["Full curated catalog"]
    else:
        premium_brands_selection = [b.strip() for b in brands_input.split(",") if b.strip()]
        premium_brands_display = premium_brands_selection

    # Step 10 — Additional Context
    additional_context = _text_input(
        "Step 10/10 — Additional Context (optional, press Enter to skip)",
        default="",
    )

    # Build the brief
    brief = CampaignBrief(
        goal=goal,
        funnel_stage=funnel_stage,
        target_audience=target_audience,
        placements=placements,
        visual_lever=visual_lever,
        messaging_pillar=messaging_pillar,
        num_concepts=num_concepts,
        competitors_researched=competitors_researched,
        premium_brands_researched=premium_brands_display,
        additional_context=additional_context,
    )

    # Summary
    print("\n" + "═" * 60)
    print("  📋 CAMPAIGN BRIEF SUMMARY")
    print("═" * 60)
    print(f"  Goal:               {brief.goal}")
    print(f"  Funnel Stage:       {brief.funnel_stage}")
    print(f"  Target Audience:    {brief.target_audience[:60]}...")
    print(f"  Placements:         {', '.join(brief.placements)}")
    print(f"  Visual Approach:    {brief.visual_lever}")
    print(f"  Messaging Pillar:   {brief.messaging_pillar}")
    print(f"  Concepts:           {brief.num_concepts}")
    print(f"  Competitors:        {', '.join(brief.competitors_researched)}")
    print(f"  Premium Brands:     {', '.join(brief.premium_brands_researched)}")
    if brief.additional_context:
        print(f"  Additional Context: {brief.additional_context[:60]}...")
    print("═" * 60)

    # Confirmation
    confirm = input("\n  Proceed? [Y/n] ").strip()
    if confirm.lower() == "n":
        print("  Cancelled.")
        sys.exit(0)

    return brief, premium_brands_selection


# ---------------------------------------------------------------------------
# LLM Generation
# ---------------------------------------------------------------------------

def generate_concepts(
    system_prompt: str,
    user_message: str,
    api_key: str,
    model: str = "gemini-2.5-flash",
) -> str:
    """Call Gemini to generate creative concepts."""
    from google import genai

    print("\n🤖 Generating creative concepts via Gemini...")
    print(f"  Model: {model}")
    print(f"  System prompt: {len(system_prompt):,} chars")
    print(f"  User message: {len(user_message):,} chars")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=user_message,
        config={
            "system_instruction": system_prompt,
            "max_output_tokens": 8000,
        },
    )

    # Try to get text
    if response.text:
        return response.text

    # Fallback: try candidates
    try:
        if response.candidates and response.candidates[0].content.parts:
            text = response.candidates[0].content.parts[0].text
            if text:
                return text
    except (AttributeError, IndexError):
        pass

    print("❌ Empty response from Gemini. Check your API key and model.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Output Assembly
# ---------------------------------------------------------------------------

def assemble_final_output(
    campaign: CampaignBrief,
    research_brief_text: str,
    creative_output: str,
    validation_text: str,
) -> str:
    """Produce a structured markdown document."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    placements_str = ", ".join(campaign.placements)
    competitors_str = ", ".join(campaign.competitors_researched)
    brands_str = ", ".join(campaign.premium_brands_researched)

    doc = f"""# Meta Ads Creative Brief
**Generated:** {timestamp}
**Agent:** Meta Ads Creative Agent v1.0

---

## Campaign Parameters

| Parameter | Value |
|-----------|-------|
| **Goal** | {campaign.goal} |
| **Funnel Stage** | {campaign.funnel_stage} |
| **Target Audience** | {campaign.target_audience} |
| **Placements** | {placements_str} |
| **Visual Approach** | {campaign.visual_lever} |
| **Messaging Pillar** | {campaign.messaging_pillar} |
| **Concepts Generated** | {campaign.num_concepts} |
| **Competitors Researched** | {competitors_str} |
| **Premium Brands Studied** | {brands_str} |
| **Additional Context** | {campaign.additional_context or 'None'} |

---

## Creative Intelligence Summary

{research_brief_text}

---

## Creative Concepts

{creative_output}

---

{validation_text}
"""
    return doc


# ---------------------------------------------------------------------------
# Output Saving
# ---------------------------------------------------------------------------

def save_output(content: str, campaign: CampaignBrief) -> str:
    """Save the final document to disk."""
    # Find project root
    current = Path(__file__).resolve().parent
    while current != current.parent:
        if (current / "commands").is_dir():
            break
        current = current.parent

    base_dir = current / "docs" / "paid_ads_assets" / "meta"
    date_str = datetime.now().strftime("%Y-%m-%d")
    folder_name = f"{date_str}_{campaign.goal}_{campaign.funnel_stage}_creative_brief"

    output_dir = base_dir / folder_name
    counter = 1
    while output_dir.exists():
        counter += 1
        output_dir = base_dir / f"{folder_name}_{counter}"

    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "creative_brief.md"
    output_file.write_text(content, encoding="utf-8")

    return str(output_file)


def maybe_prepare_canva_sync(
    campaign: CampaignBrief,
    creative_output: str,
    output_doc_path: str,
    *,
    enable_canva_sync: bool,
) -> None:
    """
    Build and save a Canva MCP sync plan when enabled.
    This does not execute MCP tool calls directly; it validates connector readiness
    and emits a deterministic handoff artifact used by downstream Canva automation.
    """
    if not enable_canva_sync:
        return

    print("\n🧩 Preparing Canva MCP sync plan...")
    descriptor = discover_canva_server()
    checks = validate_canva_tooling(descriptor)

    print(f"  Canva MCP server: {descriptor.server_name}")
    print(f"  Tools discovered: {len(descriptor.tools)}")
    print(
        "  Tooling checks: "
        f"create/template={checks['has_create_or_template']} "
        f"text/edit={checks['has_text_or_element_tool']} "
        f"export/publish={checks['has_export_or_publish']}"
    )

    if not checks["ready"]:
        print(
            "❌ Canva MCP connector is not ready. "
            "Expected create/template, text/edit, and export/publish tool coverage."
        )
        sys.exit(1)

    plan = parse_creative_output_to_plan(
        creative_output,
        campaign_goal=campaign.goal,
        funnel_stage=campaign.funnel_stage,
        target_audience=campaign.target_audience,
        placement_tags=campaign.placements,
    )

    plan_path = Path(output_doc_path).parent / "canva_mcp_sync_plan.json"
    persist_sync_plan(plan, plan_path)
    print(f"  ✅ Canva sync plan saved: {plan_path}")


# ---------------------------------------------------------------------------
# Dry Run Sample Data
# ---------------------------------------------------------------------------

DRY_RUN_SAMPLE_OUTPUT = """## CONCEPT [1]: The Inbox of Chaos vs. The Single Thread

**Visual Type:** Combination
**Messaging Pillar:** Pillar 4 — The Autonomous Marketing Teammate
**Funnel Stage:** retargeting
**Inspired By:** Rippling — Bold competitive split-screen positioning
**Pattern Break:** Split-screen showing 12 open browser tabs (chaos side) vs. a single clean Mia chat thread managing all campaigns (order side)

### VISUAL DESCRIPTION
- **Scene and Composition:** Left half: a chaotic desktop with 12 browser tabs open — Meta Business Suite, Google Ads, TikTok Ads, Sheets, Looker Studio, email — all visible, overlapping, stressful. Right half: a single clean Mia chat window on dark #111827 background, with a message reading "Your Meta CPA is up 23%. I paused the underperforming ad set and shifted budget to your top creative. Here's what I recommend next."
- **The Scroll-Stop Element:** The extreme visual contrast between chaos (left) and calm (right) — the viewer's eye is drawn to the clean Mia chat as relief from the visual noise
- **Premium Execution Notes:** Inter Bold typography for the headline, precise alignment of the split-screen divider, subtle shadow on the Mia chat card, #2563EB accent on the chat interface elements
- **Color and Mood:** Left side uses desaturated, slightly overwhelming multi-colored browser tabs. Right side uses Hostfully Dark #111827 background with Primary Blue #2563EB chat accents and Success Green #10B981 for positive metrics
- **Layout and Hierarchy:** 50/50 split composition. Left = chaos (many small elements). Right = single focal point (one chat window). The eye naturally moves from noise to clarity.
- **Format Notes:** 1:1 for Instagram/Facebook feed. For 9:16 stories, stack vertically (chaos top, order bottom)

### AI IMAGE GENERATION PROMPT
Split-screen digital composition. Left side: cluttered desktop screenshot with multiple overlapping browser tabs showing advertising dashboards, spreadsheets, analytics tools, busy and overwhelming, desaturated colors, slight motion blur. Right side: single clean chat interface on solid dark background #111827, minimalist, one message thread, blue accent #2563EB, green metric highlight #10B981, polished premium editorial quality, refined typography Inter font, intentional negative space, high-end software brand aesthetic. No clutter on right side, no generic stock photo, no AI-generated look, no neon, no excessive gradients.

### ON-IMAGE COPY VARIATIONS
**Variation 1:**
- Headline: Twelve tabs open. Zero campaigns optimized. Sound familiar?
- Subtext: Replace the dashboard circus with one intelligent conversation. Mia manages it all.
- CTA: Meet your AI teammate

**Variation 2:**
- Headline: Your browser has 12 tabs. Mia needs one chat.
- Subtext: Stop switching between dashboards. Start talking to your campaigns directly.
- CTA: Try Mia free

**Variation 3:**
- Headline: This is your marketing stack. This is Mia.
- Subtext: One AI marketing agent replaces the tab chaos. Plan, build, optimize, report — one conversation.
- CTA: Start free today

### BELOW-IMAGE AD COPY
- **Primary Text:** Still toggling between 12 tabs to manage your ads? Mia runs Meta, Google, TikTok & Amazon from one chat.
- **Headline:** One chat. Every campaign. Zero tabs.
- **Description:** Your AI marketing teammate

### PREMIUM BRAND REFERENCE
- **Inspired by:** Rippling's confrontational side-by-side comparison ads
- **What we adapted:** The stark visual contrast technique — showing the painful status quo vs. the clean alternative
- **Why it works for our audience:** Marketers instantly recognize the chaos of multiple open tabs — this is their daily reality, making the contrast emotionally powerful

### COMPETITOR CONTRAST
- **Differs from Madgicx because:** Madgicx adds MORE complexity (a cockpit with 50 buttons). This ad shows the opposite — reducing everything to a single conversation. Teammate vs. Cockpit.

### CREATIVE RATIONALE
- **Why this stops the scroll:** The split-screen creates an immediate visual tension — viewers recognize their own messy desktop on the left and are drawn to the relief of the clean right side
- **How it meets the polished/premium bar:** Clean typography, precise alignment at the split point, intentional negative space on the Mia side, brand colors applied consistently
- **Research insight that inspired this:** "Nobody targets the emotional exhaustion of tab-switching and context-switching" — this is the #1 unoccupied creative territory
- **Why this is NOT a boring SaaS ad:** No floating laptop, no abstract gradients, no feature list — it's a visceral before/after that triggers an emotional reaction

---

## CONCEPT [2]: The 3AM Campaign Save

**Visual Type:** UI-based
**Messaging Pillar:** Pillar 4 — The Autonomous Marketing Teammate
**Funnel Stage:** retargeting
**Inspired By:** Linear — UI-as-hero typographic minimalism
**Pattern Break:** A real Mia chat screenshot timestamped at 3:14 AM showing Mia catching and fixing a budget-burning campaign while the marketer sleeps

### VISUAL DESCRIPTION
- **Scene and Composition:** Dark #111827 background. A single Mia chat window, premium framing with subtle shadow. The timestamp reads 3:14 AM. Mia's message: "I noticed your 'Summer Launch' campaign CPA spiked to $47 (2.3x your target) in the last 2 hours. I've paused the underperforming ad set, shifted $120 to your top performer, and your projected CPA is now back to $19. Here's what happened." Below: a small metrics card showing the save — green #10B981 arrow.
- **The Scroll-Stop Element:** The "3:14 AM" timestamp — it immediately communicates "this works while you're asleep"
- **Premium Execution Notes:** Monospace font for the timestamp for technical credibility. Inter for the chat text. Generous negative space around the chat card. Subtle gradient shadow behind the card.
- **Color and Mood:** Hostfully Dark #111827 dominant. Primary Blue #2563EB for the Mia avatar and interface elements. Success Green #10B981 for the metric improvement. Overall mood: calm authority — "everything is handled"
- **Layout and Hierarchy:** Single focal point — the chat window. The timestamp is the entry point, the message body is the substance, the metrics card is the proof.
- **Format Notes:** 1:1 for feeds (centered chat card). 9:16 for stories (chat card fills upper 60%, headline text below)

### AI IMAGE GENERATION PROMPT
Dark background #111827, single chat interface window centered with subtle drop shadow, premium framing, timestamp showing 3:14 AM in monospace font, chat message from AI assistant showing campaign optimization details, small green #10B981 metrics card showing improvement, minimal composition with one focal element, generous negative space, polished premium editorial quality, refined typography, high-end software brand aesthetic. No clutter, no generic stock photo, no AI-generated look, no neon, no excessive gradients.

### ON-IMAGE COPY VARIATIONS
**Variation 1:**
- Headline: At 3AM, your campaigns had a problem. Mia fixed it.
- Subtext: Your AI marketing agent optimizes while you sleep. Real actions, real results, real transparency.
- CTA: Meet Mia — start free

**Variation 2:**
- Headline: You slept. Mia saved your campaign $340 overnight.
- Subtext: An AI marketing agent that doesn't just alert you — she acts. Then explains why.
- CTA: Try Mia free

**Variation 3:**
- Headline: Your last AI tool sent you a notification. Mia sent results.
- Subtext: While you sleep, Mia monitors, optimizes, and acts on your campaigns across every platform.
- CTA: Start free today

### BELOW-IMAGE AD COPY
- **Primary Text:** Your campaign burned $340 at 3AM. Ryze would've sent a notification. Mia paused the bleed and fixed it.
- **Headline:** AI that acts while you sleep
- **Description:** Your AI marketing teammate

### PREMIUM BRAND REFERENCE
- **Inspired by:** Linear's product-as-hero approach — making the UI the entire ad
- **What we adapted:** The single UI screenshot as the complete visual, with typographic precision and dark-mode elegance making it feel premium rather than promotional
- **Why it works for our audience:** Marketers fear overnight budget burns. Seeing a REAL chat log of Mia catching one is more compelling than any feature description

### COMPETITOR CONTRAST
- **Differs from Ryze because:** Ryze would have sent a notification at 3AM that the marketer wouldn't see until morning. Mia actually FIXED it. Suggestions vs. Actions.

### CREATIVE RATIONALE
- **Why this stops the scroll:** The 3AM timestamp is an emotional trigger — every marketer has woken up to a campaign that burned budget overnight. This shows the alternative
- **How it meets the polished/premium bar:** Single focal point, dark mode elegance, precise typography, generous negative space — Linear-level minimalism
- **Research insight that inspired this:** "Fear of missing optimization windows — campaigns underperform while they sleep" is a top emotional driver
- **Why this is NOT a boring SaaS ad:** No feature list, no dashboard screenshot, no abstract claims — it's a specific, timestamped scenario that tells a story

---

## CONCEPT [3]: The Teammate Manifesto

**Visual Type:** ICP-based
**Messaging Pillar:** Pillar 4 — The Autonomous Marketing Teammate
**Funnel Stage:** retargeting
**Inspired By:** Notion — Aspirational lifestyle meets bold typographic statement
**Pattern Break:** A marketer at a cafe with coffee, relaxed and smiling, with oversized typographic statement overlaid — feels like a magazine editorial, not an ad

### VISUAL DESCRIPTION
- **Scene and Composition:** Editorial-quality photograph of a marketer (late 20s/early 30s) at a bright cafe table. Natural light. Coffee in hand. Laptop open (subtle, not hero). They're looking at their phone — a tiny Mia chat notification visible. The dominant visual element: an oversized typographic statement filling the upper portion of the frame: "I didn't become a marketer to babysit dashboards."
- **The Scroll-Stop Element:** The oversized text statement — it reads like a personal declaration, not ad copy
- **Premium Execution Notes:** Inter Bold for the headline at large scale. The typography is the hero — sized to fill ~40% of the frame. Warm, editorial color grading on the photo. Subtle Hostfully Blue #2563EB on the CTA button.
- **Color and Mood:** Warm natural tones (the cafe). White/cream for the oversized type. Hostfully Blue #2563EB for the subtle CTA. Overall mood: aspirational confidence — "this is what marketing feels like now"
- **Layout and Hierarchy:** Typography (40% of frame) → Person (40%) → Product subtle hint (20%). The text draws you in, the person makes it relatable, the product hint creates curiosity.
- **Format Notes:** 4:5 for Instagram feed (vertical orientation suits the typographic layout). 9:16 for stories (text fills upper third, person fills middle, CTA at bottom)

### AI IMAGE GENERATION PROMPT
Editorial photography, young professional at a bright modern cafe, natural window light, warm tones, relaxed confident expression, coffee in hand, laptop slightly visible, candid authentic moment not posed, shot with shallow depth of field, overlaid with large bold white typography reading a manifesto statement, magazine editorial quality, clean modern environment, polished premium aesthetic, no cluttered background, no stock photo feel, no AI-generated look, no neon, no excessive gradients, high-end brand campaign photography style.

### ON-IMAGE COPY VARIATIONS
**Variation 1:**
- Headline: I didn't become a marketer to babysit dashboards.
- Subtext: Meet Mia — the AI marketing agent that handles Meta, Google, TikTok, and Amazon while you do strategy.
- CTA: Meet your teammate

**Variation 2:**
- Headline: Strategist, not button-pusher. That's the job I signed up for.
- Subtext: Mia is your AI marketing agent — she acts on your campaigns so you can think bigger.
- CTA: Try Mia free

**Variation 3:**
- Headline: I used to manage campaigns. Now I manage an AI teammate.
- Subtext: Hostfully handles the execution — optimization, reporting, and actions — across every platform.
- CTA: Start free today

**Variation 4:**
- Headline: Five dashboards down to one conversation. This is the future.
- Subtext: Your AI marketing agent replaces the tab chaos. Plan, build, and report — all through chat.
- CTA: Meet Mia now

### BELOW-IMAGE AD COPY
- **Primary Text:** You didn't become a marketer to babysit dashboards. Mia is your AI marketing agent — she acts, not suggests.
- **Headline:** Your AI marketing teammate
- **Description:** Start free. No credit card.

### PREMIUM BRAND REFERENCE
- **Inspired by:** Notion's aspirational lifestyle-meets-product editorial campaign
- **What we adapted:** The warm, authentic lifestyle photography with bold typographic overlay — making the ad feel like a magazine spread rather than a product promo
- **Why it works for our audience:** Marketers aspire to be strategic thinkers, not execution drones. This ad validates their identity and positions Mia as the enabler of that aspiration

### COMPETITOR CONTRAST
- **Differs from Albert because:** Albert's ads are technical and opaque — autonomous AI with no emotional connection. This ad connects on identity and aspiration while still communicating AI capability. Transparency vs. Black Box.

### CREATIVE RATIONALE
- **Why this stops the scroll:** The oversized typography reads like a personal manifesto — it's unexpected in a B2B SaaS ad context and triggers immediate identification
- **How it meets the polished/premium bar:** Editorial photography quality, precise typographic hierarchy, warm but controlled color palette, magazine-level composition
- **Research insight that inspired this:** "Identity tension — they became marketers for strategy and creativity, not to babysit CPMs and adjust bids" — this is the deepest emotional driver
- **Why this is NOT a boring SaaS ad:** There's no product screenshot as hero, no feature list, no dashboard — it's a human story told through a typographic statement that happens to be an ad for Hostfully
"""


# ---------------------------------------------------------------------------
# Dry Run Mode
# ---------------------------------------------------------------------------

def run_dry_test() -> None:
    """Run the full pipeline with preset inputs, no API key needed."""
    print("\n" + "═" * 60)
    print("  🧪 DRY RUN MODE — Testing full pipeline")
    print("═" * 60)

    # 1. Preset campaign brief
    campaign = CampaignBrief(
        goal="lead_gen",
        funnel_stage="retargeting",
        target_audience="Digital marketers and agency owners managing Meta/Google ad campaigns",
        placements=["instagram_feed", "facebook_feed", "instagram_stories"],
        visual_lever="combination",
        messaging_pillar="Pillar 4",
        num_concepts=3,
        competitors_researched=list(research.COMPETITOR_CATALOG.keys()),
        premium_brands_researched=["Linear", "Notion", "Ramp", "Rippling", "Stripe", "Figma"],
    )

    print(f"\n📋 Campaign: {campaign.goal} / {campaign.funnel_stage}")
    print(f"  Pillar: {campaign.messaging_pillar}")
    print(f"  Visual: {campaign.visual_lever}")
    print(f"  Concepts: {campaign.num_concepts}")

    # 2. Load brand context
    print("\n📂 Loading brand context files...")
    ctx = context_loader.load_all_context()
    brand_context = context_loader.build_brand_context_block(ctx)
    print(f"  Brand context: {len(brand_context):,} chars")

    # 3. Fallback research
    print("\n🧠 Generating fallback research data...")
    research_brief = research.run_deep_research(
        competitors=campaign.competitors_researched,
        premium_brands=None,
        target_description=campaign.target_audience,
        api_key="",  # Empty key forces fallback
    )
    research_text = research_brief.to_prompt_block()
    print(f"  Research brief: {len(research_text):,} chars")

    # 4. Build prompts (for inspection)
    system_prompt = build_system_prompt(brand_context, research_text, campaign)
    user_message = build_user_message(campaign)
    print(f"\n📝 System prompt: {len(system_prompt):,} chars")
    print(f"  User message: {len(user_message):,} chars")

    # 5. Use sample output
    print("\n🎨 Using sample creative output (3 concepts)...")
    creative_output = DRY_RUN_SAMPLE_OUTPUT

    # 6. Validate
    print("\n✅ Running validation checks...")
    report = validate_output(creative_output, campaign.num_concepts)
    validation_text = format_validation_for_output(report)
    print(f"  {report.summary()}")

    # 7. Assemble
    final_doc = assemble_final_output(campaign, research_text, creative_output, validation_text)
    print(f"\n📄 Final document: {len(final_doc):,} chars")

    # 8. Save
    output_path = save_output(final_doc, campaign)
    print(f"\n💾 Saved to: {output_path}")

    if not report.passed:
        print("\n⚠️  Validation FAILED — review the validation report section in the output.")
    else:
        print("\n✅ Dry run complete — all checks passed!")


# ---------------------------------------------------------------------------
# Main Pipeline
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Meta Ads Creative Agent — Generate premium ad creative concepts for Hostfully"
    )
    parser.add_argument("--api-key", type=str, help="Gemini API key")
    parser.add_argument("--model", type=str, default="gemini-2.5-flash", help="Gemini model name")
    parser.add_argument("--skip-research", action="store_true", help="Skip live research, use fallback data")
    parser.add_argument("--dry-run", action="store_true", help="Full pipeline test with preset inputs")
    parser.add_argument(
        "--canva-sync",
        action="store_true",
        help="Validate Canva MCP connector and emit canva_mcp_sync_plan.json alongside output",
    )
    args = parser.parse_args()

    # Dry run mode
    if args.dry_run:
        run_dry_test()
        return

    # Resolve API key
    api_key = _resolve_api_key(args.api_key)

    # Interactive intake
    campaign, premium_brands_selection = collect_campaign_brief()

    # Load brand context
    print("\n📂 Loading brand context files...")
    ctx = context_loader.load_all_context()
    brand_context = context_loader.build_brand_context_block(ctx)
    print(f"  Brand context: {len(brand_context):,} chars")

    # Research
    if args.skip_research:
        print("\n⏩ Skipping live research — using fallback data...")
        research_brief = research.run_deep_research(
            competitors=campaign.competitors_researched,
            premium_brands=premium_brands_selection,
            target_description=campaign.target_audience,
            api_key="",  # Empty key forces fallback
        )
    else:
        research_brief = research.run_deep_research(
            competitors=campaign.competitors_researched,
            premium_brands=premium_brands_selection,
            target_description=campaign.target_audience,
            api_key=api_key,
        )

    research_text = research_brief.to_prompt_block()

    # Build prompts
    system_prompt = build_system_prompt(brand_context, research_text, campaign)
    user_message = build_user_message(campaign)

    print(f"\n📝 Prompt sizes:")
    print(f"  System: {len(system_prompt):,} chars")
    print(f"  User:   {len(user_message):,} chars")

    # Generate
    creative_output = generate_concepts(system_prompt, user_message, api_key, args.model)
    print(f"\n🎨 Generated {len(creative_output):,} chars of creative output")

    # Validate
    print("\n✅ Running validation checks...")
    report = validate_output(creative_output, campaign.num_concepts)
    validation_text = format_validation_for_output(report)
    print(f"  {report.summary()}")

    # Assemble
    final_doc = assemble_final_output(campaign, research_text, creative_output, validation_text)

    # Save
    output_path = save_output(final_doc, campaign)
    print(f"\n💾 Output saved to: {output_path}")
    print(f"  Total: {len(final_doc):,} chars")

    maybe_prepare_canva_sync(
        campaign,
        creative_output,
        output_path,
        enable_canva_sync=args.canva_sync,
    )

    if not report.passed:
        print("\n⚠️  Validation FAILED — review the validation report section in the output.")


if __name__ == "__main__":
    main()
