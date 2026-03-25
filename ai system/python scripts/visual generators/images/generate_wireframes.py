#!/usr/bin/env python3
"""
Generate precise slide wireframes for the Lambda GTM Technology presentation.
Each wireframe shows exact layout, placeholder boxes, and content areas for Canva reproduction.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

# ── Color palette ──────────────────────────────────────────────────────
BG      = '#1B2333'   # Dark navy
CARD_BG = '#232F42'   # Slightly lighter card bg
TEAL    = '#00BFA5'   # Teal accent
WHITE   = '#FFFFFF'
GRAY    = '#8A94A6'   # Muted text
LTGRAY  = '#C5CDD9'
DASHED  = '#4A5568'   # Dashed border color
AMBER   = '#FFB74D'   # Warning/callout accent

SLIDE_W = 16
SLIDE_H = 9


def new_slide(fig_num=1):
    """Create a new 16:9 slide canvas."""
    fig, ax = plt.subplots(1, 1, figsize=(SLIDE_W, SLIDE_H), num=fig_num)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(0, SLIDE_W)
    ax.set_ylim(0, SLIDE_H)
    ax.axis('off')
    return fig, ax


def draw_box(ax, x, y, w, h, label='', sublabel='', color=TEAL, dashed=False, fill=True, fontsize=9, sublabel_fontsize=7.5, header_height=None, text_color=WHITE):
    """Draw a labeled box (card style)."""
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
                fontsize=sublabel_fontsize, color=GRAY, family='sans-serif', style='italic',
                wrap=True)


def draw_bullet_placeholder(ax, x, y, width, lines, fontsize=7.5, color=GRAY):
    """Draw placeholder bullet lines."""
    for i, line in enumerate(lines):
        ax.plot([x, x + 0.12], [y - i*0.3, y - i*0.3], color=TEAL, linewidth=2, solid_capstyle='round')
        ax.text(x + 0.22, y - i*0.3, line, va='center', fontsize=fontsize, color=color, family='sans-serif')


def draw_arrow(ax, x1, y1, x2, y2, color=TEAL):
    """Draw an arrow between two points."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))


def add_slide_number(ax, num):
    """Add slide number badge."""
    ax.text(SLIDE_W - 0.4, 0.3, str(num), ha='center', va='center',
            fontsize=10, fontweight='bold', color=BG, family='sans-serif',
            bbox=dict(boxstyle='circle,pad=0.3', facecolor=TEAL, edgecolor='none'))


