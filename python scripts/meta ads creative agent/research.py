"""
research.py — 4-Track Creative Research Module

Runs 4 research tracks (competitor ads, premium brands, trends, audience psychology)
using web search + LLM synthesis, with comprehensive hardcoded fallback data.
"""

import json
import subprocess
import sys
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Premium Brand Catalog
# ---------------------------------------------------------------------------

PREMIUM_BRAND_CATALOG: dict[str, dict[str, str]] = {
    "Dev Tools": {
        "Linear": "minimal, typographically sharp, product-led",
        "Vercel": "developer-aesthetic, dark mode elegance",
        "Raycast": "ultra-clean UI showcases, tight copy",
    },
    "Design": {
        "Figma": "bold visual identity, high brand recognition",
        "Framer": "motion-rich, editorial-grade creative",
        "Canva Pro": "accessible premium, bright and polished",
    },
    "Fintech": {
        "Ramp": "premium, clean, authority-driven creative",
        "Mercury": "minimal banking aesthetic, trust signals",
        "Brex": "bold data visuals, corporate elegance",
    },
    "Productivity": {
        "Notion": "aspirational lifestyle + product UI fusion",
        "Arc Browser": "counter-culture positioning, distinctive",
        "Cron": "dark-mode minimalism, calendar UI as hero",
    },
    "Infrastructure": {
        "Stripe": "data-rich yet elegant, technical credibility",
        "Retool": "product-as-hero screenshots, builder aesthetic",
        "Supabase": "developer-focused with strong brand color",
    },
    "Vertical SaaS": {
        "Gusto": "SMB-focused B2B, warm and approachable",
        "Rippling": "bold, opinionated competitive positioning",
        "Toast": "industry-specific, real-world imagery",
    },
}


# ---------------------------------------------------------------------------
# Competitor Catalog
# ---------------------------------------------------------------------------

COMPETITOR_CATALOG: dict[str, dict] = {
    # Tier 1 — Direct AI Agent Competitors
    "ryze": {
        "label": "Ryze AI — the Co-Pilot (suggestions only, no execution)",
        "category": "direct_agent",
        "tier": 1,
        "leapfrog": "Autonomy — Doing vs. Suggesting",
        "ad_angle": "Don't just get notifications about what to fix. Get a teammate who fixes it.",
    },
    "smartly": {
        "label": "Smartly.io — the Legacy Giant (enterprise, rule-based, expensive)",
        "category": "direct_agent",
        "tier": 1,
        "leapfrog": "Agility + Modern AI — LLMs vs. Rules, PLG vs. Enterprise bloat",
        "ad_angle": "Enterprise power without the Enterprise bloat.",
    },
    "albert": {
        "label": "Albert.ai — the Black Box (autonomous but opaque, expensive)",
        "category": "direct_agent",
        "tier": 1,
        "leapfrog": "Autonomy WITH Transparency — Mia explains why before she acts",
        "ad_angle": "Autonomy with transparency. Your AI should explain its decisions.",
    },
    # Tier 2 — Traditional Services
    "agencies": {
        "label": "Traditional Agencies — slow, opaque, expensive human services",
        "category": "services",
        "tier": 2,
        "leapfrog": "Speed + Transparency — Agency strategy at software speed, 24/7",
        "ad_angle": "Agency-level strategy with software-level speed. Real-time, transparent, 24/7.",
    },
    # Tier 3 — Data Pipes / Reporting Tools
    "funnel": {
        "label": "Funnel.io — the Data Pipes (moves data but doesn't act on it)",
        "category": "data_pipes",
        "tier": 3,
        "leapfrog": "Action vs. Plumbing — Mia analyzes data AND makes optimization changes",
        "ad_angle": "Don't just move data around. Do something with it.",
    },
    "supermetrics": {
        "label": "Supermetrics — the Connector (data into Sheets/Excel, manual mastery required)",
        "category": "data_pipes",
        "tier": 3,
        "leapfrog": "Agent vs. Plugin — Mia is the analyst AND the media buyer in one",
        "ad_angle": "Stop staring at spreadsheets. Start seeing results.",
    },
    "improvado": {
        "label": "Improvado — the Enterprise Pipe (heavy IT setup, infrastructure not agent)",
        "category": "data_pipes",
        "tier": 3,
        "leapfrog": "Zero-setup intelligence vs. engineering-team infrastructure",
        "ad_angle": "No engineers required. Just connect and talk.",
    },
    # Tier 4 — SMB Optimizers / Point Solutions
    "adzooma": {
        "label": "Adzooma — the SMB Optimizer (rule-based tips, a checklist not an agent)",
        "category": "point_solution",
        "tier": 4,
        "leapfrog": "Execution vs. Homework — Adzooma gives homework, Mia does the work",
        "ad_angle": "Advice is cheap. Execution is everything.",
    },
    "adscale": {
        "label": "AdScale — the E-Com Auto-Pilot (shopping feeds, no brand strategy)",
        "category": "point_solution",
        "tier": 4,
        "leapfrog": "Brand strategy vs. SKU math — Mia understands creative, not just catalogs",
        "ad_angle": "Sell the brand, not just the SKU.",
    },
    "madgicx": {
        "label": "Madgicx — the Facebook Power Tool (brilliant UI but overwhelming cockpit)",
        "category": "point_solution",
        "tier": 4,
        "leapfrog": "Teammate vs. Cockpit — Mia pushes the buttons for you",
        "ad_angle": "You don't need a sharper cockpit. You need a teammate who flies.",
    },
    "adpulse": {
        "label": "AdPulse — the Guardrail (budget protection, defensive posture only)",
        "category": "point_solution",
        "tier": 4,
        "leapfrog": "Offense vs. Defense — Mia maximizes budget, not just protects it",
        "ad_angle": "Don't just protect the budget. Maximize it.",
    },
    # Tier 5 — Attribution / Measurement
    "roadway": {
        "label": "Roadway AI — the Attribution Engine (measures but doesn't build or launch)",
        "category": "measurement",
        "tier": 5,
        "leapfrog": "Action vs. Measurement — Mia automates actions, not just attribution reports",
        "ad_angle": "Don't just measure the road. Drive the car.",
    },
}

