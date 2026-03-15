#!/usr/bin/env python3
"""
Generate precise slide wireframes for the TLDR GTM presentation.
Includes Subheadlines, Takeaway footers, and an Agenda slide (16 slides total).
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os
from PIL import Image

# ── Color palette ──────────────────────────────────────────────────────
BG      = '#1B2333'
CARD_BG = '#232F42'
TEAL    = '#00BFA5'
WHITE   = '#FFFFFF'
GRAY    = '#8A94A6'
LTGRAY  = '#C5CDD9'
DASHED  = '#4A5568'
AMBER   = '#FFB74D'
PURPLE  = '#BB86FC'
BLUE    = '#4FC3F7'
GREEN   = '#66BB6A'
CORAL   = '#F7768E'

SLIDE_W = 16
SLIDE_H = 9
TOTAL_SLIDES = 16

# ── Slide Content References (Subhead & Takeaway) ──────────────────────
SLIDE_META = {
    1: {"sub": "Setting the stage for today's discussion", "top": "AGENDA", "takeaway": "We will align on the $100M mandate, our structural moat, and the execution engine."},
    2: {"sub": "The Paradigm Shift", "top": "EXECUTIVE SUMMARY & THE $100M MANDATE", "takeaway": "Pivot from B2C retail efficiency to a self-funding B2B enterprise engine with near-zero marginal scale cost."},
    3: {"sub": "Why our structural moat is unassailable", "top": "COMPETITIVE LANDSCAPE & STRUCTURAL MOAT", "takeaway": "Competitors can copy formats, but no one can replicate 7M+ active specialists feeding a proprietary enterprise intent engine."},
    4: {"sub": "Why Now? | TLDR's advantage widens as traditional channels degrade", "top": "THE EXHAUSTION OF TRADITIONAL SAAS CHANNELS", "takeaway": "TLDR is a direct beneficiary of the death of digital advertising. The harder it is to reach professionals elsewhere, the more CMOs pay us."},
    5: {"sub": "The Dual Engine", "top": "TARGET AUDIENCE & IDENTIFICATION", "takeaway": "We monetize the attention of ad-blocking professional skeptics by selling Intent Data to B2B buying committees."},
    6: {"sub": "Frictionless conversion & B2B proof", "top": "WEBSITE & DIGITAL EXPERIENCE ALIGNMENT", "takeaway": "Our digital surfaces are purpose-built to capture B2C engagement and convert it directly into B2B intent signals."},
    7: {"sub": "$200K Budget for 1H 2026 | Dual-Engine Execution", "top": "MARKETING CHANNELS & GO-TO-MARKET MECHANICS", "takeaway": "We allocate 50% of budget to B2C acquisition (attention layer) to feed the 30% spent on B2B ABM capture (revenue layer)."},
    8: {"sub": "Specialists value Status, Utility, and Team Network Effects", "top": "REFERRAL MECHANISMS & PROFESSIONAL VIRALITY", "takeaway": "Traditional SWAG referrals fail; granting utility (Team Unlock, Ad-Free) creates true viral coefficient growth."},
    9: {"sub": "Ensuring sponsor ROI to prevent churn", "top": "B2B SUCCESS & 'WHITE-GLOVE' COPYWRITING", "takeaway": "Our B2B CS pod acts as copywriting consultants to rewrite generic SaaS ads into 'Specialist's Proof' that actually converts professionals."},
    10: {"sub": "Automating the Enterprise Pipeline", "top": "TAM MAPPING & CRM AUTOMATION PLAYBOOK", "takeaway": "We route intent instantly: VP engagement triggers a Slack alert and <5 min Senior AE response time."},
    11: {"sub": "Enterprise sponsor buys 100% of ad inventory in a vertical for 30 days", "top": "PATH TO SCALE & CATEGORY DOMINANCE", "takeaway": "Selling exclusive monthly access creates neurological brand association and allows ACVs to scale to $200K+/month."},
    12: {"sub": "Orchestrated Outbound | The Signal Dossier Handoff", "top": "SALES & MARKETING SYMBIOSIS", "takeaway": "SDRs receive a 'Signal Dossier' detailing exactly what professional teams are reading, enabling surgical outbound pitches."},
    13: {"sub": "Protecting the core engine", "top": "RISK MITIGATION & CHALLENGES", "takeaway": "We bypass tracking degradation (Apple MPP) by forcing all sponsor ROI criteria downstream to verified clicks and SQLs."},
    14: {"sub": "The math behind the Trust-Revenue Loop", "top": "KPIs, UNIT ECONOMICS, & CAC PAYBACK", "takeaway": "Every $2.50 B2C subscriber enables a >$50k B2B sponsorship. Our >20:1 LTV:CAC ratio self-funds the entire empire."},
    15: {"sub": "Defining success for the next 6-36 months", "top": "DEFINING SUCCESS — 1H & 2026 VISION", "takeaway": "By 2026, we will push past $100M ARR while maintaining our legendary sub-10 FTE operating leverage."},
    16: {"sub": "Strategic Questions Leadership Must Align On", "top": "THE UNASKED QUESTIONS", "takeaway": "Scaling B2B data monetization must be carefully balanced against our core promise of respecting subscriber privacy."}
}


def new_slide(fig_num=1):
    fig, ax = plt.subplots(1, 1, figsize=(SLIDE_W, SLIDE_H), num=fig_num)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, SLIDE_W)
    ax.set_ylim(0, SLIDE_H)
    ax.axis('off')
    return fig, ax

def draw_box(ax, x, y, w, h, label='', sublabel='', color=TEAL, dashed=False, fill=True, fontsize=9, sublabel_fontsize=7.5, header_height=None, text_color=WHITE):
    ls = '--' if dashed else '-'
    ec = DASHED if dashed else color
    fc = CARD_BG if fill else 'none'
    rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                          facecolor=fc, edgecolor=ec, linewidth=1.2, linestyle=ls)
    ax.add_patch(rect)
    if header_height and label:
        header = FancyBboxPatch((x, y + h - header_height), w, header_height,
                                boxstyle="round,pad=0.05", facecolor=color, edgecolor=color, linewidth=0, alpha=0.25)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - header_height/2, label, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=text_color, family='sans-serif')
    elif label:
        ax.text(x + w/2, y + h - 0.25, label, ha='center', va='top',
                fontsize=fontsize, fontweight='bold', color=text_color, family='sans-serif')
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.1, sublabel, ha='center', va='center',
                fontsize=sublabel_fontsize, color=GRAY, family='sans-serif', style='italic', wrap=True)

def apply_template(ax, num):
    meta = SLIDE_META[num]
    
    # Title & Subheadline
    ax.text(0.6, 8.2, meta["top"], fontsize=22, fontweight='bold', color=WHITE, family='sans-serif')
    ax.text(0.6, 7.65, meta["sub"], fontsize=12, color=TEAL, family='sans-serif', style='italic')
    ax.plot([0.6, 15.4], [7.35, 7.35], color=DASHED, linewidth=0.5)

    if num == 2: # Logo on Exec Summary
        draw_box(ax, 13.8, 7.8, 1.8, 0.9, label='[TLDR LOGO]', color=DASHED, dashed=True, fill=False, fontsize=8)

    # Footer elements
    rect = plt.Rectangle((0, 0), SLIDE_W, 0.08, facecolor=TEAL, edgecolor='none')
    ax.add_patch(rect)
    
    # Slide Number Target
    ax.text(SLIDE_W - 0.4, 0.45, str(num), ha='center', va='center',
            fontsize=10, fontweight='bold', color=BG, family='sans-serif',
            bbox=dict(boxstyle='circle,pad=0.3', facecolor=TEAL, edgecolor='none'))
    
    ax.text(0.6, 0.45, f'SLIDE {num} OF {TOTAL_SLIDES}', fontsize=8, color=GRAY, family='sans-serif', fontweight='bold')
    
    # Key Takeaway (Centered at Bottom)
    ax.text(8.0, 0.45, f'KEY TAKEAWAY: {meta["takeaway"]}', fontsize=10, color=WHITE, family='sans-serif', fontweight='bold', ha='center', va='center')


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 1: AGENDA (NEW)
# ═══════════════════════════════════════════════════════════════════════
def slide_1():
    fig, ax = new_slide(1)
    apply_template(ax, 1)
    
    agendas = [
        ("The Current State & The $100M Mandate", "Metrics, structural moat, and pivoting to B2B enterprise monetization.", 5.5),
        ("The Target Audiences & Delivery Engine", "The 'Technical Skeptic' B2C vs. The B2B Buying Committee.", 4.2),
        ("Marketing Mix & B2B Execution Playbook", "GTM mechanics, 'White-Glove' copywriting, and ABM pipeline routing.", 2.9),
        ("Sales Symbiosis & Economics", "Category dominance, Outbound dossiers, and our >20:1 LTV/CAC ratio.", 1.6)
    ]
    for i, (title, desc, y) in enumerate(agendas):
        ax.text(1.2, y, f"0{i+1}.", fontsize=22, fontweight='bold', color=TEAL, family='sans-serif')
        ax.text(2.6, y, title, fontsize=15, fontweight='bold', color=WHITE, family='sans-serif')
        ax.text(2.6, y - 0.45, desc, fontsize=10, color=LTGRAY, family='sans-serif')
        ax.plot([2.6, 14.8], [y - 0.8, y - 0.8], color=DASHED, linewidth=0.5, linestyle=':')

    fig.savefig('tldr-wireframes/slide-01-agenda.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 1 wireframe saved')


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 2: Executive Summary (Original Slide 1)
# ═══════════════════════════════════════════════════════════════════════
def slide_2():
    fig, ax = new_slide(2)
    apply_template(ax, 2)

    # Left: Key metrics
    draw_box(ax, 0.6, 3.8, 5.0, 3.0, color=TEAL)
    ax.text(1.0, 6.4, 'TODAY\'S METRICS', fontsize=11, fontweight='bold', color=TEAL, family='sans-serif')
    metrics = ['7M+ total subscribers across 12+ verticals', '~$10M+ annual revenue', '~4 full-time employees', '38-40% open rates (vs. 21% SaaS avg)', 'Bootstrapped & profitable']
    for i, m in enumerate(metrics):
        ax.plot([1.0, 1.12], [5.9 - i*0.42, 5.9 - i*0.42], color=TEAL, linewidth=2, solid_capstyle='round')
        ax.text(1.22, 5.9 - i*0.42, m, va='center', fontsize=8, color=LTGRAY, family='sans-serif')

    # Center: Strategy
    draw_box(ax, 5.9, 3.8, 5.0, 3.0, color=BLUE)
    ax.text(6.3, 6.4, 'THE STRATEGY', fontsize=11, fontweight='bold', color=BLUE, family='sans-serif')
    strat = ['Execute the Trust-Revenue Loop:', '  B2C attention → B2B sponsorships', '  → reinvest margins → B2C scale', '', 'Marginal cost near-zero;', 'sponsor revenue scales supralinearly']
    for i, s in enumerate(strat):
        ax.text(6.3, 5.9 - i*0.38, s, fontsize=7.5, color=LTGRAY, family='sans-serif')

    # Right: Visual placeholder
    draw_box(ax, 11.2, 3.8, 4.2, 3.0, dashed=True, fill=False, color=DASHED)
    ax.text(13.3, 5.6, '[VISUAL]', fontsize=14, fontweight='bold', color=DASHED, ha='center', family='sans-serif')
    ax.text(13.3, 5.0, 'Trust-Revenue\nLoop Flywheel\nDiagram', fontsize=9, color=GRAY, ha='center', family='sans-serif', linespacing=1.5)

    # Bottom: Vertical subscriber cards
    ax.text(0.6, 3.3, 'THE VERTICAL EMPIRE', fontsize=10, fontweight='bold', color=TEAL, family='sans-serif')
    verticals = [('Tech', '1.6M'), ('AI', '920K'), ('InfoSec', '410K'), ('DevOps', '340K'), ('Crypto', '310K'), ('WebDev', '~200K')]
    for i, (name, count) in enumerate(verticals):
        x = 0.6 + i * 2.55
        pill = FancyBboxPatch((x, 1.2), 2.3, 1.8, boxstyle="round,pad=0.08", facecolor=CARD_BG, edgecolor=TEAL, linewidth=0.8)
        ax.add_patch(pill)
        ax.text(x + 1.15, 2.5, name, ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
        ax.text(x + 1.15, 1.9, count, ha='center', va='center', fontsize=12, fontweight='bold', color=TEAL, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-02-executive-summary.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 2 wireframe saved')

def slide_5():
    fig, ax = new_slide(5)
    apply_template(ax, 5)

    # Left: B2C
    draw_box(ax, 0.6, 3.3, 7.2, 3.8, color=TEAL, header_height=0.6)
    ax.text(4.2, 6.8, 'B2C: THE HIGH-SIGNAL SPECIALIST', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, family='sans-serif')
    
    ax.text(0.9, 6.15, 'AUDIENCE', fontweight='bold', fontsize=7.5, color=TEAL, family='sans-serif')
    ax.text(3.0, 6.15, 'VALUE', fontweight='bold', fontsize=7.5, color=TEAL, family='sans-serif')
    ax.text(5.3, 6.15, 'WANT', fontweight='bold', fontsize=7.5, color=TEAL, family='sans-serif')
    ax.plot([0.8, 7.6], [5.9, 5.9], color=TEAL, linewidth=1, alpha=0.5)
    
    table_data = [
        ('Engineers', 'Technical depth,\nSignal > Noise', '5-min zero-fluff\ntool curation'),
        ('Marketers', 'Actionable tactics,\nROI benchmarks', 'Case studies,\ngrowth frameworks'),
        ('IT Admins', 'Operational security,\nSystem reliability', 'CVE alerts,\ninfra updates')
    ]
    for i, (aud, val, wnt) in enumerate(table_data):
        y = 5.4 - i * 0.75
        ax.text(0.9, y, aud, fontsize=8.5, fontweight='bold', color=WHITE, family='sans-serif', va='center')
        ax.text(3.0, y, val, fontsize=7.5, color=LTGRAY, family='sans-serif', va='center')
        ax.text(5.3, y, wnt, fontsize=7.5, color=LTGRAY, family='sans-serif', va='center')
        if i < 2:
            ax.plot([0.8, 7.6], [y - 0.38, y - 0.38], color=GRAY, linewidth=0.5)

    # Right: B2B
    draw_box(ax, 8.2, 3.3, 7.2, 3.8, color=PURPLE, header_height=0.6)
    ax.text(11.8, 6.8, 'B2B: THE BUYING COMMITTEE', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, family='sans-serif')
    b2b = [('Champion', 'Dir. of Demand Gen — needs MQLs this quarter'), ('Economic Buyer', 'VP Marketing / CMO — CAC payback & brand'), ('Tech Evaluator', 'Perf. Marketing Mgr — scrutinizes audience data')]
    for i, (role, desc) in enumerate(b2b):
        y = 5.9 - i*1.0
        ax.text(8.6, y, role, fontsize=8.5, fontweight='bold', color=PURPLE, family='sans-serif')
        ax.text(8.6, y - 0.35, desc, fontsize=7.5, color=LTGRAY, family='sans-serif')

    # Bottom: Data flow
    draw_box(ax, 0.6, 1.1, 14.8, 1.9, color=BLUE, header_height=0.5)
    ax.text(8.0, 2.75, 'DATA EXECUTION FLOW', ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
    flow = ['Internal Behavioral Profiling (click-surge data across 7M+ subs)', '→  Firmographic Filtering (Series B+ SaaS with active marketing budgets)',
            '→  Job Title Mapping (VP Marketing, Head of Growth via LinkedIn enrichment)']
    for i, f in enumerate(flow):
        ax.text(1.0, 2.1 - i*0.35, f, fontsize=7.5, color=LTGRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-05-target-audience.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 5 wireframe saved')

def slide_6():
    fig, ax = new_slide(6)
    apply_template(ax, 6)

    # Top-left: B2C Landing
    draw_box(ax, 0.6, 4.8, 5.0, 2.3, color=TEAL, header_height=0.5)
    ax.text(3.1, 6.85, 'B2C LANDING PAGE', ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
    items = ['Autofocus email field', 'OAuth sign-up (~50% mobile conversions)', 'No newsletter preview = higher conversion', 'Vertical self-segmentation on sign-up']
    for i, item in enumerate(items):
        ax.text(1.0, 6.1 - i*0.35, '•  ' + item, fontsize=7, color=LTGRAY, family='sans-serif')

    # Top-right: B2B /advertise
    draw_box(ax, 5.9, 4.8, 5.0, 2.3, color=PURPLE, header_height=0.5)
    ax.text(8.4, 6.85, 'B2B /ADVERTISE OVERHAUL', ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
    items = ['Function like B2B SaaS product page', 'Live "Intent Heatmap" visualization', 'Specialist\'s Proof case studies', 'Address CMO fears: wasted spend, attribution']
    for i, item in enumerate(items):
        ax.text(6.3, 6.1 - i*0.35, '•  ' + item, fontsize=7, color=LTGRAY, family='sans-serif')

    # Top-far-right: SEO
    draw_box(ax, 11.2, 4.8, 4.2, 2.3, color=BLUE, header_height=0.5)
    ax.text(13.3, 6.85, 'PROGRAMMATIC SEO', ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
    items = ['/topics/kubernetes', '/topics/large-language-models', 'Auto-populated daily from archives', 'Dual: B2C acquisition + B2B capture']
    for i, item in enumerate(items):
        ax.text(11.6, 6.1 - i*0.35, '•  ' + item, fontsize=7, color=LTGRAY, family='sans-serif')

    # Bottom: 5 ELG Tools
    ax.text(0.6, 4.3, '5 PRODUCT-LED GROWTH (PLG) TOOLS', fontsize=11, fontweight='bold', color=TEAL, family='sans-serif')
    tools = [('Cloud Cost\nBenchmarker', 'Share to\nunlock results'), ('AI Ad-Copy\nGrader', 'Test LinkedIn\ncreatives'),
             ('B2B Sponsor\nROI Calculator', 'Pre-sells CFO\non pipeline'), ('CVE Threat\nScanner', 'IT Admins check\nrepo pulls'),
             ('Startup Equity\nVisualizer', 'Founders view\ncomp data')]
    for i, (name, sub) in enumerate(tools):
        x = 0.6 + i * 3.1
        draw_box(ax, x, 1.1, 2.8, 3.0, color=TEAL)
        ax.text(x + 1.4, 3.5, name, ha='center', va='center', fontsize=8, fontweight='bold', color=WHITE, family='sans-serif')
        ax.text(x + 1.4, 2.2, sub, ha='center', va='center', fontsize=7, color=GRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-06-digital-experience.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 6 wireframe saved')

def slide_7():
    fig, ax = new_slide(7)
    apply_template(ax, 7)

    # Left: B2C
    draw_box(ax, 0.6, 2.7, 7.2, 4.3, color=TEAL, header_height=0.55)
    ax.text(4.2, 6.72, 'B2C CHANNEL MIX', ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
    channels = [('1. PLG & Free Tools', 'Viral utility tools requiring sharing to unlock'),
                ('2. Native Paid Social (Reddit/X)', 'Brutalist, text-heavy ads perfectly mimicking native UI'),
                ('3. Creator Partnerships', 'Sponsor trusted vertical creators for mid‑roll reads'),
                ('4. Referral Loops', 'Friction-removing mechanics for intra‑company sharing')]
    for i, (ch, strat) in enumerate(channels):
        y = 5.9 - i*0.8
        ax.text(1.0, y, ch, fontsize=8, fontweight='bold', color=WHITE, family='sans-serif')
        ax.text(1.0, y - 0.35, 'Strategy: ' + strat, fontsize=7, color=LTGRAY, family='sans-serif')

    # Right: B2B
    draw_box(ax, 8.2, 2.7, 7.2, 4.3, color=PURPLE, header_height=0.55)
    ax.text(11.8, 6.72, 'B2B CHANNEL MIX', ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
    channels = [('1. Automated ABM Outbound', 'TLDR subscriber click-data as the direct pitch hook'),
                ('2. Dark Funnel Acceleration', 'De-anonymize /advertise traffic & trigger Sales alerts'),
                ('3. "Champion Move" Tracking', 'Monitor job changes & auto-pitch past sponsors'),
                ('4. B2B Paid Social (LinkedIn)', 'Contrarian creative steering CMOs to TLDR ads')]
    for i, (ch, strat) in enumerate(channels):
        y = 5.9 - i*0.8
        ax.text(8.6, y, ch, fontsize=8, fontweight='bold', color=WHITE, family='sans-serif')
        ax.text(8.6, y - 0.35, 'Strategy: ' + strat, fontsize=7, color=LTGRAY, family='sans-serif')

    # Bottom: Budget bar
    draw_box(ax, 0.6, 1.1, 14.8, 1.3, color=AMBER, header_height=0.45)
    ax.text(8.0, 2.17, 'BUDGET ALLOCATION ($200K)', ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
    ax.text(8.0, 1.5, '50% B2C Acquisition ($100K)   |   30% B2B ABM & Intent Infra ($60K)   |   20% PLG Tool Dev ($40K)',
            ha='center', va='center', fontsize=8, color=LTGRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-07-channel-mix.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 7 wireframe saved')

def slide_8():
    fig, ax = new_slide(8)
    apply_template(ax, 8)

    mechs = [('TEAM UNLOCK', 'Invite 5 coworkers →\nwhole team gets TLDR Pro', 'Network\nEffect', TEAL),
             ('ZERO NOISE', 'Refer 5 peers →\nunlock ad-free digest', 'Utility\nValue', BLUE),
             ('CURATOR BADGE', 'Submit links; get public\ncredit + leaderboard', 'Status\nVirality', PURPLE),
             ('EARLY ACCESS', 'Refer 3 peers → beta\naccess new verticals', 'Scarcity +\nFOMO', AMBER),
             ('DARK-SOCIAL', '1-click Share to\nSlack / Discord buttons', 'Friction\nRemoval', GREEN)]
    for i, (name, desc, lever, color) in enumerate(mechs):
        x = 0.6 + i * 3.1
        draw_box(ax, x, 2.4, 2.8, 4.6, color=color, header_height=0.6)
        ax.text(x + 1.4, 6.7, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color=WHITE, family='sans-serif')
        ax.text(x + 1.4, 5.4, desc, ha='center', va='center', fontsize=7.5, color=LTGRAY, family='sans-serif')
        pill = FancyBboxPatch((x + 0.4, 2.8), 2.0, 0.9, boxstyle="round,pad=0.08", facecolor=color, edgecolor='none', alpha=0.2)
        ax.add_patch(pill)
        ax.text(x + 1.4, 3.25, lever, ha='center', va='center', fontsize=7, fontweight='bold', color=color, family='sans-serif')

    # Bottom: fraud prevention
    draw_box(ax, 0.6, 1.1, 14.8, 1.0, color=CORAL)
    ax.text(8.0, 1.6, 'FRAUD PREVENTION:  SparkLoop engagement screening — credit referrals only if referred subscriber opens 3+ of first 10 emails',
            ha='center', va='center', fontsize=8, color=LTGRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-08-referral-mechanisms.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 8 wireframe saved')

def slide_11():
    fig, ax = new_slide(11)
    apply_template(ax, 11)

    # Pricing table
    table_top = 6.6
    headers = ['VERTICAL', 'SUBSCRIBERS', 'MONTHLY PRICE', 'VALUE PROP']
    col_x = [0.8, 4.5, 7.5, 10.5]
    header_bar = plt.Rectangle((0.4, table_top - 0.05), 15.2, 0.5, facecolor=TEAL, edgecolor='none', alpha=0.2)
    ax.add_patch(header_bar)
    for i, h in enumerate(headers):
        ax.text(col_x[i], table_top + 0.2, h, fontsize=8, fontweight='bold', color=TEAL, va='center', family='sans-serif')

    rows = [('TLDR Tech (Flagship)', '1.6M', '$200,000+', 'Broadest reach; every DevTool buyer'),
            ('TLDR AI', '920K', '$120,000+', 'Hottest vertical; ML/AI infrastructure'),
            ('TLDR InfoSec', '410K', '$60,000+', 'Cybersecurity; high-ACV sponsors'),
            ('TLDR DevOps', '340K', '$50,000+', 'CI/CD, observability, cloud native'),
            ('Smaller Verticals', '100K-300K', '$25K-$40K', 'WebDev, Founders, Design, Marketing')]
    for ri, (vert, subs, price, vp) in enumerate(rows):
        y = table_top - 0.7 - ri * 0.8
        if ri % 2 == 0:
            row_bg = plt.Rectangle((0.4, y - 0.1), 15.2, 0.7, facecolor=CARD_BG, edgecolor='none', alpha=0.4)
            ax.add_patch(row_bg)
        ax.text(col_x[0], y + 0.2, vert, fontsize=8, color=WHITE, va='center', family='sans-serif', fontweight='bold')
        ax.text(col_x[1], y + 0.2, subs, fontsize=8, color=LTGRAY, va='center', family='sans-serif')
        ax.text(col_x[2], y + 0.2, price, fontsize=9, color=AMBER, va='center', family='sans-serif', fontweight='bold')
        ax.text(col_x[3], y + 0.2, vp, fontsize=7, color=GRAY, va='center', family='sans-serif')

    # Bottom: Data Exclusivity
    draw_box(ax, 0.6, 1.1, 14.8, 1.6, color=AMBER)
    ax.text(1.0, 2.3, 'DATA EXCLUSIVITY BONUS', fontsize=10, fontweight='bold', color=AMBER, family='sans-serif')
    ax.text(1.0, 1.7, 'Category Dominance sponsors receive exclusive aggregated click behavior data for their vertical during the campaign.', fontsize=8, color=LTGRAY, family='sans-serif')
    ax.text(1.0, 1.3, 'They learn which sub-topics their audience cares about most, informing product & marketing strategy.', fontsize=7.5, color=GRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-11-category-dominance.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 11 wireframe saved')

def slide_13():
    fig, ax = new_slide(13)
    apply_template(ax, 13)

    risks = [('LIST FATIGUE', 'Verticalizing too fast → readers burn out', 'Frequency capping, cross-list dedup,\n"Daily Digest Bundle." Monitor: <30% opens → re-engage.', TEAL),
             ('TRACKING DEGRADATION', 'Apple MPP obfuscates open rates', 'Pivot ALL sponsor ROI to downstream\npipeline velocity: verified clicks, sign-ups, SQLs.', BLUE),
             ('KEY-PERSON RISK', 'Editorial voice tied to Dan Ni', 'Recruit vertical-specific expert curators\n(ex-Google, ex-Stripe) and brand them publicly.', PURPLE),
             ('PLATFORM RISK', 'Gmail/Outlook spam algorithm updates', 'Strict list hygiene (purge non-openers 90d),\nfull DMARC/DKIM/SPF, diversify to web + RSS.', AMBER)]
    bw, bh = 7.2, 2.8
    for i, (title, risk, mitigation, color) in enumerate(risks):
        col = i % 2
        row = i // 2
        x = 0.6 + col * (bw + 0.4)
        y = 4.2 - row * (bh + 0.3)
        draw_box(ax, x, y, bw, bh, color=color, header_height=0.55)
        ax.text(x + bw/2, y + bh - 0.28, title, ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
        ax.text(x + 0.3, y + bh - 0.95, '⚠ ' + risk, fontsize=7.5, color=CORAL, family='sans-serif')
        ax.text(x + 0.3, y + bh - 1.55, '✓ MITIGATION:', fontsize=7, fontweight='bold', color=GREEN, family='sans-serif')
        ax.text(x + 0.3, y + bh - 2.0, mitigation, fontsize=7, color=LTGRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-13-risk-mitigation.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 13 wireframe saved')

def slide_12():
    fig, ax = new_slide(12)
    apply_template(ax, 12)

    # Left: Signal Dossier
    draw_box(ax, 0.6, 2.3, 7.2, 4.7, color=TEAL, header_height=0.55)
    ax.text(4.2, 6.72, 'THE SIGNAL DOSSIER (MQL → SQL)', ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
    items = ['Company Profile (funding stage, headcount, news)', 'Audience Engagement Report:', '  → Which TLDR verticals their employees read', '  → Most-clicked articles in past 30 days',
             'Intent Score (media kit dwell time)', 'Recommended Pitch Angle:', '  → "Their Marketing team clicked AI AdTech.', '       Lead with TLDR Marketing Takeover."']
    for i, item in enumerate(items):
        c = LTGRAY if not item.startswith('  →') else GRAY
        ax.text(1.0, 6.0 - i*0.44, item, fontsize=7, color=c, family='sans-serif')

    # Right: Feedback Loop + Enablement
    draw_box(ax, 8.2, 4.4, 7.2, 2.6, color=BLUE, header_height=0.5)
    ax.text(11.8, 6.75, 'CONTINUOUS FEEDBACK LOOP', ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
    items = ['Bi-weekly "Pipeline Councils"', 'Refine targeting, messaging, channel mix overnight', 'If Series A lacks budget → adjust firmographic filters']
    for i, item in enumerate(items):
        ax.text(8.6, 6.0 - i*0.4, '•  ' + item, fontsize=7, color=LTGRAY, family='sans-serif')

    draw_box(ax, 8.2, 1.1, 7.2, 3.0, color=AMBER, header_height=0.5)
    ax.text(11.8, 3.85, 'SALES ENABLEMENT', ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
    items = ['Competitor Battlecards (TLDR vs LinkedIn Ads)', '"$50+ CPMs for banners vs. 500-1,000 verified clicks"', 'Positioning Guides (pipeline velocity vs. brand authority)']
    for i, item in enumerate(items):
        ax.text(8.6, 3.1 - i*0.5, '•  ' + item, fontsize=7, color=LTGRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-12-sales-symbiosis.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 12 wireframe saved')


def slide_15():
    fig, ax = new_slide(15)
    apply_template(ax, 15)

    draw_box(ax, 0.6, 2.6, 7.2, 4.4, color=TEAL, header_height=0.55)
    ax.text(4.2, 6.72, '1H LEADING INDICATORS', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, family='sans-serif')
    items = [('Subscriber Scale', 'Surpass 10M total (SAC < $2.50)'), ('B2B Logos', '5-10 "Category Dominance" deals (ACV > $50K)'),
             ('Signal Efficiency', '15% Signal-to-Demo on B2B outbound'), ('Referral Traction', '20%+ net-new sign-ups from referrals')]
    for i, (metric, target) in enumerate(items):
        y = 5.9 - i * 0.95
        ax.text(1.0, y, metric, fontsize=9, fontweight='bold', color=TEAL, family='sans-serif')
        ax.text(1.0, y - 0.35, target, fontsize=7.5, color=LTGRAY, family='sans-serif')

    draw_box(ax, 8.2, 2.6, 7.2, 4.4, color=AMBER, header_height=0.55)
    ax.text(11.8, 6.72, '2026 LAGGING INDICATORS', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, family='sans-serif')
    items = [('ARR Target', 'Push past $100M — Enterprise Sponsorships + DaaS'), ('Market Leadership', 'Default highest-ROI technical execution layer for DevTools GTM'),
             ('Operating Leverage', 'Maintain sub-10 FTE while scaling to $100M+')]
    for i, (metric, target) in enumerate(items):
        y = 5.9 - i * 1.15
        ax.text(8.6, y, metric, fontsize=9, fontweight='bold', color=AMBER, family='sans-serif')
        ax.text(8.6, y - 0.35, target, fontsize=7.5, color=LTGRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-15-success-metrics.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 15 wireframe saved')


def slide_3():
    fig, ax = new_slide(3)
    apply_template(ax, 3)

    table_top = 6.6
    headers = ['COMPETITOR', 'SCALE', 'FOCUS', 'TLDR ADVANTAGE']
    col_x = [0.8, 4.0, 6.5, 10.0]
    header_bar = plt.Rectangle((0.4, table_top - 0.05), 15.2, 0.5, facecolor=TEAL, edgecolor='none', alpha=0.2)
    ax.add_patch(header_bar)
    for i, h in enumerate(headers):
        ax.text(col_x[i], table_top + 0.2, h, fontsize=8, fontweight='bold', color=TEAL, va='center', family='sans-serif')
    rows = [('Morning Brew', '4M+', 'General business', 'Doesn\'t reach specialists'),
            ('The Hustle (HubSpot)', '2.5M+', 'Business/startup', 'Acquired; editorial questions'),
            ('The Information', '~400K', 'Deep tech analysis', 'Paywalled; TLDR is free & 10x scale'),
            ('The Rundown AI', '600K+', 'AI-only newsletter', 'Single vertical; TLDR AI = 920K'),
            ('Hacker Newsletter', '~60K', 'Curated HN links', 'TLDR is 100x the audience')]
    for ri, (comp, scale, focus, adv) in enumerate(rows):
        y = table_top - 0.7 - ri * 0.7
        if ri % 2 == 0:
            row_bg = plt.Rectangle((0.4, y - 0.05), 15.2, 0.6, facecolor=CARD_BG, edgecolor='none', alpha=0.4)
            ax.add_patch(row_bg)
        ax.text(col_x[0], y + 0.2, comp, fontsize=8, color=WHITE, va='center', family='sans-serif', fontweight='bold')
        ax.text(col_x[1], y + 0.2, scale, fontsize=8, color=LTGRAY, va='center', family='sans-serif')
        ax.text(col_x[2], y + 0.2, focus, fontsize=7.5, color=LTGRAY, va='center', family='sans-serif')
        ax.text(col_x[3], y + 0.2, adv, fontsize=7.5, color=TEAL, va='center', family='sans-serif')

    draw_box(ax, 0.6, 1.1, 14.8, 1.8, color=TEAL)
    ax.text(1.0, 2.5, 'OUR STRUCTURAL MOAT', fontsize=10, fontweight='bold', color=TEAL, family='sans-serif')
    ax.text(1.0, 1.9, 'Even if a competitor copies our format perfectly, they cannot replicate: 7M+ active specialist audience + established', fontsize=8, color=LTGRAY, family='sans-serif')
    ax.text(1.0, 1.5, 'enterprise sponsor pipeline + proprietary data exhaust that compounds with scale.', fontsize=8, color=LTGRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-03-competitive-landscape.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 3 wireframe saved')

def slide_14():
    fig, ax = new_slide(14)
    apply_template(ax, 14)

    # B2C
    draw_box(ax, 0.6, 3.4, 7.2, 3.7, color=TEAL, header_height=0.55)
    ax.text(4.2, 6.82, 'B2C UNIT ECONOMICS', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, family='sans-serif')
    items = [('PLG / Referrals', '~$0.50-$1.00'), ('Creator Sponsorships', '~$1.50-$2.50'), ('Reddit / X Native Ads', '~$2.00-$3.00'), ('Meta Lookalike Ads', '~$3.00-$5.00')]
    for i, (ch, sac) in enumerate(items):
        y = 6.0 - i*0.6
        ax.text(1.0, y, ch, fontsize=8, color=LTGRAY, family='sans-serif')
        ax.text(6.5, y, sac, fontsize=9, fontweight='bold', color=TEAL, ha='right', family='sans-serif')
    ax.text(1.0, 3.8, 'PAYBACK PERIOD: < 30 DAYS', fontsize=9, fontweight='bold', color=GREEN, family='sans-serif')

    # B2B
    draw_box(ax, 8.2, 3.4, 7.2, 3.7, color=PURPLE, header_height=0.55)
    ax.text(11.8, 6.82, 'B2B UNIT ECONOMICS', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, family='sans-serif')
    items = [('B2B CAC', '$5K-$10K'), ('Enterprise Sponsor LTV', '$200K+ (3-year)'), ('LTV:CAC RATIO', '>20:1')]
    for i, (label, val) in enumerate(items):
        y = 6.0 - i*0.9
        ax.text(8.6, y, label, fontsize=8, color=LTGRAY, family='sans-serif')
        ax.text(14.0, y, val, fontsize=10, fontweight='bold', color=AMBER, ha='right', family='sans-serif')

    # Bottom callout
    draw_box(ax, 0.6, 1.1, 14.8, 2.0, color=AMBER)
    ax.text(8.0, 2.5, 'THE SELF-FUNDING ENGINE', ha='center', fontsize=10, fontweight='bold', color=AMBER, family='sans-serif')
    ax.text(8.0, 1.7, 'Every B2C subscriber enables a higher-priced B2B sponsorship → which funds the next cohort of B2C subscribers.\nThis is the mathematical core of the Trust-Revenue Loop.',
            ha='center', fontsize=8, color=LTGRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-14-unit-economics.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 14 wireframe saved')

def slide_4():
    fig, ax = new_slide(4)
    apply_template(ax, 4)

    channels = [('COLD EMAIL', 'Google/Yahoo 2024 DMARC\nenforcement. Professionals\nscript-filter outbound.', '☠', CORAL),
                ('PAID SOCIAL', 'ATT destroyed Meta signal.\nSpecialist audiences run\nad-blockers at 3-5x rates.', '☠', CORAL),
                ('CONTENT MKT', 'AI slop flooded SERPs.\n12-18 months to rank.\nDiminishing returns.', '⚠', AMBER),
                ('LINKEDIN ADS', '$50+ CPMs. Specialists\nsee it as job-search,\nnot content discovery.', '⚠', AMBER)]
    for i, (name, desc, icon, color) in enumerate(channels):
        x = 0.6 + i * 3.9
        draw_box(ax, x, 3.2, 3.6, 3.7, color=color, header_height=0.55)
        ax.text(x + 1.8, 6.62, icon + ' ' + name, ha='center', va='center', fontsize=9, fontweight='bold', color=WHITE, family='sans-serif')
        ax.text(x + 1.8, 5.0, desc, ha='center', va='center', fontsize=7.5, color=LTGRAY, family='sans-serif')

    draw_box(ax, 0.6, 1.1, 14.8, 1.8, color=TEAL)
    ax.text(1.0, 2.5, 'THE STRUCTURAL INVERSION', fontsize=10, fontweight='bold', color=TEAL, family='sans-serif')
    ax.text(1.0, 1.9, 'TLDR bypasses every collapsing channel: We don\'t send cold email — professionals opt in. We don\'t rely on Meta signal — we track clicks directly.', fontsize=8, color=LTGRAY, family='sans-serif')
    ax.text(1.0, 1.5, 'The worse LinkedIn Ads perform, the more CMOs allocate to TLDR. We are a direct beneficiary of the death of digital advertising.', fontsize=8, color=LTGRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-04-channel-exhaustion.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 4 wireframe saved')

def slide_10():
    fig, ax = new_slide(10)
    apply_template(ax, 10)

    tiers = [('TIER 1\nHYPER-INTENT', 'Multiple employees visit /advertise\n+ large funding round\n+ heavy vertical subscription', '→ Immediate Senior AE outreach\n   with Signal Dossier', TEAL),
             ('TIER 2\nCORE TAM', 'ICP match (SaaS + mktg budget)\nNo direct buying signals yet', '→ Automated "State of Tech"\n   email nurture sequence', BLUE),
             ('TIER 3\nLONG-TERM', 'Adjacent companies\n(non-tech hiring specialists)', '→ Light-touch automated\n   nurture only', GRAY)]
    for i, (name, criteria, action, color) in enumerate(tiers):
        y = 5.2 - i * 2.0
        draw_box(ax, 0.6, y, 4.5, 1.7, color=color, header_height=0.5)
        ax.text(2.85, y + 1.45, name, ha='center', va='center', fontsize=8, fontweight='bold', color=WHITE, family='sans-serif')
        ax.text(1.0, y + 0.5, criteria, fontsize=6.5, color=LTGRAY, family='sans-serif')
        ax.annotate('', xy=(5.4, y + 0.8), xytext=(5.1, y + 0.8), arrowprops={'arrowstyle': '->', 'color': color, 'lw': 2})
        ax.text(5.6, y + 0.8, action, fontsize=7, color=color, va='center', family='sans-serif')

    # CRM SLA
    draw_box(ax, 10.5, 1.2, 5.0, 5.7, color=AMBER, header_height=0.55)
    ax.text(13.0, 6.62, 'CRM SLA', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, family='sans-serif')
    steps = ['VP Marketing Reply', '↓', 'Auto-create HubSpot Deal', '↓', 'Assign Senior AE', '↓', 'Slack Alert: #sponsorship-sales', '↓', '< 5 MINUTE RESPONSE TIME']
    for i, s in enumerate(steps):
        c = AMBER if s.startswith('<') else (TEAL if s == '↓' else LTGRAY)
        fw = 'bold' if s.startswith('<') else 'normal'
        ax.text(13.0, 5.8 - i*0.5, s, ha='center', fontsize=8, color=c, fontweight=fw, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-10-tam-mapping.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 10 wireframe saved')


def slide_9():
    fig, ax = new_slide(9)
    apply_template(ax, 9)

    draw_box(ax, 0.6, 5.2, 7.2, 1.8, color=CORAL, header_height=0.5)
    ax.text(4.2, 6.75, 'THE PROBLEM', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, family='sans-serif')
    ax.text(1.0, 6.0, 'Enterprise clients supply marketing-heavy copy that fails with strict specialists.', fontsize=8, color=LTGRAY, family='sans-serif')
    ax.text(1.0, 5.5, 'Underperformance → sponsor blames TLDR → churn.', fontsize=8, color=LTGRAY, family='sans-serif')

    draw_box(ax, 8.2, 5.2, 7.2, 1.8, color=GREEN, header_height=0.5)
    ax.text(11.8, 6.75, 'THE SOLUTION', ha='center', va='center', fontsize=10, fontweight='bold', color=WHITE, family='sans-serif')
    ax.text(8.6, 6.0, 'Dedicated B2B CS Pod as "Copywriting Consultants"', fontsize=8, color=LTGRAY, family='sans-serif')
    ax.text(8.6, 5.5, 'Pre-campaign workshops • Specialist\'s Proof rewrites • Performance reviews', fontsize=8, color=LTGRAY, family='sans-serif')

    draw_box(ax, 0.6, 2.5, 7.2, 2.2, color=CORAL)
    ax.text(1.0, 4.2, 'BEFORE (What sponsors submit):', fontsize=8, fontweight='bold', color=CORAL, family='sans-serif')
    ax.text(1.0, 3.4, '"Reach professionals fast! Try our platform free."', fontsize=9, color=GRAY, family='sans-serif', style='italic')

    draw_box(ax, 8.2, 2.5, 7.2, 2.2, color=GREEN)
    ax.text(8.6, 4.2, 'AFTER (Specialist\'s Proof rewrite):', fontsize=8, fontweight='bold', color=GREEN, family='sans-serif')
    ax.text(8.6, 3.4, '"Kubernetes clusters don\'t auto-heal.\nSee how Datadog\'s OPA integration catches\npolicy violations before your 3AM PagerDuty."', fontsize=8, color=LTGRAY, family='sans-serif')

    draw_box(ax, 0.6, 1.1, 14.8, 1.1, color=AMBER)
    ax.text(8.0, 1.65, 'ROI GUARANTEE:  For first-time $50K+ sponsors, if campaign delivers fewer than pre-agreed verified clicks → bonus placements at no cost.',
            ha='center', va='center', fontsize=8, color=LTGRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-09-white-glove.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 9 wireframe saved')


def slide_16():
    fig, ax = new_slide(16)
    apply_template(ax, 16)

    questions = [
        ('1', 'EDITORIAL INTEGRITY vs. MONETIZATION',
         'As we rely heavier on B2B data exhaust (tracking user clicks to sell intent data),\nhow do we balance monetization with our core brand promise of respecting\nsubscriber privacy and zero-fluff ethics?', TEAL),
        ('2', 'SECONDARY MONETIZATION WEDGE',
         'If native ad performance drops due to market saturation, do we have a secondary\nmonetization wedge ready? Candidates: premium B2C subscriptions (TLDR Pro),\nproprietary B2B data API, TLDR job board.', PURPLE),
        ('3', 'INTERNATIONAL EXPANSION',
         'Is there a localized playbook for launching TLDR editions in Europe (DACH, UK)\nand Asia (India, Southeast Asia), where specialist talent density is massive\nbut the media landscape is even more fragmented?', AMBER),
    ]
    for i, (num, title, desc, color) in enumerate(questions):
        y = 5.3 - i * 2.0
        draw_box(ax, 0.6, y, 14.8, 1.6, color=color)
        ax.text(1.2, y + 1.2, num, fontsize=16, fontweight='bold', color=color, va='center', family='sans-serif',
                bbox={'boxstyle': 'circle,pad=0.3', 'facecolor': color, 'edgecolor': 'none', 'alpha': 0.2})
        ax.text(2.2, y + 1.2, title, fontsize=10, fontweight='bold', color=WHITE, va='center', family='sans-serif')
        ax.text(2.2, y + 0.5, desc, fontsize=7, color=LTGRAY, family='sans-serif')

    fig.savefig('tldr-wireframes/slide-16-unasked-questions.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 16 wireframe saved')


if __name__ == '__main__':
    if not os.path.exists('tldr-wireframes'):
        os.makedirs('tldr-wireframes')

    print(f'Generating {TOTAL_SLIDES} slide wireframes with new order...\n')
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
    print(f'\n✅ All {TOTAL_SLIDES} wireframes generated successfully!')

    # Regenerating the consolidated deck image
    from PIL import Image
    files = sorted([f for f in os.listdir('tldr-wireframes') if f.endswith('.png') and f != 'tldr_full_deck_wireframe.png'])
    images = [Image.open(os.path.join('tldr-wireframes', f)) for f in files]
    gap = 20
    total_width = max(img.width for img in images)
    total_height = sum(img.height for img in images) + gap * (len(images) - 1)
    combined = Image.new('RGB', (total_width, total_height), color=(27, 35, 51))
    y_offset = 0
    for img in images:
        combined.paste(img, ((total_width - img.width) // 2, y_offset))
        y_offset += img.height + gap
    output_path = 'tldr-wireframes/tldr_full_deck_wireframe.png'
    combined.save(output_path, quality=95)
    print(f'✅ Combined layout saved to {output_path} ({combined.width}x{combined.height})')
