#!/usr/bin/env python3
"""
Generate precise slide wireframes (PNG) for the Mosaic Enterprise GTM deck.

We mirror the TLDR wireframe generator style (matplotlib + placeholder boxes)
but adapt slide count/layout to match:
`mosaic_enterprise_gtm_deck_outline.md` (Slides 1-20), including net-new:
- AI Ops slide (lead routing/scoring + 10x creative output)
- 3-month roadmap inserted after Risks & Mitigations
- Acquisition, Activation, Retention (AAR) slide
"""

import os
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.patches import FancyArrowPatch


# ── Color palette ──────────────────────────────────────────────────────
BG = "#1B2333"
CARD_BG = "#232F42"
TEAL = "#00BFA5"
WHITE = "#FFFFFF"
GRAY = "#8A94A6"
LTGRAY = "#C5CDD9"
DASHED = "#4A5568"
AMBER = "#FFB74D"
PURPLE = "#BB86FC"
BLUE = "#4FC3F7"
GREEN = "#66BB6A"
CORAL = "#F7768E"

SLIDE_W = 16
SLIDE_H = 9
TOTAL_SLIDES = 20

OUT_DIR = os.path.join(
    "outputs",
    "company case studies",
    "Mosaic",
    "wireframes",
)


SLIDE_META = {
    1: {
        "sub": "Setting the stage",
        "top": "AGENDA",
        "takeaway": "Two adoption engines (Creators; Enterprise + Agencies) supported by measurable intent → routing → onboarding.",
    },
    2: {
        "sub": "Mosaic adoption mandate",
        "top": "EXECUTIVE SUMMARY & THE MOSAIC MANDATE",
        "takeaway": "Sell workflow outcomes with enterprise governance + pipeline integration.",
    },
    3: {
        "sub": "Why Mosaic compounds",
        "top": "COMPETITIVE LANDSCAPE & STRUCTURAL MOAT",
        "takeaway": "Agentic workflow + multimodal intelligence + enterprise governance + API automation compound adoption.",
    },
    4: {
        "sub": "Why the old world breaks",
        "top": "THE EXHAUSTION OF TRADITIONAL VIDEO OPS",
        "takeaway": "Manual editing and fragmented toolchains fail at scale; Mosaic runs workflows on autopilot.",
    },
    5: {
        "sub": "Dual engine",
        "top": "TARGET AUDIENCES & IDENTIFICATION",
        "takeaway": "Creators optimize for time-to-first-output; Enterprise + Agencies optimize for governed, integrated pipelines.",
    },
    6: {
        "sub": "Conversion surfaces",
        "top": "WEBSITE & DIGITAL EXPERIENCE ALIGNMENT",
        "takeaway": "Activation surfaces for creators; trust narrative + technical credibility surfaces for teams and admins.",
    },
    7: {
        "sub": "Channel system",
        "top": "MARKETING CHANNELS & GO-TO-MARKET MECHANICS",
        "takeaway": "Use `paid, content, community, partnerships` with distinct B2C vs B2B (enterprise + agencies) channel motions.",
    },
    8: {
        "sub": "Professional virality",
        "top": "REFERRAL MECHANISMS & PROFESSIONAL VIRALITY",
        "takeaway": "Status-safe sharing + utility-rich workflows drive compounding adoption (not spammy referrals).",
    },
    9: {
        "sub": "Enterprise implementability",
        "top": "WHITE-GLOVE WORKFLOW IMPLEMENTATION",
        "takeaway": "Implementation is a marketing feature: map pipelines into Mosaic workflows with governance-ready onboarding.",
    },
    10: {
        "sub": "Intent → routing",
        "top": "TAM MAPPING & CRM AUTOMATION PLAYBOOK",
        "takeaway": "Tier accounts by intent + fit, then route with SLAs to demos and technical onboarding.",
    },
    11: {
        "sub": "Use-case empire",
        "top": "USE-CASE & MOTION PORTFOLIO",
        "takeaway": "Package B2C template/workflow families and B2B team motions into repeatable go-to-market surfaces.",
    },
    12: {
        "sub": "Orchestrated outbound",
        "top": "SALES & MARKETING SYMBIOSIS",
        "takeaway": "Signal dossiers align outbound messaging across Marketing and Sales for predictable conversion.",
    },
    13: {
        "sub": "Net new AI Ops slide",
        "top": "AI OPS (GTM AUTOMATION AGENTS)",
        "takeaway": "Automate demand gen execution (experiments, SEO, paid creative, social) with cross-channel intelligence feedback.",
    },
    14: {
        "sub": "Protect adoption trust",
        "top": "RISKS & MITIGATIONS",
        "takeaway": "Security, integration, quality, latency, and persona fit are solved with proactive operating mechanisms.",
    },
    15: {
        "sub": "Net new roadmap",
        "top": "3-MONTH ROADMAP (AFTER RISKS)",
        "takeaway": "Month 1 instruments + AI Ops MVP; Month 2 runs experiments; Month 3 scales winners and systematizes iteration.",
    },
    16: {
        "sub": "Lifecycle system",
        "top": "ACQUISITION, ACTIVATION, RETENTION (AAR)",
        "takeaway": "Growth quality improves when acquisition, activation, and retention are measured as one lifecycle system.",
    },
    17: {
        "sub": "The math",
        "top": "UNIT ECONOMICS & CAC PAYBACK",
        "takeaway": "Time saved + output multipliers create usage compounding; B2B expansion drives LTV via seats, workspaces, automation, API usage.",
    },
    18: {
        "sub": "How we measure success",
        "top": "DEFINING SUCCESS",
        "takeaway": "Measure activation + repeat usage for creators; measure demo-to-onboarding + governed expansion for teams and agencies.",
    },
    19: {
        "sub": "Alignment",
        "top": "THE UNASKED QUESTIONS",
        "takeaway": "Leadership aligns on data-handling guarantees, integration standardization, and first AI Ops priority.",
    },
    20: {
        "sub": "Wrap-up",
        "top": "CLOSING",
        "takeaway": "Mosaic wins by executing faster experiments and governed onboarding—powered by AI Ops.",
    },
}


def new_slide(fig_num: int):
    fig, ax = plt.subplots(1, 1, figsize=(SLIDE_W, SLIDE_H), num=fig_num)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, SLIDE_W)
    ax.set_ylim(0, SLIDE_H)
    ax.axis("off")
    return fig, ax