TIER_NAMES: dict[str, str] = {
    "direct_agent": "Tier 1 — Direct AI Agent Competitors",
    "services": "Tier 2 — Traditional Services",
    "data_pipes": "Tier 3 — Data Pipes / Reporting Tools",
    "point_solution": "Tier 4 — SMB Optimizers / Point Solutions",
    "measurement": "Tier 5 — Attribution / Measurement",
}


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class ResearchResult:
    track: str
    summary: str
    raw_data: str | None = None
    sources: list[str] = field(default_factory=list)


@dataclass
class CreativeIntelligenceBrief:
    competitor_patterns: str = ""
    premium_benchmark: str = ""
    trending_techniques: str = ""
    audience_insights: str = ""
    raw_results: list[ResearchResult] = field(default_factory=list)

    def to_prompt_block(self) -> str:
        """Format all 4 sections under a CREATIVE INTELLIGENCE BRIEF heading."""
        return f"""# CREATIVE INTELLIGENCE BRIEF

## Competitor Ad Patterns
{self.competitor_patterns}

## Premium Software Brand Benchmark
{self.premium_benchmark}

## Trending Creative Techniques (2025-2026)
{self.trending_techniques}

## Audience Psychology Insights
{self.audience_insights}"""


# ---------------------------------------------------------------------------
# Fallback Data
# ---------------------------------------------------------------------------