def add_accent_bar(ax):
    """Add bottom teal accent bar."""
    rect = plt.Rectangle((0, 0), SLIDE_W, 0.06, facecolor=TEAL, edgecolor='none')
    ax.add_patch(rect)


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 1: Executive Summary & Strategic Frame
# ═══════════════════════════════════════════════════════════════════════
def slide_1():
    fig, ax = new_slide(1)

    # Title
    ax.text(0.6, 8.2, 'EXECUTIVE SUMMARY & STRATEGIC FRAME', fontsize=22, fontweight='bold',
            color=WHITE, family='sans-serif')

    # Logo placeholder
    draw_box(ax, 13.8, 7.8, 1.8, 0.9, label='[LAMBDA LOGO]', color=DASHED, dashed=True, fill=False, fontsize=8)

    # Subtitle
    ax.text(0.6, 7.5, 'Turning GTM Systems from Constraint to Competitive Advantage',
            fontsize=13, color=TEAL, family='sans-serif', style='italic')

    # Divider line
    ax.plot([0.6, 15.4], [7.2, 7.2], color=DASHED, linewidth=0.5)

    # Left content box - Key Messages
    draw_box(ax, 0.6, 1.2, 8.8, 5.8, color=TEAL)
    ax.text(1.0, 6.6, 'KEY MESSAGES', fontsize=11, fontweight='bold', color=TEAL, family='sans-serif')

    bullets = [
        '[CONTEXT]  Lambda serves 3 GTM motions: self-serve,',
        '                   mid-market, enterprise — all scaling fast',
        '',
        '[DIAGNOSIS]  "Every major GTM friction maps to a missing',
        '                        decision about ownership, automation, or',
        '                        governance — not missing tools."',
        '',
        '[SCOPE]  This presentation: Current State → Target',
        '                 Architecture → AI Strategy → Operating Model',
        '',
        '[PHILOSOPHY]  Single source of truth per domain,',
        '                          event-driven AI, governance that enables speed',
    ]
    for i, line in enumerate(bullets):
        c = LTGRAY if not line.startswith('[') else WHITE
        fw = 'bold' if line.startswith('[') else 'normal'
        ax.text(1.2, 6.1 - i*0.42, line, fontsize=8.5, color=c, fontweight=fw, family='sans-serif')

    # Right visual placeholder
    draw_box(ax, 10.0, 1.2, 5.4, 5.8, dashed=True, fill=False, color=DASHED)
    ax.text(12.7, 4.5, '[VISUAL]', fontsize=14, fontweight='bold', color=DASHED, ha='center', family='sans-serif')
    ax.text(12.7, 3.8, 'Strategic Transformation\nGraphic', fontsize=10, color=GRAY,
            ha='center', family='sans-serif', linespacing=1.5)
    ax.text(12.7, 2.8, 'Fragmented → Unified', fontsize=9, color=TEAL, ha='center', family='sans-serif')
    # Sketch: scattered dots → connected nodes
    for dx, dy in [(-1.5, -0.3), (-0.8, 0.4), (-.3, -0.6), (-1.2, -0.8)]:
        ax.plot(12.0+dx, 2.0+dy, 'o', color=GRAY, markersize=5, alpha=0.4)
    ax.text(12.7, 1.5, '→', fontsize=20, color=TEAL, ha='center', va='center')
    for dx, dy in [(0.5, -0.3), (1.2, 0.4), (1.7, -0.6), (0.8, -0.8)]:
        ax.plot(12.0+dx, 2.0+dy, 'o', color=TEAL, markersize=5, alpha=0.7)

    add_accent_bar(ax)
    add_slide_number(ax, 1)
    ax.text(0.6, 0.3, 'SLIDE 1 OF 8', fontsize=7, color=GRAY, family='sans-serif')

    fig.savefig('slide-wireframes/slide-1-wireframe.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 1 wireframe saved')


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 2: Stack Assessment — Where the System Breaks Today
# ═══════════════════════════════════════════════════════════════════════
def slide_2():
    fig, ax = new_slide(2)

    # Title
    ax.text(0.6, 8.2, 'STACK ASSESSMENT — WHERE THE SYSTEM BREAKS TODAY', fontsize=20, fontweight='bold',
            color=WHITE, family='sans-serif')

    # Executive synthesis callout
    synth_box = FancyBboxPatch((0.6, 7.0), 14.8, 0.85, boxstyle="round,pad=0.08",
                                facecolor='none', edgecolor=TEAL, linewidth=1.5)
    ax.add_patch(synth_box)
    ax.text(8.0, 7.42, '[EXEC SYNTHESIS]  Every friction maps to missing ownership, automation,\n'
            'or governance — not missing tools.', ha='center', va='center',
            fontsize=9.5, color=TEAL, fontweight='bold', family='sans-serif', linespacing=1.4)

    # 2x3 grid of friction boxes
    box_w, box_h = 4.7, 2.6
    gap_x, gap_y = 0.35, 0.3
    start_x, start_y = 0.6, 1.0

    frictions = [
        ('1. IDENTITY & LIFECYCLE\n    FRAGMENTATION',
         ['Accounts/contacts don\'t resolve across systems',
          'Different "customer" definitions per tool',
          'Parent-child hierarchy drift']),
        ('2. SCATTERED ACTIVITY\n    & ENGAGEMENT',
         ['Buyer journey split across 7+ tools',
          'No single place for complete journey',
          'Attribution is argument-driven']),
        ('3. QUOTE → CONTRACT →\n    PROVISION → BILL',
         ['CPQ/DocuSign/Jira/Chargebee loosely coupled',
          'Signed status lives only in DocuSign',
          'SKU definitions drift between systems']),
        ('4. ROUTING & EXCEPTION\n    SPRAWL',
         ['LeanData logic becomes spaghetti',
          'Shadow workflows bypass CRM',
          'SLA tracking requires ops intervention']),
        ('5. POST-SALES\n    ESCALATIONS',
         ['Zendesk→Slack→Jira loop, no SoR',
          'CSMs manually build renewal narratives',
          'Support history invisible in CS views']),
        ('6. ANALYTICS ≠\n    BUSINESS TRUTH',
         ['Tableau sits on inconsistent joins',
          'Different teams, different tool answers',
          'Dashboards polished, decisions debated']),
    ]

    for idx, (title, bullets) in enumerate(frictions):
        col = idx % 3
        row = idx // 3
        x = start_x + col * (box_w + gap_x)
        y = start_y + (1 - row) * (box_h + gap_y)

        draw_box(ax, x, y, box_w, box_h, color=TEAL, header_height=0.65)
        ax.text(x + 0.2, y + box_h - 0.33, title, fontsize=8, fontweight='bold',
                color=WHITE, family='sans-serif', va='center')
        for bi, b in enumerate(bullets):
            ax.plot([x + 0.2, x + 0.32], [y + box_h - 1.0 - bi*0.4, y + box_h - 1.0 - bi*0.4],
                    color=TEAL, linewidth=2, solid_capstyle='round')
            ax.text(x + 0.42, y + box_h - 1.0 - bi*0.4, b, fontsize=7, color=LTGRAY,
                    va='center', family='sans-serif')

    # Root cause callout
    callout = FancyBboxPatch((11.5, 0.15), 4.0, 0.6, boxstyle="round,pad=0.08",
                              facecolor=AMBER, edgecolor='none', alpha=0.15)
    ax.add_patch(callout)
    ax.text(13.5, 0.45, '⚡ ROOT CAUSE: Identity resolution', ha='center', va='center',
            fontsize=8.5, fontweight='bold', color=AMBER, family='sans-serif')

    add_accent_bar(ax)
    add_slide_number(ax, 2)
    ax.text(0.6, 0.3, 'SLIDE 2 OF 8  |  TASK 1a', fontsize=7, color=GRAY, family='sans-serif')

    fig.savefig('slide-wireframes/slide-2-wireframe.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 2 wireframe saved')


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 3: Source of Truth Map & Scalability Stress Test
# ═══════════════════════════════════════════════════════════════════════
def slide_3():
    fig, ax = new_slide(3)

    # Title
    ax.text(0.6, 8.2, 'SOURCE OF TRUTH MAP & SCALABILITY STRESS TEST', fontsize=20, fontweight='bold',
            color=WHITE, family='sans-serif')
    ax.plot([0.6, 15.4], [7.95, 7.95], color=DASHED, linewidth=0.5)

    # ── LEFT HALF: Source of Truth ──
    ax.text(0.8, 7.6, 'SOURCE OF TRUTH  (ONE-GLANCE VIEW)', fontsize=11, fontweight='bold',
            color=TEAL, family='sans-serif')

    sot_items = [
        ('Salesforce', 'Commercial & Lifecycle Spine', TEAL),
        ('Chargebee', 'Financial Truth (MRR, Invoices)', '#4FC3F7'),
        ('Marketing Tools', 'Signal Providers, NOT Truth', GRAY),
        ('Sales & CS Tools', 'Context Providers, NOT Record Keepers', GRAY),
        ('Tableau', 'Mirror, NOT Referee', GRAY),
    ]

    for i, (system, role, color) in enumerate(sot_items):
        y = 6.8 - i * 1.1
        # Bar background
        bar = FancyBboxPatch((0.8, y), 7.0, 0.8, boxstyle="round,pad=0.05",
                              facecolor=CARD_BG, edgecolor=color, linewidth=1.2, alpha=0.9)
        ax.add_patch(bar)
        # System name (bold left)
        ax.text(1.1, y + 0.4, system, fontsize=9, fontweight='bold', color=WHITE, va='center', family='sans-serif')
        # Role (right-aligned or after)
        ax.text(7.5, y + 0.4, '= ' + role, fontsize=8, color=color, va='center', ha='right', family='sans-serif')

    # ── Vertical divider ──
    ax.plot([8.2, 8.2], [1.0, 7.8], color=DASHED, linewidth=1, linestyle='--')

    # ── RIGHT HALF: Scalability Stress Test ──
    ax.text(8.6, 7.6, '5 GTM MOTIONS THAT STRESS THE SYSTEM', fontsize=11, fontweight='bold',
            color=TEAL, family='sans-serif')

    motions = [
        ('PLG / Product-Led', 'Identity resolution + PQL routing', '⚠'),
        ('Partners / Channel', 'Attribution + crediting + ownership', '⚠'),
        ('Enterprise Scaling', 'CPQ complexity + order-to-activation', '⚠'),
        ('International', 'Data compliance + regional billing', '⚠'),
        ('NRR as North Star', 'Chargebee ↔ SF ↔ Vitally stitching', '⚠'),
    ]

    for i, (motion, breaks, icon) in enumerate(motions):
        y = 6.8 - i * 1.1
        # Motion box
        bar = FancyBboxPatch((8.6, y), 6.8, 0.8, boxstyle="round,pad=0.05",
                              facecolor=CARD_BG, edgecolor=DASHED, linewidth=1)
        ax.add_patch(bar)
        ax.text(8.9, y + 0.55, motion, fontsize=9, fontweight='bold', color=WHITE,
                va='center', family='sans-serif')
        ax.text(8.9, y + 0.2, 'BREAKS: ' + breaks, fontsize=7.5, color=AMBER,
                va='center', family='sans-serif')

    add_accent_bar(ax)
    add_slide_number(ax, 3)
    ax.text(0.6, 0.3, 'SLIDE 3 OF 8  |  TASK 1b & 1c', fontsize=7, color=GRAY, family='sans-serif')

    fig.savefig('slide-wireframes/slide-3-wireframe.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 3 wireframe saved')


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 4: Target-State GTM Technology Architecture
# ═══════════════════════════════════════════════════════════════════════
def slide_4():
    fig, ax = new_slide(4)

    # Title
    ax.text(0.6, 8.2, 'TARGET-STATE GTM TECHNOLOGY ARCHITECTURE', fontsize=20, fontweight='bold',
            color=WHITE, family='sans-serif')
    ax.text(0.6, 7.7, '12–18 Month North Star  |  Lead → Cash → Renewal', fontsize=11,
            color=TEAL, family='sans-serif', style='italic')

    # ── Architecture diagram area ──
    diag_y = 3.0
    diag_h = 4.2
    box_w = 2.3
    box_h = 3.2
    gap = 0.25
    start_x = 0.8

    layers = [
        ('MARKETING\n& INTENT', ['HubSpot', '6sense', 'Apollo', 'Gong', 'Highspot', 'Reachdesk'], '#4FC3F7'),
        ('SALES &\nLEGAL', ['Salesforce CRM', 'Salesforce CPQ', 'LeanData', 'DocuSign'], TEAL),
        ('PROVISIONING', ['Jira', '(Activation', 'Tickets)'], '#FFB74D'),
        ('REVENUE /\nFINANCE', ['Chargebee', 'Quotapath'], '#AB47BC'),
        ('CS &\nSUPPORT', ['Vitally', 'Zendesk', 'Front'], '#66BB6A'),
    ]

    box_positions = []
    for i, (title, tools, color) in enumerate(layers):
        x = start_x + i * (box_w + gap)
        box_positions.append((x, diag_y, box_w, box_h))

        # Box
        rect = FancyBboxPatch((x, diag_y), box_w, box_h, boxstyle="round,pad=0.08",
                              facecolor=CARD_BG, edgecolor=color, linewidth=1.5)
        ax.add_patch(rect)

        # Header
        header = FancyBboxPatch((x, diag_y + box_h - 0.8), box_w, 0.8,
                                boxstyle="round,pad=0.08", facecolor=color, edgecolor=color,
                                linewidth=0, alpha=0.3)
        ax.add_patch(header)
        ax.text(x + box_w/2, diag_y + box_h - 0.4, title, ha='center', va='center',
                fontsize=8, fontweight='bold', color=WHITE, family='sans-serif')

        # Tools list
        for ti, tool in enumerate(tools):
            ax.text(x + box_w/2, diag_y + box_h - 1.2 - ti*0.35, tool, ha='center', va='center',
                    fontsize=7, color=LTGRAY, family='sans-serif')

        # Arrow to next box
        if i < len(layers) - 1:
            ax.annotate('', xy=(x + box_w + gap - 0.05, diag_y + box_h/2),
                       xytext=(x + box_w + 0.05, diag_y + box_h/2),
                       arrowprops=dict(arrowstyle='->', color=TEAL, lw=1.5))

    # Renewal loop arrow (curved, from CS back to Sales)
    ax.annotate('', xy=(start_x + 1*(box_w+gap) + box_w/2, diag_y - 0.15),
               xytext=(start_x + 4*(box_w+gap) + box_w/2, diag_y - 0.15),
               arrowprops=dict(arrowstyle='->', color=AMBER, lw=1.5,
                              connectionstyle='arc3,rad=0.3'))
    ax.text(start_x + 2.5*(box_w+gap) + box_w/2, diag_y - 0.55, '↺ RENEWAL LOOP',
            ha='center', fontsize=8, fontweight='bold', color=AMBER, family='sans-serif')

    # Data Platform bar (bottom of diagram)
    dp_y = 2.0
    dp = FancyBboxPatch((0.8, dp_y), 14.6, 0.7, boxstyle="round,pad=0.08",
                         facecolor=CARD_BG, edgecolor='#78909C', linewidth=1.5)
    ax.add_patch(dp)
    ax.text(8.1, dp_y + 0.35, 'DATA PLATFORM    Fivetran → dbt → Snowflake / BigQuery → Tableau',
            ha='center', va='center', fontsize=9, fontweight='bold', color='#78909C', family='sans-serif')

    # Arrows from each box down to data platform
    for i in range(5):
        x = start_x + i * (box_w + gap) + box_w/2
        ax.plot([x, x], [diag_y, dp_y + 0.7], color='#78909C', linewidth=0.7, linestyle=':', alpha=0.5)

    # ── Design Principles strip ──
    ax.text(0.8, 1.5, 'DESIGN PRINCIPLES', fontsize=9, fontweight='bold', color=TEAL, family='sans-serif')
    principles = ['1. Single SoT', '2. Audited\n   Handoffs', '3. Canonical\n   Identity',
                  '4. Auto +\n   Exceptions', '5. Fewer\n   P2P Links', '6. Speed +\n   Governance']
    for i, p in enumerate(principles):
        x = 0.8 + i * 2.5
        pill = FancyBboxPatch((x, 0.55), 2.2, 0.75, boxstyle="round,pad=0.08",
                              facecolor=CARD_BG, edgecolor=TEAL, linewidth=0.8, alpha=0.7)
        ax.add_patch(pill)
        ax.text(x + 1.1, 0.92, p, ha='center', va='center', fontsize=7, color=LTGRAY, family='sans-serif')

    add_accent_bar(ax)
    add_slide_number(ax, 4)
    ax.text(0.6, 0.15, 'SLIDE 4 OF 8  |  TASK 2', fontsize=7, color=GRAY, family='sans-serif')

    fig.savefig('slide-wireframes/slide-4-wireframe.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 4 wireframe saved')


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 5: High-Impact AI Opportunities Across the Stack
# ═══════════════════════════════════════════════════════════════════════
def slide_5():
    fig, ax = new_slide(5)

    # Title
    ax.text(0.6, 8.2, 'HIGH-IMPACT AI OPPORTUNITIES ACROSS THE STACK', fontsize=20, fontweight='bold',
            color=WHITE, family='sans-serif')
    ax.text(0.6, 7.65, 'Practical, defensible AI — tied to system events, governed, and measurable',
            fontsize=10, color=TEAL, family='sans-serif', style='italic')

    # ── Table header ──
    table_top = 7.1
    col_x = [0.6, 1.1, 5.2, 8.8, 12.0, 14.0]
    col_w = [0.5, 4.0, 3.5, 3.1, 1.9, 1.6]
    headers = ['#', 'AI OPPORTUNITY', 'STACK LOCATION', 'TYPE', 'KEY METRIC', '']

    # Header bar
    header_bar = plt.Rectangle((0.4, table_top - 0.05), 15.2, 0.5, facecolor=TEAL, edgecolor='none', alpha=0.2)
    ax.add_patch(header_bar)
    for i, h in enumerate(headers[:-1]):
        ax.text(col_x[i] + 0.05, table_top + 0.2, h, fontsize=7.5, fontweight='bold',
                color=TEAL, va='center', family='sans-serif')

    # ── Table rows ──
    opportunities = [
        ('1', 'Deal Desk Triage +\nRedline Readiness', 'CPQ + DocuSign\n+ Gong', 'Agent / Workflow\nOrchestration', 'Quote-to-sign\ncycle time ↓'),
        ('2', 'Account Identity Resolution\n+ Duplicate Prevention', 'Salesforce CRM +\nenrichment tools', 'Automation +\nDecision Support', 'Duplicate rate ↓\nRouting exceptions ↓'),
        ('3', 'Intent-to-Pipeline\nPrioritization', '6sense + SF +\nHubSpot + Gong', 'Decision Support +\nLight Automation', 'SDR meetings per\n100 accounts ↑'),
        ('4', 'Forecast Risk\nDetector', 'SF + Gong +\nCPQ + DocuSign', 'Decision\nSupport', 'Forecast accuracy ↑\nSlippage ↓'),
        ('5', 'Support-to-Renewal\nTranslator', 'Zendesk + Vitally\n+ Salesforce', 'Agent / Workflow\nOrchestration', 'Churn ↓\nNRR ↑'),
        ('6', 'Billing Anomaly +\nCollections Priority', 'Chargebee +\nSF + Tableau', 'Automation +\nOrchestration', 'DSO ↓\nInvoluntary churn ↓'),
    ]

    row_h = 0.93
    for ri, (num, opp, loc, typ, metric) in enumerate(opportunities):
        y = table_top - 0.65 - ri * row_h
        # Alternate row shading
        if ri % 2 == 0:
            row_bg = plt.Rectangle((0.4, y - 0.15), 15.2, row_h, facecolor=CARD_BG, edgecolor='none', alpha=0.4)
            ax.add_patch(row_bg)

        # Number circle
        ax.text(col_x[0] + 0.15, y + 0.25, num, ha='center', va='center', fontsize=10, fontweight='bold',
                color=BG, family='sans-serif',
                bbox=dict(boxstyle='circle,pad=0.2', facecolor=TEAL, edgecolor='none'))

        vals = [None, opp, loc, typ, metric]
        colors = [None, WHITE, LTGRAY, LTGRAY, AMBER]
        sizes = [None, 8.5, 7.5, 7.5, 7.5]
        for ci in range(1, 5):
            ax.text(col_x[ci] + 0.05, y + 0.25, vals[ci], fontsize=sizes[ci],
                    color=colors[ci], va='center', family='sans-serif')

    # ── Footer: Why defensible ──
    ax.plot([0.6, 15.4], [0.9, 0.9], color=DASHED, linewidth=0.5)
    ax.text(0.8, 0.55, 'WHY DEFENSIBLE:', fontsize=8, fontweight='bold', color=TEAL, family='sans-serif')
    ax.text(3.2, 0.55, 'Sit on existing system events  •  Structured write-backs to SoR  •  Human-in-the-loop governance  •  Measurable revenue-linked outcomes',
            fontsize=7.5, color=GRAY, family='sans-serif')

    add_accent_bar(ax)
    add_slide_number(ax, 5)
    ax.text(0.6, 0.15, 'SLIDE 5 OF 8  |  TASK 3', fontsize=7, color=GRAY, family='sans-serif')

    fig.savefig('slide-wireframes/slide-5-wireframe.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 5 wireframe saved')


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 6: AI & Data Architecture
# ═══════════════════════════════════════════════════════════════════════
def slide_6():
    fig, ax = new_slide(6)

    # Title
    ax.text(0.6, 8.2, 'AI & DATA ARCHITECTURE', fontsize=20, fontweight='bold',
            color=WHITE, family='sans-serif')
    ax.text(0.6, 7.65, 'AI Control Plane: Unified Data → Governed AI Services → Write-back to Systems of Record',
            fontsize=10, color=TEAL, family='sans-serif', style='italic')

    # ── 5-box horizontal flow diagram ──
    boxes_data = [
        ('SOURCE\nSYSTEMS', 'Salesforce/CPQ\nHubSpot · Gong\nChargebee\nZendesk · Vitally\nDocuSign · 6sense\nFront · Jira', '#4FC3F7'),
        ('INTEGRATION\n+ EVENT LAYER', 'Webhooks / CDC\nBatch sync\nNormalization\nCanonical IDs\nCrosswalk tables', '#78909C'),
        ('UNIFIED\nDATA LAYER', 'Operational Store\n(AI feature store:\nlatest state +\nrecent events)\n─────────\nWarehouse\n(full history)', '#AB47BC'),
        ('AI CONTROL\nPLANE', 'Policy / RBAC\nRetrieval + context\nOrchestration\nEvaluation\nConfidence\nthresholds', TEAL),
        ('ACTION +\nUX LAYER', 'Write-backs to\nSF / Zendesk /\nVitally\n─────────\nTableau metrics\nSlack notifications', '#66BB6A'),
    ]

    box_w = 2.6
    box_h = 4.0
    gap = 0.3
    start_x = 0.6
    diag_y = 3.2

    for i, (title, content, color) in enumerate(boxes_data):
        x = start_x + i * (box_w + gap)

        # Box
        rect = FancyBboxPatch((x, diag_y), box_w, box_h, boxstyle="round,pad=0.08",
                              facecolor=CARD_BG, edgecolor=color, linewidth=1.5)
        ax.add_patch(rect)

        # Header
        header = FancyBboxPatch((x, diag_y + box_h - 0.8), box_w, 0.8,
                                boxstyle="round,pad=0.08", facecolor=color, edgecolor=color,
                                linewidth=0, alpha=0.3)
        ax.add_patch(header)
        ax.text(x + box_w/2, diag_y + box_h - 0.4, title, ha='center', va='center',
                fontsize=8, fontweight='bold', color=WHITE, family='sans-serif')

        # Content
        lines = content.split('\n')
        for li, line in enumerate(lines):
            ax.text(x + box_w/2, diag_y + box_h - 1.2 - li*0.35, line, ha='center', va='center',
                    fontsize=6.5, color=LTGRAY, family='sans-serif')

        # Arrow
        if i < len(boxes_data) - 1:
            arrow_x = x + box_w + 0.03
            ax.annotate('', xy=(arrow_x + gap - 0.06, diag_y + box_h/2),
                       xytext=(arrow_x, diag_y + box_h/2),
                       arrowprops=dict(arrowstyle='->', color=TEAL, lw=2))

    # ── 6 Principle pills at bottom ──
    ax.text(0.6, 2.65, 'ARCHITECTURE PRINCIPLES', fontsize=9, fontweight='bold', color=TEAL, family='sans-serif')

    principles = [
        ('Unify identity first', '#4FC3F7'),
        ('Event-driven AI', TEAL),
        ('Central brain,\nembedded UX', '#AB47BC'),
        ('Trust by design\n(reason codes)', AMBER),
        ('Reusable building\nblocks', '#66BB6A'),
        ('No lock-in\n(adapters + SoR)', '#78909C'),
    ]

    for i, (p, color) in enumerate(principles):
        x = 0.6 + i * 2.55
        pill = FancyBboxPatch((x, 1.15), 2.3, 1.15, boxstyle="round,pad=0.08",
                              facecolor=CARD_BG, edgecolor=color, linewidth=1, alpha=0.8)
        ax.add_patch(pill)
        ax.text(x + 1.15, 1.72, p, ha='center', va='center', fontsize=7, color=LTGRAY,
                family='sans-serif', linespacing=1.3)

    add_accent_bar(ax)
    add_slide_number(ax, 6)
    ax.text(0.6, 0.3, 'SLIDE 6 OF 8  |  TASK 4', fontsize=7, color=GRAY, family='sans-serif')

    fig.savefig('slide-wireframes/slide-6-wireframe.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 6 wireframe saved')


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 7: Operating Model & Governance
# ═══════════════════════════════════════════════════════════════════════
def slide_7():
    fig, ax = new_slide(7)

    # Title
    ax.text(0.6, 8.2, 'OPERATING MODEL & GOVERNANCE', fontsize=20, fontweight='bold',
            color=WHITE, family='sans-serif')
    ax.plot([0.6, 15.4], [7.95, 7.95], color=DASHED, linewidth=0.5)

    # ── 4 quadrant layout ──
    qw, qh = 7.2, 3.0
    gap = 0.4

    # Q1: Intake & Prioritization (top-left)
    x, y = 0.6, 4.5
    draw_box(ax, x, y, qw, qh, color=TEAL)
    ax.text(x + 0.3, y + qh - 0.3, 'INTAKE & PRIORITIZATION', fontsize=10, fontweight='bold',
            color=TEAL, family='sans-serif')
    items = [
        'Single front door: intake form + Slack + weekly triage',
        'Weekly GTM Systems Triage (30-45 min)',
        'Monthly steering: VP Sales, VP CS, Marketing, Finance, IT',
        '6-factor scoring: revenue impact, risk, time-to-value,',
        '     adoption certainty, platform leverage, data readiness',
        'Governance: SoR map, field governance, release calendar',
    ]
    for i, item in enumerate(items):
        ax.text(x + 0.3, y + qh - 0.75 - i*0.35, '•  ' + item, fontsize=7, color=LTGRAY, family='sans-serif')

    # Q2: Cross-Functional Partnerships (top-right)
    x, y = 0.6 + qw + gap, 4.5
    draw_box(ax, x, y, qw, qh, color='#4FC3F7')
    ax.text(x + 0.3, y + qh - 0.3, 'CROSS-FUNCTIONAL PARTNERSHIPS', fontsize=10, fontweight='bold',
            color='#4FC3F7', family='sans-serif')
    items = [
        'RevOps = GTM process owner (routing, stages, SLAs)',
        'Finance = revenue truth (ARR/MRR, billing policy)',
        'IT = platform reliability (SSO, integrations, vendors)',
        'Security = guardrails (PII, access, audit)',
        'Legal = contracts + data handling (DPAs, retention)',
        '─── Working agreements ───',
        '"No write-backs without an owner"',
        '"Security early, not as a gate"',
    ]
    for i, item in enumerate(items):
        c = LTGRAY if not item.startswith('───') else '#4FC3F7'
        sz = 7 if not item.startswith('───') else 6.5
        ax.text(x + 0.3, y + qh - 0.75 - i*0.32, '•  ' + item if not item.startswith('───') else item,
                fontsize=sz, color=c, family='sans-serif')

    # Q3: AI Governance (bottom-left)
    x, y = 0.6, 1.1
    draw_box(ax, x, y, qw, qh, color=AMBER)
    ax.text(x + 0.3, y + qh - 0.3, 'AI GOVERNANCE (3 TIERS)', fontsize=10, fontweight='bold',
            color=AMBER, family='sans-serif')
    items = [
        'Tier 1 (LOW risk): Summarization, tagging → automate faster',
        'Tier 2 (MED risk): Workflow recommendations → human approval',
        'Tier 3 (HIGH risk): Customer-facing / financial → strict review',
        '── Controls ──',
        'Human-in-the-loop for Tier 2/3',
        'Reason codes + evidence links + audit logs',
        'Kill switch + rollback for every AI automation',
    ]
    for i, item in enumerate(items):
        c = LTGRAY if not item.startswith('──') else AMBER
        ax.text(x + 0.3, y + qh - 0.75 - i*0.33, '•  ' + item if not item.startswith('──') else item,
                fontsize=7, color=c, family='sans-serif')

    # Q4: Adoption + What NOT to Build (bottom-right)
    x, y = 0.6 + qw + gap, 1.1
    draw_box(ax, x, y, qw, qh, color='#66BB6A')
    ax.text(x + 0.3, y + qh - 0.3, 'ADOPTION  +  WHAT NOT TO BUILD', fontsize=10, fontweight='bold',
            color='#66BB6A', family='sans-serif')
    items = [
        'Build into where work happens (SF, Zendesk, Vitally)',
        'Default-on reporting: show usage + what\'s ignored',
        'Role-based enablement + "what changed" Looms',
        '── First 6 months: explicitly AVOID ──',
        'Customer-facing AI (auto-emails, pricing msgs)',
        'Big-bang CRM/warehouse rebuilds',
        'Complex multi-model agents without proven triggers',
        'Automating broken processes (fix process first)',
    ]
    for i, item in enumerate(items):
        c = LTGRAY if not item.startswith('──') else '#66BB6A'
        ax.text(x + 0.3, y + qh - 0.75 - i*0.31, '•  ' + item if not item.startswith('──') else item,
                fontsize=7, color=c, family='sans-serif')

    add_accent_bar(ax)
    add_slide_number(ax, 7)
    ax.text(0.6, 0.3, 'SLIDE 7 OF 8  |  TASK 5', fontsize=7, color=GRAY, family='sans-serif')

    fig.savefig('slide-wireframes/slide-7-wireframe.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 7 wireframe saved')