def draw_box(
    ax,
    x,
    y,
    w,
    h,
    label="",
    sublabel="",
    color=TEAL,
    dashed=False,
    fill=True,
    fontsize=9,
    sublabel_fontsize=7.5,
    header_height=None,
    text_color=WHITE,
):
    ls = "--" if dashed else "-"
    ec = DASHED if dashed else color
    fc = CARD_BG if fill else "none"
    rect = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.05",
        facecolor=fc,
        edgecolor=ec,
        linewidth=1.2,
        linestyle=ls,
    )
    ax.add_patch(rect)

    if header_height and label:
        header = FancyBboxPatch(
            (x, y + h - header_height),
            w,
            header_height,
            boxstyle="round,pad=0.05",
            facecolor=color,
            edgecolor=color,
            linewidth=0,
            alpha=0.25,
        )
        ax.add_patch(header)
        ax.text(
            x + w / 2,
            y + h - header_height / 2,
            label,
            ha="center",
            va="center",
            fontsize=fontsize,
            fontweight="bold",
            color=text_color,
            family="sans-serif",
        )
    elif label:
        ax.text(
            x + w / 2,
            y + h - 0.25,
            label,
            ha="center",
            va="top",
            fontsize=fontsize,
            fontweight="bold",
            color=text_color,
            family="sans-serif",
        )

    if sublabel:
        ax.text(
            x + w / 2,
            y + h / 2 - 0.1,
            sublabel,
            ha="center",
            va="center",
            fontsize=sublabel_fontsize,
            color=GRAY,
            family="sans-serif",
            style="italic",
            wrap=True,
        )


def apply_template(ax, slide_num: int, sub: str, top: str, takeaway: str):
    # Top title & subtitle
    ax.text(0.6, 8.2, top, fontsize=22, fontweight="bold", color=WHITE, family="sans-serif")
    ax.text(0.6, 7.65, sub, fontsize=12, color=TEAL, family="sans-serif", style="italic")
    ax.plot([0.6, 15.4], [7.35, 7.35], color=DASHED, linewidth=0.5)

    # Bottom teal accent bar
    rect = plt.Rectangle((0, 0), SLIDE_W, 0.08, facecolor=TEAL, edgecolor="none")
    ax.add_patch(rect)

    # Slide number badge
    ax.text(
        SLIDE_W - 0.4,
        0.45,
        str(slide_num),
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color=BG,
        family="sans-serif",
        bbox=dict(boxstyle="circle,pad=0.3", facecolor=TEAL, edgecolor="none"),
    )
    ax.text(
        0.6,
        0.45,
        f"SLIDE {slide_num} OF {TOTAL_SLIDES}",
        fontsize=8,
        color=GRAY,
        family="sans-serif",
        fontweight="bold",
    )
    ax.text(
        8.0,
        0.45,
        f"KEY TAKEAWAY: {takeaway}",
        fontsize=10,
        color=WHITE,
        family="sans-serif",
        fontweight="bold",
        ha="center",
        va="center",
    )


def wrap_lines(s: str, width: int = 26) -> str:
    return "\n".join(textwrap.wrap(s, width=width))


def save_slide(fig, name: str):
    os.makedirs(OUT_DIR, exist_ok=True)
    fig.savefig(
        os.path.join(OUT_DIR, name),
        dpi=150,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
        pad_inches=0.2,
    )
    plt.close(fig)


def slide_1():
    fig, ax = new_slide(1)
    meta = SLIDE_META[1]
    apply_template(ax, 1, meta["sub"], meta["top"], meta["takeaway"])

    draw_box(ax, 0.6, 1.2, 14.8, 7.0, color=TEAL, header_height=0.55, dashed=False)
    agenda = [
        "Status quo & adoption mandate",
        "Target audiences & delivery engine",
        "Marketing channels & GTM mechanics",
        "Website alignment & conversion surfaces",
        "Referral mechanics & professional virality",
        "White-glove implementation",
        "Sales symbiosis & CRM automation",
        "AI Ops (GTM automation agents)",
        "Risks & mitigations",
        "3-month roadmap",
        "Unit economics & success metrics",
    ]
    ax.text(2.0, 6.6, "AGENDA (DECK FLOW)", fontsize=10, fontweight="bold", color=TEAL, family="sans-serif")
    for i, item in enumerate(agenda):
        y = 6.0 - i * 0.35
        ax.text(1.0, y, f"• {wrap_lines(item, 28)}", fontsize=7.5, color=LTGRAY, family="sans-serif", va="center")

    save_slide(fig, "slide-01-agenda.png")
    print("✅ Slide 1 wireframe saved")