FALLBACK_COMPETITOR = """Competitors analyzed across 5 tiers:

Tier 1 — Direct AI Agent Competitors (Ryze, Smartly, Albert): Ryze uses co-pilot positioning, 'suggestions' framing, clean but passive UI screenshots. Smartly uses enterprise-heavy complex dashboard visuals, 'scale' messaging, rule-based logic. Albert uses 'autonomous' claims, black-box aesthetic, enterprise pricing gates content.

Tier 2 — Traditional Agencies: 'We handle it for you' service positioning, team photos, case study carousels. Slow turnaround reality masked by polished brand imagery. Pricing opacity is their biggest vulnerability.

Tier 3 — Data Pipes (Funnel.io, Supermetrics, Improvado): Integration logo grids as hero visuals ('We connect to 500+ sources'). Dashboard/spreadsheet screenshots as proof of value. 'Data' positioning — they move data but never ACT on it. Targeting analysts and ops people, not growth marketers.

Tier 4 — SMB Optimizers (Adzooma, AdScale, Madgicx, AdPulse): 'Optimization tips' and 'opportunities' framing — checklist energy. Before/after ROAS screenshots, green up-arrow graphics. Feature-dense carousel ads, often cluttered. Madgicx has brilliant power-user UI visuals but overwhelming for most. AdScale is e-commerce-specific with shopping feed imagery. AdPulse uses budget protection, defensive/guardrail positioning.

Tier 5 — Attribution/Measurement (Roadway AI): Attribution models and funnel diagrams as visuals. 'Measure ROI' messaging, data warehouse terminology. Passive — tells you what happened, doesn't build what's next.

Common Patterns to AVOID (overused across all tiers): Purple/blue gradient backgrounds with floating dashboard mockups. Integration logo grids as the primary visual. Generic 'AI-powered' claims with no specificity. Before/after ROAS screenshots with green arrows. Feature-list carousels. '10x your marketing' or 'supercharge your ads' empty promises.

Gaps and Opportunities (what NOBODY is doing): Nobody shows a CONVERSATIONAL interface as hero — they all show dashboards or dashboards-with-chatbots. No competitor leads with the 'teammate' frame (vs tool, co-pilot, platform). No one contrasts 'AI that suggests' vs 'AI that acts' visually. Minimal use of real chat transcripts as ad creative. Nobody targets the emotional exhaustion of tab-switching and context-switching. Nobody runs 'agency vs AI agent' comparison creative. Transparency messaging is completely unoccupied — Albert's black-box approach left the 'trust' lane wide open. Free tier positioning is underexploited — most competitors gate everything behind sales calls."""


FALLBACK_PREMIUM_BRANDS = """Premium Brand Benchmark (curated reference library):

Linear (Dev Tools) — Signature: Monochrome product screenshots with typographic precision. Technique: UI-as-hero — the product interface IS the ad creative. Transferable: Show Mia's chat interface as the focal visual — the conversation IS the product.

Ramp (Fintech) — Signature: Data cards as hero visuals on dark backgrounds, green accent. Technique: Metric-first — lead with a number, make it the biggest element. Transferable: 'Agency-level strategy, software-level speed' as oversized typography with chat proof.

Notion (Productivity) — Signature: Warm lifestyle photography with subtle product integration. Technique: Aspirational context — show the LIFE the product enables. Transferable: Marketer at a cafe, phone showing Mia chat managing campaigns mid-latte.

Stripe (Infrastructure) — Signature: Animated gradients, editorial typography, data visualizations. Technique: Technical credibility through visual sophistication. Transferable: Multi-platform connection visuals (Meta + Google + TikTok + Amazon) as polished flow diagrams.

Figma (Design) — Signature: Bold brand color, real collaboration screenshots, multiplayer cursors. Technique: Show the product in action with real content, not mockups. Transferable: Real Mia conversations with real campaign data (anonymized).

Rippling (Vertical SaaS) — Signature: Bold competitive callouts, side-by-side comparisons, confrontational tone. Technique: Name competitors directly, use before/after framing. Transferable: '5 dashboards vs. 1 conversation' or 'Suggestions vs. Actions' split-screen visuals.

Top 10 Transferable Techniques: 1. Linear — UI-as-hero, chat interface screenshot IS the ad. 2. Ramp — Metric-first, lead with the number not the feature. 3. Notion — Lifestyle-meets-UI, aspirational context + product. 4. Stripe — Editorial typography, type-driven layouts minimal imagery. 5. Rippling — Confrontational positioning, name the pain directly. 6. Figma — Real content not mockups, authenticity over polish theater. 7. Mercury — Extreme negative space, let one element breathe. 8. Framer — Motion-first, design for video/GIF even in static formats. 9. Brex — Data as drama, make charts/numbers the visual centerpiece. 10. Arc — Counter-positioning, 'not like other AI tools' brand voice."""


