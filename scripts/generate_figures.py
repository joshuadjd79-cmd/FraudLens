"""
FraudLens: Diagram & Figure Generation Script
Generates high-resolution publication-quality diagrams for the Review reports:
1. ER Diagram (erd_diagram.png)
2. System Architecture (architecture_flow.png)
3. Lifecycle Workflow (workflow_lifecycle.png)
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
ASSETS_DIR = os.path.join(DOCS_DIR, "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

def generate_er_diagram():
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 1200)
    ax.set_ylim(0, 750)
    ax.axis('off')
    
    # Background
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Palette
    header_color = '#1E3A8A'      # Deep Navy
    header_text_color = '#FFFFFF'
    box_bg = '#F8FAFC'            # Slate 50
    box_border = '#CBD5E1'        # Slate 300
    pk_color = '#B91C1C'          # Red 700
    fk_color = '#2563EB'          # Blue 600
    line_color = '#475569'        # Slate 600

    def draw_entity(x, y, w, h, name, attributes):
        # Card shadow / border
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=6",
                                     linewidth=1.2, edgecolor=box_border, facecolor=box_bg)
        ax.add_patch(rect)
        # Header banner
        header_h = 28
        header_rect = patches.FancyBboxPatch((x, y + h - header_h), w, header_h,
                                            boxstyle="round,pad=0,rounding_size=6",
                                            linewidth=1.2, edgecolor=header_color, facecolor=header_color)
        ax.add_patch(header_rect)
        # Header text
        ax.text(x + w/2, y + h - header_h/2, name, ha='center', va='center',
                fontsize=11, fontweight='bold', color=header_text_color, family='sans-serif')
        
        # Attributes
        line_y = y + h - header_h - 14
        for prefix, attr_name, attr_type in attributes:
            # Prefix color
            p_color = pk_color if prefix == 'PK' else (fk_color if 'FK' in prefix else '#64748B')
            ax.text(x + 10, line_y, prefix, ha='left', va='center', fontsize=8.5, fontweight='bold', color=p_color, family='monospace')
            ax.text(x + 40, line_y, attr_name, ha='left', va='center', fontsize=8.5, fontweight='semibold', color='#1E293B', family='sans-serif')
            ax.text(x + w - 10, line_y, attr_type, ha='right', va='center', fontsize=8, color='#64748B', family='monospace')
            line_y -= 17

    # Entity Definitions
    entities = {
        'CUSTOMER': (40, 480, 260, 220, [
            ('PK', 'customer_id', 'NUMBER(10)'),
            ('',   'first_name',  'VARCHAR2(50)'),
            ('',   'last_name',   'VARCHAR2(50)'),
            ('UQ', 'email',       'VARCHAR2(100)'),
            ('UQ', 'phone',       'VARCHAR2(15)'),
            ('',   'kyc_status',  'VARCHAR2(15)'),
            ('',   'risk_score',  'NUMBER(3)'),
            ('',   'created_at',  'DATE'),
        ]),
        'ACCOUNT': (370, 480, 260, 220, [
            ('PK', 'account_id',    'NUMBER(10)'),
            ('FK', 'customer_id',   'NUMBER(10)'),
            ('UQ', 'account_number', 'VARCHAR2(20)'),
            ('',   'account_type',  'VARCHAR2(20)'),
            ('',   'balance',       'NUMBER(15,2)'),
            ('',   'currency',      'VARCHAR2(5)'),
            ('',   'status',        'VARCHAR2(15)'),
            ('',   'created_at',    'DATE'),
        ]),
        'TRANSACTIONS': (700, 460, 280, 240, [
            ('PK', 'transaction_id', 'NUMBER(12)'),
            ('FK', 'account_id',     'NUMBER(10)'),
            ('',   'transaction_type', 'VARCHAR2(20)'),
            ('',   'amount',         'NUMBER(15,2)'),
            ('',   'transaction_date', 'TIMESTAMP'),
            ('',   'channel',        'VARCHAR2(20)'),
            ('',   'status',         'VARCHAR2(15)'),
            ('',   'counterparty_acc', 'VARCHAR2(30)'),
            ('',   'description',    'VARCHAR2(200)'),
        ]),
        'INVESTIGATOR': (40, 100, 260, 200, [
            ('PK', 'investigator_id', 'NUMBER(6)'),
            ('',   'first_name',      'VARCHAR2(50)'),
            ('',   'last_name',       'VARCHAR2(50)'),
            ('UQ', 'email',           'VARCHAR2(100)'),
            ('',   'department',      'VARCHAR2(50)'),
            ('',   'experience_years','NUMBER(3)'),
            ('',   'active_status',   'VARCHAR2(15)'),
        ]),
        'INVESTIGATION': (370, 100, 260, 220, [
            ('PK', 'investigation_id', 'NUMBER(10)'),
            ('FK,UQ', 'alert_id',      'NUMBER(10)'),
            ('FK', 'investigator_id',  'NUMBER(6)'),
            ('',   'start_date',       'DATE'),
            ('',   'end_date',         'DATE'),
            ('',   'status',           'VARCHAR2(15)'),
            ('',   'outcome',          'VARCHAR2(20)'),
            ('',   'notes',            'VARCHAR2(1000)'),
        ]),
        'FRAUD_ALERT': (700, 100, 280, 220, [
            ('PK', 'alert_id',       'NUMBER(10)'),
            ('FK', 'transaction_id', 'NUMBER(12)'),
            ('',   'alert_type',     'VARCHAR2(30)'),
            ('',   'severity',       'VARCHAR2(15)'),
            ('',   'rule_triggered', 'VARCHAR2(150)'),
            ('',   'alert_date',     'TIMESTAMP'),
            ('',   'status',         'VARCHAR2(15)'),
        ]),
    }

    for name, params in entities.items():
        x, y, w, h, attrs = params
        draw_entity(x, y, w, h, name, attrs)

    # Relationship connectors
    # CUSTOMER -> ACCOUNT (1:N)
    ax.annotate("", xy=(370, 590), xytext=(300, 590),
                arrowprops=dict(arrowstyle="->", color=line_color, lw=1.5))
    ax.text(335, 600, "1 : N\nowns", ha='center', va='bottom', fontsize=8, color='#0F172A', fontweight='bold')

    # ACCOUNT -> TRANSACTIONS (1:N)
    ax.annotate("", xy=(700, 590), xytext=(630, 590),
                arrowprops=dict(arrowstyle="->", color=line_color, lw=1.5))
    ax.text(665, 600, "1 : N\nconducts", ha='center', va='bottom', fontsize=8, color='#0F172A', fontweight='bold')

    # TRANSACTIONS -> FRAUD_ALERT (1:N)
    ax.annotate("", xy=(840, 320), xytext=(840, 460),
                arrowprops=dict(arrowstyle="->", color=line_color, lw=1.5))
    ax.text(855, 390, "1 : N\ntriggers", ha='left', va='center', fontsize=8, color='#0F172A', fontweight='bold')

    # FRAUD_ALERT -> INVESTIGATION (1:1)
    ax.annotate("", xy=(630, 210), xytext=(700, 210),
                arrowprops=dict(arrowstyle="->", color=line_color, lw=1.5))
    ax.text(665, 220, "1 : 1\nescalates", ha='center', va='bottom', fontsize=8, color='#0F172A', fontweight='bold')

    # INVESTIGATOR -> INVESTIGATION (1:N)
    ax.annotate("", xy=(370, 210), xytext=(300, 210),
                arrowprops=dict(arrowstyle="->", color=line_color, lw=1.5))
    ax.text(335, 220, "1 : N\nassigned", ha='center', va='bottom', fontsize=8, color='#0F172A', fontweight='bold')

    # Title & Subtitle banner
    ax.text(600, 730, "FraudLens — Entity-Relationship (ER) Architecture", 
            ha='center', va='top', fontsize=16, fontweight='bold', color='#0F172A')
    ax.text(600, 708, "Relational mapping across Customer, Account, Transactions, Alerts, Investigators, and Investigations", 
            ha='center', va='top', fontsize=10, color='#64748B')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "erd_diagram.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Generated: {out_path}")

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(11, 4.5), dpi=300)
    ax.set_xlim(0, 1100)
    ax.set_ylim(0, 450)
    ax.axis('off')
    
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # Step cards
    steps = [
        (40, 140, 160, 180, "1. Client Layer", "Channels\n• UPI\n• Net-Banking\n• Mobile App\n• ATM / POS", "#0284C7", "#F0F9FF"),
        (250, 140, 170, 180, "2. Core Ledger", "Transactions\n• Account Debits\n• Transfers\n• Balance Enforce\n• Check Constraints", "#2563EB", "#EFF6FF"),
        (470, 140, 180, 180, "3. Surveillance", "Rule Heuristics\n• Amount > ₹50,000\n• Rapid Velocity\n• Nocturnal Wire\n• Structuring Check", "#D97706", "#FFFBEB"),
        (700, 140, 170, 180, "4. Triage & Alert", "Risk Queue\n• Alert Generation\n• Severity Scoring\n• Automated Triage\n• Pending Signals", "#DC2626", "#FEF2F2"),
        (910, 140, 160, 180, "5. Forensic Case", "Investigation\n• OPEN -> REVIEW\n• Assigned Lead\n• Verdict & Closure\n• Audit Event Log", "#059669", "#ECFDF5"),
    ]

    for x, y, w, h, title, body, border_c, bg_c in steps:
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=8",
                                     linewidth=1.5, edgecolor=border_c, facecolor=bg_c)
        ax.add_patch(rect)
        # Title pill
        pill = patches.FancyBboxPatch((x, y + h - 32), w, 32, boxstyle="round,pad=0,rounding_size=8",
                                     linewidth=1.5, edgecolor=border_c, facecolor=border_c)
        ax.add_patch(pill)
        ax.text(x + w/2, y + h - 16, title, ha='center', va='center', fontsize=10, fontweight='bold', color='#FFFFFF')
        ax.text(x + 14, y + h - 50, body, ha='left', va='top', fontsize=8.5, color='#1E293B', linespacing=1.6)

    # Connection Arrows
    arrows = [(200, 230, 250, 230), (420, 230, 470, 230), (650, 230, 700, 230), (870, 230, 910, 230)]
    for x1, y1, x2, y2 in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color='#475569', lw=2))

    ax.text(550, 420, "FraudLens End-to-End Transaction & Forensic Workflow", 
            ha='center', va='top', fontsize=14, fontweight='bold', color='#0F172A')
    ax.text(550, 395, "From Multi-Channel Ingestion to Automated Anomaly Flagging and Audit Logging", 
            ha='center', va='top', fontsize=9.5, color='#64748B')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "architecture_flow.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Generated: {out_path}")

def generate_lifecycle_diagram():
    fig, ax = plt.subplots(figsize=(10, 3.2), dpi=300)
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 300)
    ax.axis('off')
    
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    nodes = [
        (60, 90, 160, 100, "TRANSACTION\nENTERED", "#0284C7", "Amount & Channel"),
        (290, 90, 180, 100, "ALERT TRIGGERED\n(PENDING)", "#D97706", "Threshold > 50,000"),
        (540, 90, 180, 100, "INVESTIGATION\n(UNDER REVIEW)", "#4F46E5", "Officer Assigned"),
        (790, 90, 160, 100, "CASE CLOSED\n(FINAL VERDICT)", "#059669", "Fraud / False Pos"),
    ]

    for x, y, w, h, label, color, sub in nodes:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=10",
                                    linewidth=1.8, edgecolor=color, facecolor='#F8FAFC')
        ax.add_patch(box)
        ax.text(x + w/2, y + h/2 + 10, label, ha='center', va='center', fontsize=9.5, fontweight='bold', color=color)
        ax.text(x + w/2, y + 22, sub, ha='center', va='center', fontsize=8, color='#64748B')

    # Arrows
    arrs = [(220, 140, 290, 140), (470, 140, 540, 140), (720, 140, 790, 140)]
    for x1, y1, x2, y2 in arrs:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6", color='#334155', lw=2.2))

    ax.text(500, 270, "Investigation Case Lifecycle Progression", 
            ha='center', va='top', fontsize=13, fontweight='bold', color='#0F172A')

    plt.tight_layout()
    out_path = os.path.join(ASSETS_DIR, "workflow_lifecycle.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[OK] Generated: {out_path}")

if __name__ == "__main__":
    generate_er_diagram()
    generate_architecture_diagram()
    generate_lifecycle_diagram()
    print("[SUCCESS] All architectural figures generated successfully.")