def slide_2():
    fig, ax = new_slide(2)
    meta = SLIDE_META[2]
    apply_template(ax, 2, meta["sub"], meta["top"], meta["takeaway"])

    draw_box(ax, 0.6, 3.0, 5.1, 4.0, color=TEAL, header_height=0.55)
    ax.text(3.15, 6.85, "WHERE WE ARE TODAY", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    items = [
        "Agentic AI video editing on a canvas",
        "Enterprise-ready governance (RBAC, audit logs)",
        "Integrations: MAM + NLE export/roundtrip",
        "Automation: triggers + batch processing + webhooks",
        "Security: SOC 2 Type II + zero retention/no training posture",
    ]
    for i, it in enumerate(items):
        ax.text(1.2, 6.2 - i * 0.7, f"• {wrap_lines(it, 22)}", fontsize=7.2, color=LTGRAY, family="sans-serif")

    draw_box(ax, 6.1, 3.0, 3.3, 4.0, color=BLUE, header_height=0.55)
    ax.text(7.75, 6.85, "THE MOSAIC MANDATE", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    mand = [
        "Sell workflow outcomes",
        "Creators: faster time-to-output",
        "Teams: governed, integrated pipelines",
        "Agencies: scalable client delivery",
    ]
    for i, it in enumerate(mand):
        ax.text(6.55, 6.2 - i * 0.9, f"• {wrap_lines(it, 24)}", fontsize=7.2, color=LTGRAY, family="sans-serif")

    draw_box(ax, 9.8, 3.0, 5.0, 4.0, color=PURPLE, header_height=0.55, dashed=True, fill=False)
    ax.text(12.3, 6.8, "[VISUAL]", ha="center", va="center", fontsize=14, fontweight="bold", color=DASHED)
    ax.text(12.3, 5.9, "Growth\nFlywheel\nDiagram", ha="center", va="center", fontsize=9, color=GRAY)

    draw_box(ax, 0.6, 1.2, 14.8, 1.3, color=AMBER, header_height=0.4)
    ax.text(8.0, 1.65, "STRATEGY: Dual Engine (B2C) + Integration-led Adoption (B2B)", ha="center", va="center", fontsize=9,
            color=WHITE, fontweight="bold", family="sans-serif")

    save_slide(fig, "slide-02-executive-summary.png")
    print("✅ Slide 2 wireframe saved")


def slide_3():
    fig, ax = new_slide(3)
    meta = SLIDE_META[3]
    apply_template(ax, 3, meta["sub"], meta["top"], meta["takeaway"])

    headers = ["COMPETITOR", "FOCUS", "MOSAIC ADVANTAGE"]
    xs = [1.6, 6.1, 10.8]
    for x, h in zip(xs, headers):
        ax.text(x, 6.85, h, ha="center", va="center", fontsize=8.5, fontweight="bold", color=TEAL, family="sans-serif")

    rows = [
        (
            "FLORA",
            "Unified creative environment with multi-model creation workflows.",
            "Stronger enterprise video operations: triggers, API/webhooks, MAM/NLE roundtrip, governance.",
        ),
        (
            "Weavy",
            "Node-based artistic creation and editing with broad model access.",
            "Clearer production infrastructure story: RBAC, auditability, implementation support.",
        ),
        (
            "Krea (Nodes)",
            "Visual node workflows for image/video generation and model chaining.",
            "More explicit team-grade operational editing and governed onboarding.",
        ),
        (
            "Kaiber Superstudio",
            "Infinite-canvas, flow-based AI creation for video/image/motion.",
            "Stronger end-to-end workflow implementation for production reliability.",
        ),
        (
            "ComfyUI",
            "Open-source node graph for flexible generative workflows.",
            "Lower enterprise adoption friction via managed UX and compliance-ready GTM.",
        ),
    ]
    start_y = 6.2
    for i, (a, b, c) in enumerate(rows):
        y = start_y - i * 1.2
        bg = CARD_BG if i % 2 == 0 else None
        if bg:
            ax.add_patch(plt.Rectangle((0.6, y - 0.55), 14.8, 0.95, facecolor=CARD_BG, edgecolor="none", alpha=0.35))
        ax.text(xs[0], y, a, ha="center", va="center", fontsize=8, color=WHITE, fontweight="bold")
        ax.text(xs[1], y, wrap_lines(b, 30), ha="center", va="center", fontsize=7.0, color=LTGRAY, family="sans-serif")
        ax.text(xs[2], y, wrap_lines(c, 34), ha="center", va="center", fontsize=6.9, color=LTGRAY, family="sans-serif")

    draw_box(ax, 0.6, 1.2, 14.8, 1.8, color=TEAL, header_height=0.45)
    ax.text(1.2, 2.5, "OUR STRUCTURAL MOAT:", fontsize=10, fontweight="bold", color=TEAL, family="sans-serif")
    ax.text(4.0, 2.5, "Agentic node-based workflow execution + multimodal intelligence + enterprise governance + pipeline integrations + API automation.",
            fontsize=7.8, color=LTGRAY, family="sans-serif", va="center")

    save_slide(fig, "slide-03-competitive-landscape.png")
    print("✅ Slide 3 wireframe saved")


def slide_4():
    fig, ax = new_slide(4)
    meta = SLIDE_META[4]
    apply_template(ax, 4, meta["sub"], meta["top"], meta["takeaway"])

    exhaust = [
        ("Manual bottlenecks", "Repetitive tasks dominate; consistency suffers", CORAL),
        ("Fragmented toolchains", "MAM, NLE, export, and publishing are disconnected", AMBER),
        ("Enterprise adoption friction", "RBAC/audit/data-retention reviews slow rollouts", BLUE),
        ("Workflow mismatch", "Tools show outputs; teams need pipeline integration", PURPLE),
    ]

    bw = 3.4
    bh = 3.7
    for i, (title, desc, color) in enumerate(exhaust):
        col = i % 2
        row = i // 2
        x = 0.6 + col * 7.3
        y = 4.2 - row * 3.9
        draw_box(ax, x, y, bw * 2 - 0.1, bh, color=color, header_height=0.55)
        ax.text(x + 3.3, y + bh - 0.25, title, ha="center", va="top", fontsize=9, fontweight="bold", color=WHITE)
        ax.text(x + 3.3, y + bh - 1.0, wrap_lines(desc, 34), ha="center", va="center", fontsize=7.2, color=LTGRAY, family="sans-serif")

    draw_box(ax, 0.6, 1.2, 14.8, 1.8, color=TEAL)
    ax.text(7.9, 2.35, "Structural inversion: build in the canvas → run workflows on autopilot → integrate into the production pipeline with governance-first security.",
            ha="center", va="center", fontsize=7.8, color=LTGRAY, family="sans-serif")

    save_slide(fig, "slide-04-exhaustion.png")
    print("✅ Slide 4 wireframe saved")


def slide_5():
    fig, ax = new_slide(5)
    meta = SLIDE_META[5]
    apply_template(ax, 5, meta["sub"], meta["top"], meta["takeaway"])

    # Top-left: B2C 3-column chart
    draw_box(ax, 0.6, 3.2, 7.2, 4.7, color=TEAL, header_height=0.55)
    ax.text(4.2, 7.6, "B2C AUDIENCE CHART (AUDIENCE | VALUE | WANT)", ha="center", va="center", fontsize=8.3, fontweight="bold", color=WHITE)
    b2c_headers = ["AUDIENCE", "VALUE", "WANT"]
    b2c_x = [1.9, 4.2, 6.5]
    for x, h in zip(b2c_x, b2c_headers):
        ax.text(x, 7.1, h, ha="center", va="center", fontsize=7.0, fontweight="bold", color=TEAL, family="sans-serif")

    b2c_rows = [
        ("Creator-Entrepreneurs", "Speed + volume", "Prompt-to-publish repurposing"),
        ("In-house Creative Teams", "Consistency + collaboration", "Reusable templates + shared assets"),
        ("Agency/Freelance Editors", "Throughput + quality control", "Multi-client workflow reliability"),
    ]
    start_y = 6.5
    for i, (a, b, c) in enumerate(b2c_rows):
        y = start_y - i * 1.0
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((0.8, y - 0.43), 6.8, 0.78, facecolor=CARD_BG, edgecolor="none", alpha=0.35))
        ax.text(b2c_x[0], y, wrap_lines(a, 16), ha="center", va="center", fontsize=6.7, color=WHITE, fontweight="bold")
        ax.text(b2c_x[1], y, wrap_lines(b, 16), ha="center", va="center", fontsize=6.7, color=LTGRAY, family="sans-serif")
        ax.text(b2c_x[2], y, wrap_lines(c, 20), ha="center", va="center", fontsize=6.6, color=LTGRAY, family="sans-serif")

    # Top-right: B2B buying committee 3-column table
    draw_box(ax, 8.0, 3.2, 7.2, 4.7, color=PURPLE, header_height=0.55)
    ax.text(11.6, 7.6, "B2B BUYING COMMITTEE (COMMITTEE | TARGET | PAIN)", ha="center", va="center", fontsize=8.3, fontweight="bold", color=WHITE)
    b2b_headers = ["BUYING COMMITTEE", "TARGET", "PAIN POINT"]
    b2b_x = [9.1, 11.4, 13.7]
    for x, h in zip(b2b_x, b2b_headers):
        ax.text(x, 7.1, h, ha="center", va="center", fontsize=6.7, fontweight="bold", color=PURPLE, family="sans-serif")

    b2b_rows = [
        ("Champion", "Production/Media Ops Owner", "Throughput bottlenecks + missed SLAs"),
        ("Economic Buyer", "Editors Lead / Head of Creative", "Cost per asset rising; hard to scale quality"),
        ("Technical Evaluator", "IT / Security", "Access control and auditability risk"),
    ]
    start_y = 6.5
    for i, (a, b, c) in enumerate(b2b_rows):
        y = start_y - i * 1.0
        if i % 2 == 0:
            ax.add_patch(plt.Rectangle((8.2, y - 0.43), 6.8, 0.78, facecolor=CARD_BG, edgecolor="none", alpha=0.35))
        ax.text(b2b_x[0], y, wrap_lines(a, 14), ha="center", va="center", fontsize=6.7, color=WHITE, fontweight="bold")
        ax.text(b2b_x[1], y, wrap_lines(b, 18), ha="center", va="center", fontsize=6.4, color=LTGRAY, family="sans-serif")
        ax.text(b2b_x[2], y, wrap_lines(c, 20), ha="center", va="center", fontsize=6.3, color=LTGRAY, family="sans-serif")

    # Bottom: ABM execution flow
    draw_box(ax, 0.6, 1.2, 14.8, 1.7, color=BLUE, header_height=0.45)
    ax.text(8.0, 2.55, "ABM DATA EXECUTION FLOW", ha="center", va="center", fontsize=8.8, fontweight="bold", color=WHITE)
    ax.text(8.0, 1.95, "Technographic base  →  Firmographic filter  →  Persona mapping", ha="center", va="center",
            fontsize=8.0, color=LTGRAY, family="sans-serif", fontweight="bold")

    save_slide(fig, "slide-05-target-audience.png")
    print("✅ Slide 5 wireframe saved")


def slide_6():
    fig, ax = new_slide(6)
    meta = SLIDE_META[6]
    apply_template(ax, 6, meta["sub"], meta["top"], meta["takeaway"])

    # Top-left: B2C
    draw_box(ax, 0.6, 4.8, 5.0, 2.7, color=TEAL, header_height=0.55)
    ax.text(3.1, 7.25, "B2C LANDING / ACTIVATION", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    b2c = [
        "Templates across formats",
        "Agentic prompt-to-edit",
        "Content engine / autopilot editing",
    ]
    for i, it in enumerate(b2c):
        ax.text(1.2, 6.8 - i * 0.45, f"• {it}", fontsize=7.0, color=LTGRAY, family="sans-serif")

    # Top-right: B2B /enterprise
    draw_box(ax, 5.9, 4.8, 10.0, 2.7, color=PURPLE, header_height=0.55)
    ax.text(10.9, 7.25, "B2B /ENTERPRISE CONVERSION TRUST LAYER", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    b2b = [
        "RBAC + shared workspaces + asset library + audit logs",
        "Integrations: MAM/storage + NLE export/roundtrip (XML)",
        "Custom automations + full API + webhooks",
        "Security: SOC 2 Type II + zero retention/no training posture",
    ]
    for i, it in enumerate(b2b):
        ax.text(6.3, 6.85 - i * 0.46, f"• {wrap_lines(it, 34)}", fontsize=6.6, color=LTGRAY, family="sans-serif")

    # Mid: PLG interactive tools
    draw_box(ax, 0.6, 2.4, 14.8, 2.1, color=BLUE, header_height=0.45)
    ax.text(8.0, 4.15, "PLG INTERACTIVE TOOLS (AHA BEFORE SIGNUP)", ha="center", va="center", fontsize=8.7, fontweight="bold", color=WHITE)
    tools = [
        "Sandbox interactive demo (guided UI workflow run)",
        "Workflow ROI calculator",
        "Template-to-outcome wizard",
        "Integration readiness checker",
    ]
    for i, it in enumerate(tools):
        ax.text(1.3 + i * 3.7, 3.35, wrap_lines(it, 24), ha="center", va="center", fontsize=6.8, color=LTGRAY, family="sans-serif")

    # Bottom: conversion assets strip
    draw_box(ax, 0.6, 1.2, 14.8, 1.0, color=AMBER, header_height=0.35)
    ax.text(8.0, 1.65, "Conversion surfaces: Get Started, Templates, Automation, API Docs, and Book a Demo",
            ha="center", va="center", fontsize=7.2, color=LTGRAY, family="sans-serif")

    save_slide(fig, "slide-06-digital-experience.png")
    print("✅ Slide 6 wireframe saved")


def slide_7():
    fig, ax = new_slide(7)
    meta = SLIDE_META[7]
    apply_template(ax, 7, meta["sub"], meta["top"], meta["takeaway"])

    # B2C left
    draw_box(ax, 0.6, 2.7, 7.2, 4.3, color=TEAL, header_height=0.55)
    ax.text(4.2, 6.7, "B2C CHANNEL MIX (INDIVIDUAL CREATORS)", ha="center", va="center", fontsize=8.7, fontweight="bold", color=WHITE)
    b2c = [
        "Product-led templates + shareable workflows",
        "Paid acquisition for template discovery + first runs",
        "Content + SEO scaling: workflow outcomes (not slop)",
        "Community + partnerships: trust transfer + iterative feedback",
    ]
    for i, it in enumerate(b2c):
        ax.text(1.4, 6.2 - i * 0.8, f"• {wrap_lines(it, 30)}", fontsize=7.2, color=LTGRAY, family="sans-serif")

    # B2B right
    draw_box(ax, 8.2, 2.7, 7.2, 4.3, color=PURPLE, header_height=0.55)
    ax.text(11.8, 6.7, "B2B CHANNEL MIX (ENTERPRISE + AGENCIES)", ha="center", va="center", fontsize=8.7, fontweight="bold", color=WHITE)
    b2b = [
        "AI ABM outbound (enterprise + agencies) using intent surfaces",
        "Dark funnel inbound acceleration: /enterprise + automation/API triggers",
        "Champion move tracking for agency/exec lead changes",
        "B2B paid social: outcome + governance framing",
    ]
    for i, it in enumerate(b2b):
        ax.text(9.0, 6.2 - i * 0.8, f"• {wrap_lines(it, 30)}", fontsize=7.2, color=LTGRAY, family="sans-serif")

    # Budget/operating callout
    draw_box(ax, 0.6, 1.2, 14.8, 1.3, color=AMBER, header_height=0.4)
    ax.text(
        8.0,
        1.8,
        "Budget principle (first 90 days): B2C experimentation for activation + B2B ABM + intent infra tied to demo conversion.",
        ha="center",
        va="center",
        fontsize=8.2,
        color=LTGRAY,
        family="sans-serif",
        fontweight="bold",
    )

    save_slide(fig, "slide-07-channel-mix.png")
    print("✅ Slide 7 wireframe saved")


def slide_8():
    fig, ax = new_slide(8)
    meta = SLIDE_META[8]
    apply_template(ax, 8, meta["sub"], meta["top"], meta["takeaway"])

    cards = [
        ("OPEN WORKFLOW HUB", "GitHub-like repos for creator workflows with version history", TEAL),
        ("UGC WORKFLOW VIDEOS", "Creators share workflow runs/outcomes on LinkedIn + Instagram (deep-link to repos)", BLUE),
        ("FORK + REMIX", "Creators build on top of each other and republish improved workflows", PURPLE),
        ("EARLY ACCESS", "Referral to new workflows/agent packs", AMBER),
        ("NETWORK FLYWHEEL", "More creators → more workflows → more value → more creators", GREEN),
    ]

    # 5 cards across
    start_x = 0.6
    gap = 0.3
    card_w = (14.8 - gap * 4) / 5
    y = 2.4
    h = 4.7
    for i, (title, desc, color) in enumerate(cards):
        x = start_x + i * (card_w + gap)
        draw_box(ax, x, y, card_w, h, color=color, header_height=0.45)
        ax.text(x + card_w / 2, y + h - 0.28, title, ha="center", va="top", fontsize=8.2, fontweight="bold", color=WHITE)
        ax.text(x + card_w / 2, y + h - 1.2, wrap_lines(desc, 22), ha="center", va="center", fontsize=6.9, color=LTGRAY, family="sans-serif")

    draw_box(ax, 0.6, 1.2, 14.8, 1.1, color=CORAL, header_height=0.4)
    ax.text(
        8.0,
        1.75,
        "Fraud prevention: credit referrals only when adoption signals show meaningful workflow usage (anti-bot).",
        ha="center",
        va="center",
        fontsize=7.8,
        color=LTGRAY,
        family="sans-serif",
    )

    save_slide(fig, "slide-08-referral-mechanisms.png")
    print("✅ Slide 8 wireframe saved")


def slide_9():
    fig, ax = new_slide(9)
    meta = SLIDE_META[9]
    apply_template(ax, 9, meta["sub"], meta["top"], meta["takeaway"])

    # Left Problem/Right Solution
    draw_box(ax, 0.6, 4.9, 6.9, 3.0, color=CORAL, header_height=0.55)
    ax.text(4.05, 7.5, "THE PROBLEM", ha="center", va="center", fontsize=10, fontweight="bold", color=WHITE)
    prob = [
        "Teams don't buy edits; they buy reliability.",
        "Implementation variance kills adoption.",
        "Security + governance reviews slow pilots.",
    ]
    for i, it in enumerate(prob):
        ax.text(1.0 + i * 0, 6.9 - i * 0.7, f"• {wrap_lines(it, 28)}", fontsize=7.2, color=LTGRAY, family="sans-serif")

    draw_box(ax, 7.6, 4.9, 6.9, 3.0, color=GREEN, header_height=0.55)
    ax.text(11.05, 7.5, "THE WHITE-GLOVE SOLUTION", ha="center", va="center", fontsize=10, fontweight="bold", color=WHITE)
    sol = [
        "Workshop pipeline mapping: assets → workflow → exports → delivery",
        "Governance-ready setup (RBAC + audit log expectations)",
        "Automation/API integration + post-onboarding success review",
    ]
    for i, it in enumerate(sol):
        ax.text(8.0, 6.9 - i * 0.72, f"• {wrap_lines(it, 32)}", fontsize=7.0, color=LTGRAY, family="sans-serif")

    # Bottom checklist
    draw_box(ax, 0.6, 1.2, 14.8, 3.3, color=AMBER, header_height=0.45)
    ax.text(7.9, 4.05, "IMPLEMENTATION DELIVERABLES (EXAMPLES)", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    checklist = [
        "MAM/storage integration plan + auto-ingest expectations",
        "NLE roundtrip export plan (XML timeline) + validation",
        "Event-driven triggers + batch processing rules",
        "Security/compliance readiness pack (SOC 2 + data posture)",
        "Custom automations + webhooks wiring + ownership handoff",
    ]
    for i, it in enumerate(checklist):
        ax.text(1.2, 3.5 - i * 0.45, f"• {wrap_lines(it, 38)}", fontsize=7.1, color=LTGRAY, family="sans-serif")

    save_slide(fig, "slide-09-white-glove.png")
    print("✅ Slide 9 wireframe saved")


def slide_10():
    fig, ax = new_slide(10)
    meta = SLIDE_META[10]
    apply_template(ax, 10, meta["sub"], meta["top"], meta["takeaway"])

    # Top: three-tier
    tier_colors = [TEAL, BLUE, LTGRAY]
    tiers = [
        ("TIER 1: HYPER-INTENT", "Enterprise surface engagement + automation/API interest → immediate technical demo routing", TEAL),
        ("TIER 2: CORE TAM", "ICP match; intent warming → guided value onboarding + demo readiness", BLUE),
        ("TIER 3: LONG-TERM", "Adjacent fit; nurture only → integration/security thought leadership", LTGRAY),
    ]
    y0 = 4.9
    bh = 3.3
    for i, (title, desc, color) in enumerate(tiers):
        x = 0.6 + i * 5.05
        draw_box(ax, x, y0, 4.7, bh, color=color, header_height=0.5)
        ax.text(x + 2.35, y0 + bh - 0.25, title, ha="center", va="top", fontsize=8.2, fontweight="bold", color=WHITE)
        ax.text(x + 2.35, y0 + 2.5, wrap_lines(desc, 28), ha="center", va="center", fontsize=7.0, color=LTGRAY, family="sans-serif")

    # Bottom: CRM SLA
    draw_box(ax, 0.6, 1.2, 14.8, 3.2, color=AMBER, header_height=0.45)
    ax.text(7.9, 3.55, "CRM SLA (INTENT → ROUTING)", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    steps = [
        "Engagement triggers → route decision",
        "Owner assignment (B2C growth / B2B AE / technical pre-sales)",
        "Slack alert + handoff checklist",
        "Fast follow-up SLA for high-intent moments",
    ]
    for i, it in enumerate(steps):
        ax.text(2.0 + i * 3.8, 3.05, wrap_lines(it, 25), ha="center", va="center", fontsize=7.1, color=LTGRAY, family="sans-serif")

    save_slide(fig, "slide-10-tam-mapping.png")
    print("✅ Slide 10 wireframe saved")


def slide_11():
    fig, ax = new_slide(11)
    meta = SLIDE_META[11]
    apply_template(ax, 11, meta["sub"], meta["top"], meta["takeaway"])

    # Left B2C
    draw_box(ax, 0.6, 3.3, 7.2, 5.0, color=TEAL, header_height=0.55)
    ax.text(4.2, 8.0, "B2C: WORKFLOW / TEMPLATE FAMILIES", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    b2c = [
        "Talking Heads: captions + story rough cuts",
        "Vlogs: pacing + music + b-roll suggestions",
        "Podcasts: silence removal + intros/outros + watermarks",
        "Webinars/Keynotes: highlight extraction + reframing",
        "Clips/Montages: beat-matched repurposing",
    ]
    for i, it in enumerate(b2c):
        ax.text(1.2, 7.3 - i * 0.8, f"• {wrap_lines(it, 32)}", fontsize=7.2, color=LTGRAY, family="sans-serif")

    # Right B2B
    draw_box(ax, 8.0, 3.3, 7.2, 5.0, color=PURPLE, header_height=0.55)
    ax.text(11.6, 8.0, "B2B: TEAM MOTIONS (ENTERPRISE + AGENCIES)", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    b2b = [
        "Production pipelines: automation + throughput",
        "Editor collaboration: RBAC + audit trails",
        "Ops scheduling: autopilot publishing + notifications",
        "Integrations: MAM/storage + NLE roundtrip",
        "Agencies: scalable client delivery + governance across projects",
    ]
    for i, it in enumerate(b2b):
        ax.text(8.4, 7.3 - i * 0.8, f"• {wrap_lines(it, 30)}", fontsize=7.1, color=LTGRAY, family="sans-serif")

    # Bottom note
    draw_box(ax, 0.6, 1.2, 14.8, 1.8, color=AMBER)
    ax.text(8.0, 2.1, "Value packaging: templates drive activation; workflow outcomes drive enterprise onboarding conversion.", ha="center", va="center",
            fontsize=8.0, color=LTGRAY, family="sans-serif", fontweight="bold")

    save_slide(fig, "slide-11-use-case-empire.png")
    print("✅ Slide 11 wireframe saved")


def slide_12():
    fig, ax = new_slide(12)
    meta = SLIDE_META[12]
    apply_template(ax, 12, meta["sub"], meta["top"], meta["takeaway"])

    # Left: Signal Dossier
    draw_box(ax, 0.6, 4.8, 7.2, 3.4, color=TEAL, header_height=0.55)
    ax.text(4.2, 8.0, "SIGNAL DOSSIER (MQL → SQL)", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    dossier = [
        "Company/team context (enterprise vs agency)",
        "Engagement report (enterprise, templates, automation, API intent)",
        "Recommended pitch angle (workflow outcome + governance proof + integration plan)",
    ]
    for i, it in enumerate(dossier):
        ax.text(1.2, 7.4 - i * 0.9, f"• {wrap_lines(it, 30)}", fontsize=7.2, color=LTGRAY, family="sans-serif")

    # Right: Sales feedback loop
    draw_box(ax, 7.9, 4.8, 7.2, 3.4, color=BLUE, header_height=0.55)
    ax.text(11.5, 8.0, "FEEDBACK LOOP + ENABLEMENT", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    loop = [
        "Bi-weekly pipeline councils (messages, routing, channel allocation)",
        "Competitor battlecards (outcome + governance vs 'demo-only' tools)",
        "Positioning guides (creator vs editor vs admin messaging)",
    ]
    for i, it in enumerate(loop):
        ax.text(8.6, 7.4 - i * 0.9, f"• {wrap_lines(it, 30)}", fontsize=7.0, color=LTGRAY, family="sans-serif")

    # Bottom: Dark funnel air cover
    draw_box(ax, 0.6, 1.2, 14.8, 3.2, color=AMBER, header_height=0.45)
    ax.text(8.0, 3.85, "DARK FUNNEL AIR COVER (RETARGETING + TIMING)", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    air = [
        "Run paid/content retargeting aligned to enterprise intent triggers",
        "Mirror outreach angles while Sales calls are active",
        "Measure cohort conversion from intent surfaces → onboarding starts",
    ]
    for i, it in enumerate(air):
        ax.text(2.0 + i * 4.6, 3.2 - i * 0.32, wrap_lines(it, 26), ha="center", va="center",
                fontsize=7.1, color=LTGRAY, family="sans-serif")

    save_slide(fig, "slide-12-sales-symbiosis.png")
    print("✅ Slide 12 wireframe saved")


def slide_13():
    fig, ax = new_slide(13)
    meta = SLIDE_META[13]
    apply_template(ax, 13, meta["sub"], meta["top"], meta["takeaway"])

    # 5 agent boxes (CEO + Engineering demand gen + cross-channel intelligence)
    agents = [
        ("Growth Hacker Agent", "Prioritize experiments via ICE + design viral/UGC loops", TEAL),
        ("Programmatic SEO Agent", "Generate SEO page specs/drafts from templates + outcomes", BLUE),
        ("Ad Creative Agent", "Produce ad copy + creative direction briefs for testing", PURPLE),
        ("Social Content Agent", "Turn workflows into LinkedIn/Instagram carousels + reels", AMBER),
        ("Marketing Intelligence Agent", "Cross-channel performance analysis via APIs/MCPs (paid + content + SEO)", GREEN),
    ]
    box_w = 2.7
    box_h = 3.3
    start_x = 0.6
    start_y = 4.2
    gap_x = 0.2
    for i, (title, desc, color) in enumerate(agents):
        x = start_x + i * (box_w + gap_x)
        y = start_y
        draw_box(ax, x, y, box_w, box_h, color=color, header_height=0.5)
        ax.text(x + box_w / 2, y + box_h - 0.2, title, ha="center", va="top", fontsize=7.8, fontweight="bold", color=WHITE)
        ax.text(x + box_w / 2, y + 1.95, wrap_lines(desc, 18), ha="center", va="center", fontsize=6.4, color=LTGRAY, family="sans-serif")

    # Bottom demand-gen operating cadence strip
    draw_box(ax, 0.6, 1.2, 14.8, 2.7, color=GREEN, header_height=0.45)
    ax.text(8.0, 3.55, "OPERATING SLAs (EXAMPLES)", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    slas = [
        "Experiments: weekly backlog refresh + ICE prioritization",
        "SEO output: weekly page batch ready for publishing",
        "Creative output: rapid variations within days when metrics move",
        "Distribution: weekly social scheduling queue + UGC prompt support",
        "Intelligence: weekly cross-channel performance report + experiment updates",
    ]
    for i, it in enumerate(slas):
        ax.text(1.5 + i * 3.0, 2.7, wrap_lines(it, 26), ha="center", va="center", fontsize=6.9, color=LTGRAY, family="sans-serif")

    save_slide(fig, "slide-13-ai-ops.png")
    print("✅ Slide 13 wireframe saved")


def slide_14():
    fig, ax = new_slide(14)
    meta = SLIDE_META[14]
    apply_template(ax, 14, meta["sub"], meta["top"], meta["takeaway"])

    risks = [
        ("SECURITY TRUST", "SOC 2 + data posture may be questioned", "Security collateral + onboarding checklist", TEAL),
        ("INTEGRATION FRICTION", "Pipeline mapping variance slows adoption", "Standard playbooks + white-glove edge support", BLUE),
        ("QUALITY / ADOPTION", "Users doubt output reliability", "Template-driven workflows + quality review loop", PURPLE),
        ("ENTERPRISE LATENCY", "Sales cycle delays conversion", "Intent routing + technical demo readiness gates + SLAs", AMBER),
        ("PERSONA MISMATCH", "Creators vs admins vs ops see different messages", "Persona-specific messaging pillars and funnel content", CORAL),
    ]
    bw = 7.2
    bh = 2.3
    for i, (title, risk, mit, color) in enumerate(risks):
        col = i % 2
        row = i // 2
        x = 0.6 + col * (bw + 0.4)
        y = 5.6 - row * (bh + 0.35)
        if y < 1.2:
            break
        draw_box(ax, x, y, bw, bh, color=color, header_height=0.45)
        ax.text(x + bw / 2, y + bh - 0.2, title, ha="center", va="top", fontsize=8.5, fontweight="bold", color=WHITE)
        ax.text(x + 0.35, y + bh - 0.75, f"⚠ {wrap_lines(risk, 32)}", ha="left", va="center", fontsize=7.1, color=CORAL, family="sans-serif")
        ax.text(x + 0.35, y + bh - 1.2, f"✓ MITIGATION: {wrap_lines(mit, 28)}", ha="left", va="center", fontsize=6.6, color=LTGRAY, family="sans-serif")

    save_slide(fig, "slide-14-risks-mitigations.png")
    print("✅ Slide 14 wireframe saved")


def slide_15():
    fig, ax = new_slide(15)
    meta = SLIDE_META[15]
    apply_template(ax, 15, meta["sub"], meta["top"], meta["takeaway"])

    draw_box(ax, 0.6, 7.2, 14.8, 0.95, color=AMBER, header_height=0.35)
    ax.text(8.0, 7.68, "3-MONTH EXECUTION PLAN (MONTH 1 → 3)", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)

    phases = [
        ("MONTH 1\nFOUNDATION\nINSTRUMENTATION", TEAL, [
            "Align ICP + messaging pillars (B2C + B2B; enterprise + agencies)",
            "Instrument intent surfaces (enterprise, templates, automation, API)",
            "Ship AI Ops MVP: routing + scoring",
            "Produce first template packs + security/integration collateral",
        ]),
        ("MONTH 2\nEXPERIMENTATION", BLUE, [
            "B2C: paid experiments + workflow content + community edit challenges",
            "B2B: ABM outbound + dark funnel triggers + security/integration content",
            "Launch 2-4 creator/agency partnerships tied to conversion metrics",
        ]),
        ("MONTH 3\nSCALE WINNERS", PURPLE, [
            "Double down on highest demo-to-onboarding conversion channels/angles",
            "Expand workflow + integration templates for repeatable onboarding",
            "Scale AI Ops creative output into weekly routine",
        ]),
    ]
    phase_w = 4.8
    phase_gap = 0.3
    for i, (title, color, items) in enumerate(phases):
        x = 0.6 + i * (phase_w + phase_gap)
        y = 3.7
        draw_box(ax, x, y, phase_w, 3.6, color=color, header_height=0.6)
        ax.text(x + phase_w / 2, y + 3.4, title, ha="center", va="center", fontsize=8.2, fontweight="bold", color=WHITE)
        for ii, it in enumerate(items):
            ax.text(x + 0.35, y + 2.6 - ii * 0.55, f"• {wrap_lines(it, 26)}", fontsize=7.0, color=LTGRAY, family="sans-serif")

    save_slide(fig, "slide-15-roadmap-3-months.png")
    print("✅ Slide 15 wireframe saved")


def slide_16():
    fig, ax = new_slide(16)
    meta = SLIDE_META[16]
    apply_template(ax, 16, meta["sub"], meta["top"], meta["takeaway"])

    # Acquisition
    draw_box(ax, 0.6, 3.3, 4.7, 4.8, color=TEAL, header_height=0.55)
    ax.text(2.95, 7.8, "ACQUISITION", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    acq = [
        "B2C: template discovery via paid/content/community/partnerships",
        "B2B: enterprise + agency pipeline via ABM + intent routing",
        "Quality gate: qualified entry, not vanity traffic",
    ]
    for i, it in enumerate(acq):
        ax.text(0.9, 7.1 - i * 1.0, f"• {wrap_lines(it, 24)}", fontsize=7.0, color=LTGRAY, family="sans-serif")

    # Activation
    draw_box(ax, 5.65, 3.3, 4.7, 4.8, color=BLUE, header_height=0.55)
    ax.text(8.0, 7.8, "ACTIVATION", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    act = [
        "B2C event: first usable output from template/agent run",
        "B2B event: first successful team workflow run",
        "Levers: template-first onboarding + fast technical handoff",
    ]
    for i, it in enumerate(act):
        ax.text(5.95, 7.1 - i * 1.0, f"• {wrap_lines(it, 24)}", fontsize=7.0, color=LTGRAY, family="sans-serif")

    # Retention
    draw_box(ax, 10.7, 3.3, 4.7, 4.8, color=PURPLE, header_height=0.55)
    ax.text(13.05, 7.8, "RETENTION", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    ret = [
        "B2C: repeat runs + repurposing + workflow reuse",
        "B2B: workspace depth + collaborator growth + trigger/API expansion",
        "Guardrails: quality loops + persona-specific nurture",
    ]
    for i, it in enumerate(ret):
        ax.text(11.0, 7.1 - i * 1.0, f"• {wrap_lines(it, 24)}", fontsize=7.0, color=LTGRAY, family="sans-serif")

    draw_box(ax, 0.6, 1.2, 14.8, 1.8, color=AMBER)
    ax.text(
        8.0,
        2.05,
        "AAR north stars: Cost per activated creator • Time-to-first-value • Repeat-run/workspace expansion rates.",
        ha="center",
        va="center",
        fontsize=8.0,
        color=LTGRAY,
        family="sans-serif",
        fontweight="bold",
    )

    save_slide(fig, "slide-16-aar.png")
    print("✅ Slide 16 wireframe saved")


def slide_17():
    fig, ax = new_slide(17)
    meta = SLIDE_META[17]
    apply_template(ax, 17, meta["sub"], meta["top"], meta["takeaway"])

    # B2C economics
    draw_box(ax, 0.6, 3.3, 7.2, 4.8, color=TEAL, header_height=0.55)
    ax.text(4.2, 7.8, "B2C ECONOMICS (CREATORS)", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    b2c = [
        "Activation: time-to-first-output",
        "Retention: repeat runs + workflow reuse",
        "CAC drivers: template-first PLG + paid experiments",
        "North Star: cost per activated creator",
    ]
    for i, it in enumerate(b2c):
        ax.text(1.1, 7.1 - i * 0.85, f"• {wrap_lines(it, 32)}", fontsize=7.2, color=LTGRAY, family="sans-serif")

    # B2B economics
    draw_box(ax, 8.0, 3.3, 7.2, 4.8, color=PURPLE, header_height=0.55)
    ax.text(11.6, 7.8, "B2B ECONOMICS (ENTERPRISE + AGENCIES)", ha="center", va="center", fontsize=9, fontweight="bold", color=WHITE)
    b2b = [
        "Higher CAC (technical + security onboarding)",
        "Compounding LTV via shared workspaces + automation + API usage",
        "Measure: demo-to-onboarding and pipeline influenced",
    ]
    for i, it in enumerate(b2b):
        ax.text(8.4, 7.1 - i * 0.85, f"• {wrap_lines(it, 30)}", fontsize=7.2, color=LTGRAY, family="sans-serif")

    # Self-funding note
    draw_box(ax, 0.6, 1.2, 14.8, 2.0, color=AMBER)
    ax.text(
        8.0,
        2.2,
        "Self-funding logic: creator adoption improves proof and lowers friction for B2B pilots; B2B wins fund deeper templates/integration improvements.",
        ha="center",
        va="center",
        fontsize=8.0,
        color=LTGRAY,
        family="sans-serif",
        fontweight="bold",
    )

    save_slide(fig, "slide-17-unit-economics.png")
    print("✅ Slide 17 wireframe saved")


def slide_18():
    fig, ax = new_slide(18)
    meta = SLIDE_META[18]
    apply_template(ax, 18, meta["sub"], meta["top"], meta["takeaway"])

    # Left success creators
    draw_box(ax, 0.6, 3.3, 7.2, 4.8, color=TEAL, header_height=0.55)
    ax.text(4.2, 7.8, "B2C SUCCESS", ha="center", va="center", fontsize=10, fontweight="bold", color=WHITE)
    b2c = [
        "Repeat activation (short time-to-usable-edit)",
        "Template-driven retention (repeat runs in 7-30d)",
        "Sharing behaviors that indicate real workflow value",
    ]
    for i, it in enumerate(b2c):
        ax.text(1.2, 7.1 - i * 0.85, f"• {wrap_lines(it, 30)}", fontsize=7.2, color=LTGRAY, family="sans-serif")

    # Right success B2B
    draw_box(ax, 8.0, 3.3, 7.2, 4.8, color=PURPLE, header_height=0.55)
    ax.text(11.6, 7.8, "B2B SUCCESS (ENTERPRISE + AGENCIES)", ha="center", va="center", fontsize=10, fontweight="bold", color=WHITE)
    b2b = [
        "Demo-to-technical-onboarding conversion",
        "Governed expansion (shared workspaces + automations + API usage)",
        "Lower time-to-routing for high-intent leads",
    ]
    for i, it in enumerate(b2b):
        ax.text(8.4, 7.1 - i * 0.85, f"• {wrap_lines(it, 30)}", fontsize=7.0, color=LTGRAY, family="sans-serif")

    save_slide(fig, "slide-18-defining-success.png")
    print("✅ Slide 18 wireframe saved")


def slide_19():
    fig, ax = new_slide(19)
    meta = SLIDE_META[19]
    apply_template(ax, 19, meta["sub"], meta["top"], meta["takeaway"])

    cards = [
        ("DATA GUARANTEES", "How do we keep no-training/zero-retention posture intact while automating more?", TEAL),
        ("INTEGRATION STANDARDIZATION", "Which integrations + triggers should we standardize first to reduce setup variance?", BLUE),
        ("AI OPS PRIORITY", "Routing/scoring accuracy vs creative output throughput: what should ship first?", AMBER),
    ]
    card_w = 4.7
    gap = 0.35
    y = 3.2
    h = 5.1
    for i, (title, q, color) in enumerate(cards):
        x = 0.6 + i * (card_w + gap)
        draw_box(ax, x, y, card_w, h, color=color, header_height=0.5)
        ax.text(x + card_w / 2, y + h - 0.2, title, ha="center", va="top", fontsize=9, fontweight="bold", color=WHITE)
        ax.text(x + card_w / 2, y + 2.6, wrap_lines(q, 28), ha="center", va="center", fontsize=7.3, color=LTGRAY, family="sans-serif")

    save_slide(fig, "slide-19-unasked-questions.png")
    print("✅ Slide 19 wireframe saved")


def slide_20():
    fig, ax = new_slide(20)
    meta = SLIDE_META[20]
    apply_template(ax, 20, meta["sub"], meta["top"], meta["takeaway"])

    draw_box(ax, 0.6, 3.0, 14.8, 4.9, color=TEAL, header_height=0.55, dashed=False)
    ax.text(8.0, 7.2, "CLOSING: MOSAIC ENTERS THE WORKFLOW ERA", ha="center", va="center", fontsize=12, fontweight="bold", color=WHITE)

    points = [
        "Agentic editing is operationalized via workflows (canvas + triggers + autopilot pipelines).",
        "Enterprise adoption is governed (RBAC, audit logs) and credible (SOC 2 Type II + no-training/zero-retention posture).",
        "GTM scales by intent routing and automation (AI Ops) instead of manual chaos.",
        "3-month roadmap turns strategy into measurable conversion loops and weekly learning cadence.",
    ]
    for i, it in enumerate(points):
        ax.text(1.8, 6.3 - i * 1.0, f"• {wrap_lines(it, 72)}", fontsize=8.0, color=LTGRAY, family="sans-serif")

    # Bottom CTA placeholder
    draw_box(ax, 0.6, 1.2, 14.8, 1.7, color=AMBER, header_height=0.45)
    ax.text(8.0, 2.05, "Next step: convert top channel learnings into repeatable onboarding + AI Ops governed iteration.",
            ha="center", va="center", fontsize=8.2, color=LTGRAY, family="sans-serif", fontweight="bold")

    save_slide(fig, "slide-20-closing.png")
    print("✅ Slide 20 wireframe saved")


def merge_wireframes():
    from PIL import Image

    files = []
    for i in range(1, TOTAL_SLIDES + 1):
        slug = f"slide-{i:02d}"
        matches = [f for f in os.listdir(OUT_DIR) if f.startswith(slug) and f.endswith(".png")]
        if matches:
            # Each slide should produce exactly one file; pick the first match.
            files.append(os.path.join(OUT_DIR, sorted(matches)[0]))
    files = sorted(files)

    if not files:
        print("No slide wireframes found to merge.")
        return

    images = [Image.open(p) for p in files]
    widths, heights = zip(*(im.size for im in images))
    max_width = max(widths)
    total_height = sum(heights)

    combined = Image.new("RGB", (max_width, total_height), color=(27, 35, 51))
    y_offset = 0
    for im in images:
        combined.paste(im, (0, y_offset))
        y_offset += im.size[1]

    out_path = os.path.join(OUT_DIR, "mosaic_full_deck_wireframe.png")
    combined.save(out_path, quality=95)
    print(f"✅ Combined layout saved to {out_path} ({combined.width}x{combined.height})")


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    # Remove stale renders so numbering stays deterministic.
    for f in os.listdir(OUT_DIR):
        if f.startswith("slide-") and f.endswith(".png"):
            os.remove(os.path.join(OUT_DIR, f))
        if f == "mosaic_full_deck_wireframe.png":
            os.remove(os.path.join(OUT_DIR, f))
    print(f"Generating {TOTAL_SLIDES} Mosaic slide wireframes…")
    slide_1()
    slide_2()
    slide_3()
    slide_4()
    slide_5()
    slide_6()
    slide_7()
    slide_8()
    slide_9()
    slide_10()
    slide_11()
    slide_12()
    slide_13()
    slide_14()
    slide_15()
    slide_16()
    slide_17()
    slide_18()
    slide_19()
    slide_20()
    merge_wireframes()