FALLBACK_TRENDS = """Current Creative Trends (2025-2026): 1. UI-as-Creative — Product screenshots/recordings as the primary ad visual. SaaS brands showing real interfaces outperform generic lifestyle imagery. 2. Metric-Led Hooks — Leading with a specific number ('40%', '3 minutes', '1 chat') as the largest visual element drives higher engagement. 3. Dark Mode Aesthetics — Dark backgrounds with bright accent colors feel more premium and stand out in bright Instagram feeds. 4. Typographic Dominance — Bold, oversized type with minimal supporting imagery. Let the words be the visual. 5. Split-Screen Contrast — Before/after, chaos/order, manual/automated side-by-side compositions. 6. Authentic Texture — Mixing photography with hand-drawn elements, annotations, or rough textures to combat AI-generated sterility. 7. Negative Space Maximalism — Ultra-clean layouts with one focal element surrounded by generous white/dark space. 8. Motion in Static — Implied motion through diagonal compositions, blur effects, or sequential frame layouts. 9. Confrontational Questions — Copy that starts with a direct, uncomfortable question ('Still managing ads across 5 different dashboards?'). 10. Social Proof as Visual — Review quotes, user counts, or platform logos as the hero graphic element."""


FALLBACK_AUDIENCE = """Audience: Digital Marketers, Agency Owners and Growth Teams Managing Paid Ads

Core Emotional Drivers: Dashboard fatigue — toggling between Meta Business Suite, Google Ads, TikTok, analytics, spreadsheets. Fear of missing optimization windows — campaigns underperform while they sleep or take a weekend off. Identity tension — they became marketers for strategy and creativity, not to babysit CPMs and adjust bids. Tool overwhelm — every new platform adds another login, another dashboard, another learning curve. Trust erosion — burned by 'AI-powered' tools that were just rule-based logic with a chatbot skin.

Aspiration Triggers: Managing all campaigns from one interface, in natural language — 'just tell it what to do'. Being the 'strategic brain' while AI handles the execution grunt work. Impressing clients (agencies) with faster turnaround, deeper insights, and 24/7 optimization. Having an AI teammate that actually ACTS — not one that generates a to-do list of suggestions. Replacing the agency retainer with something faster, cheaper, and more transparent.

Switching Triggers: A campaign burns budget overnight because they missed a metric spike. Realizing they spend 60% of their week on reporting theater, not strategy. A competitor agency delivers faster results with AI tooling. Hitting the limits of their current tool's 'AI' (which is really just rules). Getting a bill from Smartly or an agency and doing the ROI math. Losing a client because turnaround was too slow.

Language They Use: 'I need one place for everything.' 'I want to talk to my campaigns, not click through 20 menus.' 'My current tool does creative OR analytics, never both.' 'I need something that actually DOES things, not just suggests.' 'I want agency-quality work without the agency price tag.' 'I'm tired of being a button-pusher — I'm supposed to be a strategist.'

Unconventional Pain Points (Competitors Miss These): The cognitive cost of context-switching between platforms (not just 'time saved' — actual mental exhaustion). Reporting theater — spending hours making dashboards look good for clients/bosses instead of optimizing. AI trust gap — burned by tools that call themselves 'AI' but are just if/then rule engines. The loneliness of solo marketers and small agency owners with no team to bounce ideas off (Mia fills this gap). The 'black box' anxiety — Albert users who want AI autonomy but ALSO want to understand why. 'Cockpit fatigue' — power tools like Madgicx that require a pilot's license to operate."""


# ---------------------------------------------------------------------------
# Web Search Helper
# ---------------------------------------------------------------------------

def _web_search(query: str) -> str | None:
    """
    Run parallel-cli search as a subprocess. Returns raw JSON string,
    or None if parallel-cli is not installed or times out.
    """
    try:
        result = subprocess.run(
            [
                "parallel-cli", "search",
                "--query", query,
                "--output", "json",
                "--excerpt-limit", "20000",
            ],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
        return None
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        print("  ⚠ Web search timed out after 120s")
        return None
    except Exception as e:
        print(f"  ⚠ Web search error: {e}")
        return None


# ---------------------------------------------------------------------------
# LLM Synthesis Helper
# ---------------------------------------------------------------------------

def _synthesize_with_llm(
    content: str,
    instruction: str,
    api_key: str,
    model: str = "gemini-2.5-flash",
) -> str:
    """
    Send content to Google Gemini for analysis/synthesis.
    Falls back to truncated raw content on error.
    """
    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model,
            contents=content,
            config={
                "system_instruction": instruction,
                "max_output_tokens": 2000,
            },
        )

        if response.text:
            return response.text

        # Try to extract from candidates
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text

        return content[:3000]

    except Exception as e:
        print(f"  ⚠ LLM synthesis error: {e}")
        return content[:3000]