# ═══════════════════════════════════════════════════════════════════════
# SLIDE 8: 90-Day Roadmap & Execution Plan
# ═══════════════════════════════════════════════════════════════════════
def slide_8():
    fig, ax = new_slide(8)

    # Title
    ax.text(0.6, 8.2, '90-DAY ROADMAP & EXECUTION PLAN', fontsize=20, fontweight='bold',
            color=WHITE, family='sans-serif')
    ax.text(0.6, 7.65, 'Highest ROI, Lowest Regret  |  Phased Delivery with Measurable Outcomes',
            fontsize=10, color=TEAL, family='sans-serif', style='italic')

    # ── 3-phase timeline ──
    phase_w = 4.6
    phase_h = 4.2
    phase_gap = 0.3
    phase_y = 3.0

    phases = [
        ('DAYS 0–30', 'STABILIZE + ALIGN\n+ 2 QUICK WINS', TEAL,
         ['Confirm SoR map + metric dictionary',
          'Stand up intake + triage + governance',
          '── Quick Wins ──',
          'Billing anomaly → finance queue',
          '  (Chargebee → SF case)',
          'Support burden summary',
          '  (Zendesk → Vitally/SF note)']),
        ('DAYS 31–60', 'REVENUE WORKFLOW\nACCELERATION', '#4FC3F7',
         ['Deal desk triage (CPQ + DocuSign)',
          '  → recommendation mode → write-backs',
          'Forecast risk detector',
          '  (SF + DocuSign + CPQ) mgr-facing',
          'Introduce baseline dashboards',
          'Establish adoption KPIs',
          '']),
        ('DAYS 61–90', 'SCALE FOUNDATIONS\n+ REDUCE FRAGMENTATION', '#AB47BC',
         ['Identity resolution for new records',
          '  (dedupe + account match)',
          'Harden integrations + monitoring',
          'Confidence thresholds + review queues',
          'Expand pilots (SDR pod,',
          '  one CS segment, one region)',
          '']),
    ]

    for i, (period, subtitle, color, items) in enumerate(phases):
        x = 0.6 + i * (phase_w + phase_gap)

        # Phase box
        rect = FancyBboxPatch((x, phase_y), phase_w, phase_h, boxstyle="round,pad=0.08",
                              facecolor=CARD_BG, edgecolor=color, linewidth=1.5)
        ax.add_patch(rect)

        # Period badge
        badge = FancyBboxPatch((x + 0.2, phase_y + phase_h - 0.55), 1.8, 0.4,
                               boxstyle="round,pad=0.08", facecolor=color, edgecolor='none', alpha=0.3)
        ax.add_patch(badge)
        ax.text(x + 1.1, phase_y + phase_h - 0.35, period, ha='center', va='center',
                fontsize=8.5, fontweight='bold', color=color, family='sans-serif')

        # Subtitle
        ax.text(x + phase_w/2, phase_y + phase_h - 0.95, subtitle, ha='center', va='center',
                fontsize=8, fontweight='bold', color=WHITE, family='sans-serif', linespacing=1.3)

        # Items
        for ii, item in enumerate(items):
            c = LTGRAY if not item.startswith('──') else color
            sz = 7 if not item.startswith('──') else 6.5
            prefix = '•  ' if item and not item.startswith('──') and not item.startswith('  ') else ''
            ax.text(x + 0.3, phase_y + phase_h - 1.65 - ii*0.33,
                    prefix + item, fontsize=sz, color=c, family='sans-serif')

        # Arrow between phases
        if i < 2:
            arrow_x = x + phase_w + 0.02
            ax.annotate('', xy=(arrow_x + phase_gap - 0.04, phase_y + phase_h/2),
                       xytext=(arrow_x, phase_y + phase_h/2),
                       arrowprops=dict(arrowstyle='->', color=TEAL, lw=2))

    # ── Day 90 target box ──
    target_y = 1.8
    target = FancyBboxPatch((0.6, target_y), 9.0, 0.85, boxstyle="round,pad=0.08",
                             facecolor=TEAL, edgecolor='none', alpha=0.15)
    ax.add_patch(target)
    ax.text(0.9, target_y + 0.42, 'DAY 90 TARGET:', fontsize=9, fontweight='bold',
            color=TEAL, va='center', family='sans-serif')
    ax.text(3.6, target_y + 0.42, '4 AI use cases operational  •  2 in scaled pilot  •  All with metrics & governance',
            fontsize=8, color=LTGRAY, va='center', family='sans-serif')

    # ── Evolution note ──
    evo = FancyBboxPatch((10.0, target_y), 5.4, 0.85, boxstyle="round,pad=0.08",
                          facecolor=CARD_BG, edgecolor=AMBER, linewidth=1)
    ax.add_patch(evo)
    ax.text(10.3, target_y + 0.55, 'EVOLVES WITH GROWTH:', fontsize=7.5, fontweight='bold',
            color=AMBER, family='sans-serif')
    ax.text(10.3, target_y + 0.2, 'Usage-based pricing → product events\nas first-class citizens', fontsize=7,
            color=GRAY, family='sans-serif', linespacing=1.3)

    # ── KPI preview strip ──
    ax.plot([0.6, 15.4], [1.5, 1.5], color=DASHED, linewidth=0.5)
    ax.text(0.8, 1.1, 'KEY METRICS:', fontsize=8, fontweight='bold', color=TEAL, family='sans-serif')
    kpis = ['Pipeline coverage', 'Cycle time', 'Forecast accuracy', 'NRR / GRR', 'DSO',
            'Duplicate rate ↓', 'Integration health']
    kpi_text = '  •  '.join(kpis)
    ax.text(3.0, 1.1, kpi_text, fontsize=7, color=GRAY, family='sans-serif')

    add_accent_bar(ax)
    add_slide_number(ax, 8)
    ax.text(0.6, 0.3, 'SLIDE 8 OF 8  |  TASK 5 + OPTIONAL', fontsize=7, color=GRAY, family='sans-serif')

    fig.savefig('slide-wireframes/slide-8-wireframe.png', dpi=150, bbox_inches='tight',
                facecolor=fig.get_facecolor(), pad_inches=0.2)
    plt.close(fig)
    print('✅ Slide 8 wireframe saved')


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════
if __name__ == '__main__':
    import os
    if not os.path.exists('slide-wireframes'):
        os.makedirs('slide-wireframes')
        print(f"Created directory: slide-wireframes")

    print('Generating 8 slide wireframes...\n')
    slide_1()
    slide_2()
    slide_3()
    slide_4()
    slide_5()
    slide_6()
    slide_7()
    slide_8()
    print('\n✅ All 8 wireframes generated in slide-wireframes/')