# ---------------------------------------------------------------------------
# 4 Research Tracks
# ---------------------------------------------------------------------------

def research_competitors(api_key: str | None = None) -> ResearchResult:
    """TRACK A — Competitor Ad Research."""
    print("  🔍 Track A: Competitor ad patterns...")

    query = (
        "Meta Facebook Instagram ads creative strategy for AI marketing agent "
        "platforms and ad tech tools. Include: Ryze AI, Smartly.io, Albert.ai, "
        "Madgicx, AdCreative.ai, Adzooma, Funnel.io, Supermetrics. "
        "What visual styles, messaging, and ad formats are they using in 2025-2026?"
    )

    instruction = (
        "You are a paid social creative strategist. Analyze these search results "
        "about AI marketing tool competitor ads. Extract: "
        "1. Common visual patterns (colors, layouts, imagery style) grouped by competitor tier. "
        "2. Copy/messaging patterns (hooks, CTAs, tone). "
        "3. Ad formats being used (static, carousel, video, stories). "
        "4. What's OVERUSED (visual sameness to avoid). "
        "5. Gaps and opportunities (what nobody is doing). "
        "Be specific and cite company names. Format as bullet points."
    )

    raw = _web_search(query) if api_key else None

    if raw and api_key:
        summary = _synthesize_with_llm(raw, instruction, api_key)
        return ResearchResult(track="competitor_ads", summary=summary, raw_data=raw, sources=["web_search"])
    else:
        print("    → Using curated fallback data")
        return ResearchResult(track="competitor_ads", summary=FALLBACK_COMPETITOR, sources=["fallback_curated"])


def research_premium_brands(
    brands: list[str] | None = None,
    api_key: str | None = None,
) -> ResearchResult:
    """TRACK B — Premium Software Brands."""
    print("  🔍 Track B: Premium brand benchmark...")

    query = (
        "Best most premium polished Meta Instagram Facebook ads from top software "
        "companies 2025 2026. Companies like Linear, Ramp, Notion, Stripe, Figma, "
        "Rippling. What makes their ad creative stand out? Visual techniques, "
        "design quality, scroll-stopping formats."
    )

    instruction = (
        "You are a world-class creative director analyzing the best software company "
        "ads across all verticals. For each brand mentioned, extract: "
        "1. Their signature visual technique (what makes their ads recognizable). "
        "2. How they achieve a 'premium' and 'polished' feel. "
        "3. Their copy approach (tone, structure, hooks). "
        "4. A specific transferable technique that an AI marketing agent company could adapt. "
        "Then produce a 'Top 10 Transferable Techniques' list ranked by applicability "
        "to an AI marketing agent targeting digital marketers and agency owners on Instagram. "
        "For each technique, label which company it comes from. "
        "Format with clear headers per brand and the ranked list at the end."
    )

    raw = _web_search(query) if api_key else None

    if raw and api_key:
        summary = _synthesize_with_llm(raw, instruction, api_key)
        return ResearchResult(track="premium_brands", summary=summary, raw_data=raw, sources=["web_search"])
    else:
        print("    → Using curated fallback data")
        return ResearchResult(track="premium_brands", summary=FALLBACK_PREMIUM_BRANDS, sources=["fallback_curated"])


def research_creative_trends(api_key: str | None = None) -> ResearchResult:
    """TRACK C — Creative Trends."""
    print("  🔍 Track C: Creative trends 2025-2026...")

    query = (
        "Best performing Meta Instagram ad creative trends 2025 2026. "
        "Scroll-stopping techniques for B2B SaaS ads. Premium polished ad design "
        "techniques. What ad formats and visual styles have highest CTR on "
        "Instagram feed and stories."
    )

    instruction = (
        "You are a paid social creative strategist. Extract the most actionable "
        "creative trends from these search results: "
        "1. Visual formats that are performing well (static, video, carousel, etc.). "
        "2. Design techniques that stop the scroll on Instagram. "
        "3. What makes an ad look 'premium' vs 'templated' in 2025-2026. "
        "4. Typography, color, and layout trends. "
        "5. Any emerging formats or techniques that are underused. "
        "Focus on techniques applicable to a B2B SaaS brand (AI marketing agent) "
        "advertising on Instagram to digital marketers and agency owners. "
        "Be specific and actionable. Format as a ranked list."
    )

    raw = _web_search(query) if api_key else None

    if raw and api_key:
        summary = _synthesize_with_llm(raw, instruction, api_key)
        return ResearchResult(track="creative_trends", summary=summary, raw_data=raw, sources=["web_search"])
    else:
        print("    → Using curated fallback data")
        return ResearchResult(track="creative_trends", summary=FALLBACK_TRENDS, sources=["fallback_curated"])


def research_audience_psychology(
    target_description: str,
    api_key: str | None = None,
) -> ResearchResult:
    """TRACK D — Audience Psychology."""
    print("  🔍 Track D: Audience psychology...")

    query = (
        "Digital marketer psychology buying behavior for AI marketing tools. "
        "What motivates them to switch ad management platforms. Pain points, "
        "aspirations, decision triggers for AI marketing agent adoption. "
        "Agency owners, growth marketers, DTC brand managers."
    )

    instruction = (
        f"You are a consumer psychologist specializing in B2B SMB buyers. "
        f"The target audience is: {target_description}. "
        "From these search results, extract: "
        "1. Core emotional drivers (what keeps them up at night). "
        "2. Aspiration triggers (what does 'success' look like to them). "
        "3. Switching triggers (what makes them finally change tools). "
        "4. Language they use (how they describe their own problems). "
        "5. What messaging hooks would resonate most. "
        "6. Unconventional pain points that competitors AREN'T addressing. "
        "Be specific to digital marketers and agency owners managing paid ads. "
        "Format as clear sections with bullet points."
    )

    raw = _web_search(query) if api_key else None

    if raw and api_key:
        summary = _synthesize_with_llm(raw, instruction, api_key)
        return ResearchResult(track="audience_psychology", summary=summary, raw_data=raw, sources=["web_search"])
    else:
        print("    → Using curated fallback data")
        return ResearchResult(track="audience_psychology", summary=FALLBACK_AUDIENCE, sources=["fallback_curated"])


# ---------------------------------------------------------------------------
# Research Orchestrator
# ---------------------------------------------------------------------------

def run_deep_research(
    competitors: list[str],
    premium_brands: list[str] | None,
    target_description: str,
    api_key: str,
) -> CreativeIntelligenceBrief:
    """
    Run all 4 research tracks sequentially, assemble a CreativeIntelligenceBrief.
    """
    print("\n🧠 Running Deep Creative Research...")
    print("=" * 60)

    # Track A — Competitors
    comp_result = research_competitors(api_key)

    # Track B — Premium Brands
    brand_result = research_premium_brands(premium_brands, api_key)

    # Track C — Trends
    trend_result = research_creative_trends(api_key)

    # Track D — Audience
    audience_result = research_audience_psychology(target_description, api_key)

    brief = CreativeIntelligenceBrief(
        competitor_patterns=comp_result.summary,
        premium_benchmark=brand_result.summary,
        trending_techniques=trend_result.summary,
        audience_insights=audience_result.summary,
        raw_results=[comp_result, brand_result, trend_result, audience_result],
    )

    # Print char counts
    print(f"\n📊 Research Summary:")
    print(f"  Track A (Competitors):    {len(comp_result.summary):,} chars")
    print(f"  Track B (Premium Brands): {len(brand_result.summary):,} chars")
    print(f"  Track C (Trends):         {len(trend_result.summary):,} chars")
    print(f"  Track D (Audience):       {len(audience_result.summary):,} chars")
    total = sum(len(r.summary) for r in brief.raw_results)
    print(f"  Total:                    {total:,} chars")
    print("=" * 60)

    return brief
