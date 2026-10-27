"""
FraudLens: Master Presentation PDF Generator
Builds two polished, submission-ready PDFs in 16:9 widescreen presentation format:
1. FraudLens_Review_1_Updated.pdf (15 slides matching reference visual identity with genuine Oracle screenshots)
2. FraudLens_Review_1_and_Review_2_Combined.pdf (29 slides comprehensive combined master report)
"""

import os
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib import colors

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "docs", "assets")

PDF_R1_UPDATED = os.path.join(BASE_DIR, "FraudLens_Review_1_Updated.pdf")
PDF_COMBINED = os.path.join(BASE_DIR, "FraudLens_Review_1_and_Review_2_Combined.pdf")
PDF_R2_PRESENTATION = os.path.join(BASE_DIR, "FraudLens_Review_2_Presentation.pdf")

# Dimensions for 16:9 widescreen presentation slides
PAGE_W = 960.0
PAGE_H = 540.0

# Color Palette Constants (Sleek Obsidian Black & Maroon Theme)
DARK_BG = colors.HexColor("#0B090A")         # Deep Obsidian Black
DARK_CARD = colors.HexColor("#171214")       # Deep Charcoal-Maroon Card Surface
LIGHT_BG = colors.HexColor("#F8F7F8")        # Crisp Neutral Ivory / Off-White
WHITE = colors.HexColor("#FFFFFF")
SLATE_900 = colors.HexColor("#100C0E")       # Pitch Black Primary text
SLATE_700 = colors.HexColor("#2B2426")       # Deep Charcoal Body text
SLATE_500 = colors.HexColor("#6E6266")       # Subtitles / Muted text
SLATE_300 = colors.HexColor("#D8D0D3")       # Border lines
SLATE_200 = colors.HexColor("#E5DFE2")       # Light card borders
AMBER = colors.HexColor("#9F1239")           # Vibrant Crimson Maroon Accent
TEAL = colors.HexColor("#881337")            # Primary Deep Maroon Accent
BLUE = colors.HexColor("#701A28")            # Deep Wine Maroon Accent
NAVY_HEADER = colors.HexColor("#540E1F")     # Velvet Burgundy Table Header
CODE_BG = colors.HexColor("#0A0809")         # Deep Obsidian Code Box
CODE_BORDER = colors.HexColor("#26171C")     # Code Border

def setup_styles():
    styles = getSampleStyleSheet()
    
    # Slide Headers
    styles.add(ParagraphStyle('SlideCategory', fontName='Helvetica-Bold', fontSize=9, leading=11, textColor=TEAL, textTransform='uppercase'))
    styles.add(ParagraphStyle('SlideHeading', fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=SLATE_900))
    styles.add(ParagraphStyle('SlideSubhead', fontName='Helvetica', fontSize=10, leading=13, textColor=SLATE_500))
    
    # Dark Slide Styles
    styles.add(ParagraphStyle('DarkTitleCat', fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.HexColor("#FB7185"), textTransform='uppercase'))
    styles.add(ParagraphStyle('DarkMainTitle', fontName='Helvetica-Bold', fontSize=32, leading=38, textColor=WHITE))
    styles.add(ParagraphStyle('DarkSubtitle', fontName='Helvetica-Bold', fontSize=15, leading=19, textColor=colors.HexColor("#F5EBEB")))
    styles.add(ParagraphStyle('DarkDesc', fontName='Helvetica', fontSize=10.5, leading=15, textColor=colors.HexColor("#D4C7CB")))
    styles.add(ParagraphStyle('DarkTeam', fontName='Helvetica-Bold', fontSize=10, leading=14, textColor=WHITE))
    styles.add(ParagraphStyle('DarkMetaLabel', fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=colors.HexColor("#FB7185")))
    styles.add(ParagraphStyle('DarkMetaVal', fontName='Helvetica', fontSize=8.5, leading=11, textColor=colors.HexColor("#A89DA1")))
    
    # Card Styles
    styles.add(ParagraphStyle('CardTagAmber', fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=AMBER, textTransform='uppercase'))
    styles.add(ParagraphStyle('CardTagTeal', fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=TEAL, textTransform='uppercase'))
    styles.add(ParagraphStyle('CardTagNavy', fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=NAVY_HEADER, textTransform='uppercase'))
    styles.add(ParagraphStyle('CardTitle', fontName='Helvetica-Bold', fontSize=12, leading=15, textColor=SLATE_900))
    styles.add(ParagraphStyle('CardBody', fontName='Helvetica', fontSize=8.5, leading=12, textColor=SLATE_700))
    styles.add(ParagraphStyle('CardBodySm', fontName='Helvetica', fontSize=7.8, leading=10.5, textColor=SLATE_700))
    
    # Table & Code Styles
    styles.add(ParagraphStyle('THeader', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=WHITE))
    styles.add(ParagraphStyle('TCell', fontName='Helvetica', fontSize=7.5, leading=10, textColor=SLATE_900))
    styles.add(ParagraphStyle('TCellBold', fontName='Helvetica-Bold', fontSize=7.5, leading=10, textColor=SLATE_900))
    styles.add(ParagraphStyle('TCellMono', fontName='Courier', fontSize=7, leading=9, textColor=SLATE_900))
    styles.add(ParagraphStyle('CodeLine', fontName='Courier', fontSize=6.5, leading=8.5, textColor=colors.HexColor("#F5EBEB")))
    styles.add(ParagraphStyle('FigCaption', fontName='Helvetica-Oblique', fontSize=8, leading=10, textColor=SLATE_500, alignment=1))
    
    return styles

STYLES = setup_styles()

def draw_para(c, text, style, x, top_y, max_w, max_h=300):
    """Wraps and draws a paragraph with top-left anchor at (x, top_y)."""
    p = Paragraph(text, style)
    w, h = p.wrap(max_w, max_h)
    p.drawOn(c, x, top_y - h)
    return w, h

def draw_header(c, category, heading, subhead):
    """Draws top category breadcrumb, main heading and subhead."""
    draw_para(c, category, STYLES['SlideCategory'], 50, 510, 860, 20)
    draw_para(c, heading, STYLES['SlideHeading'], 50, 492, 860, 32)
    draw_para(c, subhead, STYLES['SlideSubhead'], 50, 460, 860, 20)

def draw_footer(c, slide_num_str):
    """Draws consistent footer line, course title and slide number."""
    c.saveState()
    c.setStrokeColor(SLATE_200)
    c.setLineWidth(0.8)
    c.line(50, 32, 910, 32)
    
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(SLATE_500)
    c.drawString(50, 20, "FRAUDLENS  /  FINANCIAL TRANSACTION & FRAUD INVESTIGATION MANAGEMENT SYSTEM")
    
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(AMBER)
    c.drawRightString(910, 20, slide_num_str)
    c.restoreState()

def draw_card(c, x, y, w, h, accent_color=None, bg_color=WHITE):
    """Draws a clean rounded card with optional colored left accent bar."""
    c.saveState()
    c.setFillColor(bg_color)
    c.setStrokeColor(SLATE_200)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 6, stroke=1, fill=1)
    
    if accent_color:
        c.setFillColor(accent_color)
        c.roundRect(x, y, 4, h, 2, stroke=0, fill=1)
    c.restoreState()

def draw_code_box(c, x, y, w, h, title, code_lines):
    """Draws a dark-themed code snippet box with header tab."""
    c.saveState()
    c.setFillColor(CODE_BG)
    c.setStrokeColor(CODE_BORDER)
    c.setLineWidth(1)
    c.roundRect(x, y, w, h, 6, stroke=1, fill=1)
    
    # Title bar
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor("#FB7185"))
    c.drawString(x + 12, y + h - 14, title)
    c.setStrokeColor(colors.HexColor("#26171C"))
    c.setLineWidth(0.5)
    c.line(x + 10, y + h - 18, x + w - 10, y + h - 18)
    
    # Code content
    curr_top = y + h - 22
    for line in code_lines:
        w_used, h_used = draw_para(c, line.replace(" ", "&nbsp;"), STYLES['CodeLine'], x + 12, curr_top, w - 24, 15)
        curr_top -= 9.5
    c.restoreState()

# =============================================================================
# SLIDE BUILDERS (REVIEW 1)
# =============================================================================

def build_slide_1(c):
    """Slide 1: Dark Executive Title Slide"""
    c.saveState()
    c.setFillColor(DARK_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    # Right decorative area
    c.setFillColor(DARK_CARD)
    c.roundRect(690, 40, 220, 460, 10, stroke=0, fill=1)
    c.setStrokeColor(colors.HexColor("#26171C"))
    c.setLineWidth(0.6)
    for gx in range(710, 900, 35):
        c.line(gx, 50, gx, 490)
    for gy in range(60, 490, 35):
        c.line(700, gy, 900, gy)
        
    # Geometric circles
    c.setFillColor(AMBER)
    c.circle(760, 380, 34, stroke=0, fill=1)
    c.setFillColor(colors.HexColor("#F5EBEB"))
    c.circle(830, 320, 22, stroke=0, fill=1)
    c.setFillColor(TEAL)
    c.circle(790, 220, 46, stroke=0, fill=1)
    
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(colors.HexColor("#A89DA1"))
    c.drawString(715, 65, "COMPUTER SCIENCE & ENGINEERING")
    
    # Left Content
    draw_para(c, "DATABASE MANAGEMENT SYSTEMS  /  CASE STUDY • REVIEW 1", STYLES['DarkTitleCat'], 60, 475, 600, 20)
    draw_para(c, "FraudLens", STYLES['DarkMainTitle'], 60, 440, 600, 45)
    draw_para(c, "Financial Transaction & Fraud<br/>Investigation Management System", STYLES['DarkSubtitle'], 60, 380, 600, 45)
    
    p_desc = "Relational domain modelling, 3NF architecture, Oracle SQL DDL with named constraints and sequences, controlled DML, and analytical queries."
    draw_para(c, p_desc, STYLES['DarkDesc'], 60, 310, 580, 40)
    
    p_team = "D JOSHUA DANIEL &nbsp; <b>24BCE0436</b> &nbsp;&nbsp;|&nbsp;&nbsp; M SARYU &nbsp; <b>24BCE2524</b>"
    draw_para(c, p_team, STYLES['DarkTeam'], 60, 230, 600, 20)
    
    p_faculty = "Faculty: <b>Kanagaraj K</b>"
    draw_para(c, p_faculty, STYLES['DarkTeam'], 60, 195, 600, 20)
    
    draw_para(c, "Review 1  /  Relational Schema Design & SQL Foundations", STYLES['DarkMetaLabel'], 60, 155, 600, 15)
    draw_para(c, "BCSE304L Database Management Systems • SCOPE, VIT Vellore", STYLES['DarkMetaVal'], 60, 135, 600, 15)
    
    c.restoreState()

def build_slide_2(c):
    """Slide 2: Executive Overview"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "01 / EXECUTIVE OVERVIEW", "Fraud data scattered across silos", "Banks move tens of thousands of transactions a minute: RTGS, NEFT, IMPS, ATM, POS, UPI.")
    
    cw = 265
    ch = 190
    y_top = 225
    
    # Card 1: Context
    draw_card(c, 50, y_top, cw, ch, accent_color=AMBER)
    draw_para(c, "THE CONTEXT", STYLES['CardTagAmber'], 68, y_top + ch - 16, cw-30, 15)
    draw_para(c, "Fragmented storage", STYLES['CardTitle'], 68, y_top + ch - 36, cw-30, 20)
    draw_para(c, "Customers, ledgers, transactions and case notes sit in separate spreadsheets with no foreign-key links.", STYLES['CardBody'], 68, y_top + ch - 66, cw-30, 80)
    
    # Card 2: Risk
    draw_card(c, 345, y_top, cw, ch, accent_color=TEAL)
    draw_para(c, "THE RISK", STYLES['CardTagTeal'], 363, y_top + ch - 16, cw-30, 15)
    draw_para(c, "Drift + weak validation", STYLES['CardTitle'], 363, y_top + ch - 36, cw-30, 20)
    draw_para(c, "Duplicated demographics cause update anomalies; negative balances and orphan tickets slip through.", STYLES['CardBody'], 363, y_top + ch - 66, cw-30, 80)
    
    # Card 3: Response
    draw_card(c, 640, y_top, cw, ch, accent_color=NAVY_HEADER)
    draw_para(c, "OUR RESPONSE", STYLES['CardTagNavy'], 658, y_top + ch - 16, cw-30, 15)
    draw_para(c, "One 3NF Oracle schema", STYLES['CardTitle'], 658, y_top + ch - 36, cw-30, 20)
    draw_para(c, "Six core entities with PK/FK, cascading deletes and engine-level CHECK constraints enforce valid ranges and states.", STYLES['CardBody'], 658, y_top + ch - 66, cw-30, 80)
    
    # Bottom Research Question Card
    rw = 855
    rh = 120
    ry = 75
    draw_card(c, 50, ry, rw, rh, accent_color=AMBER)
    draw_para(c, "RESEARCH QUESTION", STYLES['CardTagAmber'], 70, ry + rh - 16, rw-40, 15)
    q_title = "How can a bank unify customers, accounts, transactions, alerts and investigations so suspicious activity is traceable and data stays correct?"
    draw_para(c, q_title, STYLES['CardTitle'], 70, ry + rh - 36, rw-40, 30)
    scope_text = "<b>Scope:</b> Review 1 covers relational requirements, ER model, 3NF mapping, Oracle DDL, controlled DML, and baseline analytical queries. Review 2 integrates procedural surveillance, views, stored procedures, functions, triggers, and full audit logs."
    draw_para(c, scope_text, STYLES['CardBody'], 70, ry + rh - 68, rw-40, 45)
    
    draw_footer(c, "02")
    c.restoreState()

def build_slide_3(c):
    """Slide 3: Problem Definition"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "02 / PROBLEM DEFINITION", "Three failures, three fixes", "Operational deficiencies mapped to the FraudLens relational solution.")
    
    headers = [Paragraph("Operational deficiency", STYLES['THeader']), Paragraph("Impact on banking operations", STYLES['THeader']), Paragraph("FraudLens relational solution", STYLES['THeader'])]
    rows = [
        [
            Paragraph("<b>Fragmented storage</b>", STYLES['TCell']),
            Paragraph("Transactions, alerts and case notes live in disparate systems without foreign-key links.", STYLES['TCell']),
            Paragraph("One centralised Oracle schema with strict primary/foreign key relationships.", STYLES['TCell'])
        ],
        [
            Paragraph("<b>Redundancy & drift</b>", STYLES['TCell']),
            Paragraph("Customer demographics duplicated across spreadsheets cause update anomalies.", STYLES['TCell']),
            Paragraph("Normalised to 3NF; each customer attribute is stored exactly once.", STYLES['TCell'])
        ],
        [
            Paragraph("<b>Weak validation</b>", STYLES['TCell']),
            Paragraph("Spreadsheets allow negative balances, zero amounts and orphan investigation tickets.", STYLES['TCell']),
            Paragraph("Engine-level CHECK constraints enforce valid ranges, balances and statuses.", STYLES['TCell'])
        ]
    ]
    
    t = Table([headers] + rows, colWidths=[200, 325, 335])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_HEADER),
        ('BOTTOMPADDING', (0,0), (-1,-1), 16),
        ('TOPPADDING', (0,0), (-1,-1), 16),
        ('LEFTPADDING', (0,0), (-1,-1), 14),
        ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ('BACKGROUND', (0,1), (-1,1), WHITE),
        ('BACKGROUND', (0,2), (-1,2), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0,3), (-1,3), WHITE),
        ('GRID', (0,0), (-1,-1), 0.5, SLATE_200),
    ]))
    
    w, h = t.wrap(860, 240)
    t.drawOn(c, 50, 420 - h)
    
    # Bottom Note Box
    draw_card(c, 50, 75, 860, 48, bg_color=colors.HexColor("#ECFDF5"))
    c.setStrokeColor(TEAL)
    c.setLineWidth(1)
    c.roundRect(50, 75, 860, 48, 6, stroke=1, fill=0)
    
    note_txt = "<font color='#065F46'><b>Engine Enforcement Principle:</b> Every validation rule is enforced inside the Oracle database engine via constraints and triggers, not left to application code.</font>"
    draw_para(c, note_txt, STYLES['CardBody'], 68, 75 + 32, 830, 25)
    
    draw_footer(c, "03")
    c.restoreState()

def build_slide_4(c):
    """Slide 4: Objectives & Business Rules"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "03 / OBJECTIVES & BUSINESS RULES", "What the database must enforce", "Functional objectives on the left; enforced rules BR-01 to BR-06 on the right.")
    
    bw = 415
    bh = 340
    by = 70
    
    # Left Card
    draw_card(c, 50, by, bw, bh, accent_color=TEAL)
    draw_para(c, "FUNCTIONAL OBJECTIVES", STYLES['CardTagTeal'], 70, by + bh - 16, bw-30, 15)
    
    objs = [
        "<b>Account hierarchy:</b> One customer may hold multiple accounts across Savings, Current, Salary, and NRI types.",
        "<b>Transaction journal:</b> Captures type (DEPOSIT, WITHDRAWAL, TRANSFER), timestamp, channel, counterparty, and status.",
        "<b>Rule-based alerts:</b> Dynamic severity scoring across LOW, MEDIUM, HIGH, and CRITICAL brackets.",
        "<b>Case lifecycle:</b> Structured progression through OPEN, UNDER REVIEW, and CLOSED with assigned investigators.",
        "<b>Analytical querying:</b> Comprehensive baseline reporting using character formatting, numeric filters, group metrics, and joins."
    ]
    curr_top = by + bh - 40
    for obj in objs:
        w_used, h_used = draw_para(c, f"• {obj}", STYLES['CardBody'], 70, curr_top, bw-40, 50)
        curr_top -= 52
        
    # Right Card
    draw_card(c, 495, by, bw, bh, accent_color=AMBER)
    draw_para(c, "ENFORCED BUSINESS RULES", STYLES['CardTagAmber'], 515, by + bh - 16, bw-30, 15)
    
    rules = [
        ("BR-01", "Each account belongs to exactly one customer (ON DELETE CASCADE)."),
        ("BR-02", "Account balance must stay strictly non-negative (CHECK balance >= 0)."),
        ("BR-03", "Transaction amount must be strictly greater than zero (CHECK amount > 0)."),
        ("BR-04", "A fraud alert references an existing transaction; cascade deletes on purge."),
        ("BR-05", "An investigation links one alert to one active investigator."),
        ("BR-06", "Transactions above INR 50,000 are flagged for compliance review.")
    ]
    curr_top = by + bh - 40
    for code, text in rules:
        draw_para(c, f"<b><font color='#D97706'>{code}</font></b>", STYLES['CardBody'], 515, curr_top, 55, 20)
        draw_para(c, text, STYLES['CardBody'], 575, curr_top, bw - 95, 35)
        curr_top -= 43
        
    draw_footer(c, "04")
    c.restoreState()

def build_slide_5(c):
    """Slide 5: Data Model (ERD)"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "04 / DATA MODEL", "ER model of the implemented schema", "Six entities designed in Oracle SQL Developer Data Modeler; P = primary, F = foreign, U = unique key.")
    
    erd_path = os.path.join(ASSETS_DIR, "erd_diagram.png")
    if os.path.exists(erd_path):
        draw_card(c, 50, 75, 860, 350)
        c.drawImage(erd_path, 60, 95, width=840, height=320, preserveAspectRatio=True, anchor='c')
    
    draw_para(c, "Figure 1: FraudLens relational diagram (Oracle SQL Developer Data Modeler / Oracle Database 23ai)", STYLES['FigCaption'], 50, 72, 860, 15)
    
    draw_footer(c, "05")
    c.restoreState()

def build_slide_6(c):
    """Slide 6: Relational Schema & Normalization"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "05 / RELATIONAL SCHEMA", "Keys and constraints encode the rules", "Single-column surrogate keys; every table verified against 1NF, 2NF and 3NF.")
    
    headers = [Paragraph("Table", STYLES['THeader']), Paragraph("Primary key", STYLES['THeader']), Paragraph("Foreign key(s)", STYLES['THeader']), Paragraph("Key constraints enforced", STYLES['THeader'])]
    rows = [
        [Paragraph("CUSTOMER", STYLES['TCellBold']), Paragraph("customer_id", STYLES['TCellMono']), Paragraph("-", STYLES['TCell']), Paragraph("email, phone UNIQUE NOT NULL; kyc_status CHECK; risk_score 0-100", STYLES['TCell'])],
        [Paragraph("ACCOUNT", STYLES['TCellBold']), Paragraph("account_id", STYLES['TCellMono']), Paragraph("customer_id → CUSTOMER", STYLES['TCellMono']), Paragraph("account_number UNIQUE; balance >= 0; type and status CHECK", STYLES['TCell'])],
        [Paragraph("TRANSACTIONS", STYLES['TCellBold']), Paragraph("transaction_id", STYLES['TCellMono']), Paragraph("account_id → ACCOUNT", STYLES['TCellMono']), Paragraph("amount > 0; transaction_type, channel, status CHECK", STYLES['TCell'])],
        [Paragraph("FRAUD_ALERT", STYLES['TCellBold']), Paragraph("alert_id", STYLES['TCellMono']), Paragraph("transaction_id → TRANSACTIONS", STYLES['TCellMono']), Paragraph("severity CHECK (LOW to CRITICAL); status DEFAULT 'PENDING'", STYLES['TCell'])],
        [Paragraph("INVESTIGATOR", STYLES['TCellBold']), Paragraph("investigator_id", STYLES['TCellMono']), Paragraph("-", STYLES['TCell']), Paragraph("email UNIQUE NOT NULL; experience_years >= 0; active_status CHECK", STYLES['TCell'])],
        [Paragraph("INVESTIGATION", STYLES['TCellBold']), Paragraph("case_id", STYLES['TCellMono']), Paragraph("alert_id, investigator_id", STYLES['TCellMono']), Paragraph("status CHECK; outcome CHECK; end_date >= start_date", STYLES['TCell'])],
    ]
    t = Table([headers] + rows, colWidths=[120, 110, 190, 440])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_HEADER),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, SLATE_200),
    ]))
    w, h = t.wrap(860, 175)
    t.drawOn(c, 50, 415 - h)
    
    # 3 Normal Form Cards
    cw = 265
    ch = 145
    cy = 75
    
    draw_card(c, 50, cy, cw, ch, accent_color=AMBER)
    draw_para(c, "1NF", STYLES['CardTagAmber'], 68, cy + ch - 16, cw-30, 15)
    draw_para(c, "Atomic scalar values", STYLES['CardTitle'], 68, cy + ch - 36, cw-30, 18)
    draw_para(c, "All table attributes store atomic scalar values. No repeating groups or multi-valued phone lists; first and last names separated.", STYLES['CardBody'], 68, cy + ch - 64, cw-30, 70)
    
    draw_card(c, 345, cy, cw, ch, accent_color=TEAL)
    draw_para(c, "2NF", STYLES['CardTagTeal'], 363, cy + ch - 16, cw-30, 15)
    draw_para(c, "No partial dependencies", STYLES['CardTitle'], 363, cy + ch - 36, cw-30, 18)
    draw_para(c, "Every relation relies on single-column surrogate primary keys. No non-prime attribute depends on a proper subset of any candidate key.", STYLES['CardBody'], 363, cy + ch - 64, cw-30, 70)
    
    draw_card(c, 640, cy, cw, ch, accent_color=NAVY_HEADER)
    draw_para(c, "3NF", STYLES['CardTagNavy'], 658, cy + ch - 16, cw-30, 15)
    draw_para(c, "No transitive dependencies", STYLES['CardTitle'], 658, cy + ch - 36, cw-30, 18)
    draw_para(c, "Non-key columns depend exclusively on primary keys. Investigator department and customer KYC status live only in home entities.", STYLES['CardBody'], 658, cy + ch - 64, cw-30, 70)
    
    draw_footer(c, "06")
    c.restoreState()

def build_slide_7(c):
    """Slide 7: Schema Implementation (DDL & Sequences)"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "06 / SCHEMA IMPLEMENTATION", "Oracle DDL with named constraints", "From sql/01_schema.sql; named constraints give deterministic error diagnostics.")
    
    account_ddl = [
        "CREATE TABLE ACCOUNT (",
        "  account_id   NUMBER(10) CONSTRAINT pk_account PRIMARY KEY,",
        "  customer_id  NUMBER(10) NOT NULL",
        "               CONSTRAINT fk_acc_customer",
        "               REFERENCES CUSTOMER(customer_id)",
        "               ON DELETE CASCADE,",
        "  account_number VARCHAR2(20)",
        "               CONSTRAINT uq_acc_number UNIQUE NOT NULL,",
        "  account_type VARCHAR2(20) DEFAULT 'SAVINGS'",
        "               CONSTRAINT chk_acc_type CHECK (account_type",
        "               IN ('SAVINGS','CURRENT','SALARY','NRI')),",
        "  balance      NUMBER(15,2) DEFAULT 0.00",
        "               CONSTRAINT chk_acc_balance CHECK (balance >= 0),",
        "  status       VARCHAR2(15) DEFAULT 'ACTIVE'",
        "               CONSTRAINT chk_acc_status CHECK (status IN",
        "               ('ACTIVE','FROZEN','DORMANT','CLOSED'))",
        ");"
    ]
    draw_code_box(c, 50, 75, 415, 345, "CREATE: ACCOUNT (DDL Snippet)", account_ddl)
    
    tx_ddl = [
        "CREATE TABLE TRANSACTIONS (",
        "  transaction_id NUMBER(12) CONSTRAINT pk_transactions PRIMARY KEY,",
        "  account_id     NUMBER(10) NOT NULL",
        "                 CONSTRAINT fk_tx_account",
        "                 REFERENCES ACCOUNT(account_id) ON DELETE CASCADE,",
        "  amount         NUMBER(15,2) NOT NULL",
        "                 CONSTRAINT chk_tx_amount CHECK (amount > 0),",
        "  channel        VARCHAR2(20) NOT NULL",
        "                 CONSTRAINT chk_tx_channel CHECK (channel IN",
        "                 ('ATM','POS','NET_BANKING','MOBILE_APP','UPI'))",
        ");"
    ]
    draw_code_box(c, 495, 230, 415, 190, "CREATE: TRANSACTIONS (Abbreviated)", tx_ddl)
    
    draw_card(c, 495, 75, 415, 140, accent_color=BLUE)
    draw_para(c, "SEQUENCES", STYLES['CardTagNavy'], 515, 75 + 140 - 16, 375, 15)
    draw_para(c, "Six PK sequence generators", STYLES['CardTitle'], 515, 75 + 140 - 36, 375, 20)
    seq_desc = "START WITH sits above sample IDs (e.g., customer sequence starts at 1011 after sample 1001-1010; transaction sequence at 50019 after sample 50001-50018) to avoid key collision during execution."
    draw_para(c, seq_desc, STYLES['CardBody'], 515, 75 + 140 - 64, 375, 60)
    
    draw_footer(c, "07")
    c.restoreState()

def build_slide_8(c):
    """Slide 8: DML & ALTER"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "07 / DML & ALTER", "Safe schema changes, reversible DML", "From sql/02_ddl_dml_demos.sql; structural changes on a staging table, updates under a savepoint.")
    
    alter_lines = [
        "-- 1. Schema Modification on Staging Table",
        "ALTER TABLE FRAUD_RULE_CONFIG",
        "  ADD (rule_description VARCHAR2(250));",
        "",
        "ALTER TABLE FRAUD_RULE_CONFIG",
        "  MODIFY (rule_code VARCHAR2(60));",
        "",
        "ALTER TABLE FRAUD_RULE_CONFIG",
        "  DROP COLUMN rule_description;",
        "",
        "DROP TABLE FRAUD_RULE_CONFIG PURGE;"
    ]
    draw_code_box(c, 50, 75, 415, 345, "ALTER / DROP: STAGING TABLE", alter_lines)
    
    dml_lines = [
        "-- 2. Transaction Control with Savepoint",
        "SAVEPOINT dml_demo_start;",
        "",
        "UPDATE CUSTOMER",
        "  SET kyc_status = 'VERIFIED', risk_score = 5",
        "  WHERE customer_id = 9999;",
        "",
        "DELETE FROM CUSTOMER",
        "  WHERE customer_id IN (9998, 9999);",
        "",
        "ROLLBACK TO dml_demo_start;"
    ]
    draw_code_box(c, 495, 230, 415, 190, "DML UNDER SAVEPOINT", dml_lines)
    
    draw_card(c, 495, 75, 415, 140, accent_color=AMBER)
    draw_para(c, "WHY A SAVEPOINT?", STYLES['CardTagAmber'], 515, 75 + 140 - 16, 375, 15)
    draw_para(c, "Baseline stays pristine", STYLES['CardTitle'], 515, 75 + 140 - 36, 375, 20)
    sp_desc = "The rollback restores the 56-record baseline dataset immediately after the demonstration, ensuring that subsequent analytical queries, joins, and test cases run against known, predictable data."
    draw_para(c, sp_desc, STYLES['CardBody'], 515, 75 + 140 - 64, 375, 60)
    
    draw_footer(c, "08")
    c.restoreState()

def build_screenshot_slide(c, cat_num, cat_title, main_title, subhead, ss_filename, fig_num, fig_title, slide_num, full_category=None):
    """Generic slide builder for query screenshot slides (Slides 9, 10, 11, 12, etc.)."""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    cat_header = full_category if full_category else f"08 / QUERIES / {cat_num}"
    draw_header(c, cat_header, main_title, subhead)
    
    ss_path = os.path.join(ASSETS_DIR, ss_filename)
    if os.path.exists(ss_path):
        draw_card(c, 50, 75, 860, 350)
        c.drawImage(ss_path, 60, 95, width=840, height=320, preserveAspectRatio=True, anchor='c')
        
    draw_para(c, f"Figure {fig_num}: {fig_title} (Executed on Oracle 23ai Free / FREEPDB1 via SQL*Plus)", STYLES['FigCaption'], 50, 72, 860, 15)
    
    draw_footer(c, slide_num)
    c.restoreState()

def build_slide_9(c):
    build_screenshot_slide(c, "8.1", "QUERIES", "Single-row functions", "UPPER, LOWER, LENGTH and SUBSTR standardise customer profiles.", "ss_oracle_r1_singlerow.png", "2", "Single-row character functions with query results", "09", full_category="08 / QUERIES / 8.1")

def build_slide_10(c):
    build_screenshot_slide(c, "8.2", "QUERIES", "IN, BETWEEN and ORDER BY", "High-value digital-channel transactions between INR 50,000 and 300,000.", "ss_oracle_r1_in_between.png", "3", "Range filtering with IN, BETWEEN and descending sort", "10", full_category="08 / QUERIES / 8.2")

def build_slide_11(c):
    build_screenshot_slide(c, "8.3", "QUERIES", "GROUP BY and HAVING", "Transaction count, turnover and average ticket per channel, channels with 3+ transactions.", "ss_oracle_r1_groupby.png", "4", "Channel aggregation metrics", "11", full_category="08 / QUERIES / 8.3")

def build_slide_12(c):
    build_screenshot_slide(c, "8.4", "QUERIES", "Four-table analytical join", "Customer, account, transaction and alert linked to surface high-risk exposure.", "ss_oracle_r1_join.png", "5", "Four-table join tracking high-risk alerts to accounts", "12", full_category="08 / QUERIES / 8.4")

def build_slide_13(c):
    """Slide 13: Constraint Defense & Testing"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "09 / TESTING", "Constraints reject bad data", "Negative tests trigger engine-level exceptions; positive tests are accepted.")
    
    ss_path = os.path.join(ASSETS_DIR, "ss_oracle_r1_constraint.png")
    if os.path.exists(ss_path):
        draw_card(c, 50, 245, 860, 180)
        c.drawImage(ss_path, 60, 255, width=840, height=160, preserveAspectRatio=True, anchor='c')
    
    headers = [Paragraph("Type", STYLES['THeader']), Paragraph("Constraint", STYLES['THeader']), Paragraph("Input tested", STYLES['THeader']), Paragraph("Expected", STYLES['THeader']), Paragraph("Status", STYLES['THeader'])]
    rows = [
        [Paragraph("<font color='#DC2626'><b>Negative</b></font>", STYLES['TCell']), Paragraph("CHECK (amount > 0)", STYLES['TCellMono']), Paragraph("amount = -500.00", STYLES['TCell']), Paragraph("Rejected, ORA-02290", STYLES['TCell']), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", STYLES['TCell'])],
        [Paragraph("<font color='#DC2626'><b>Negative</b></font>", STYLES['TCell']), Paragraph("UNIQUE (email)", STYLES['TCellMono']), Paragraph("existing aarav.sharma@finmail.in", STYLES['TCell']), Paragraph("Rejected, ORA-00001", STYLES['TCell']), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", STYLES['TCell'])],
        [Paragraph("<font color='#DC2626'><b>Negative</b></font>", STYLES['TCell']), Paragraph("FOREIGN KEY (customer_id)", STYLES['TCellMono']), Paragraph("customer_id = 999999", STYLES['TCell']), Paragraph("Rejected, ORA-02291", STYLES['TCell']), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", STYLES['TCell'])],
        [Paragraph("<font color='#16A34A'><b>Positive</b></font>", STYLES['TCell']), Paragraph("CHECK (kyc_status)", STYLES['TCellMono']), Paragraph("kyc_status = 'VERIFIED'", STYLES['TCell']), Paragraph("Accepted and updated", STYLES['TCell']), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", STYLES['TCell'])],
        [Paragraph("<font color='#16A34A'><b>Positive</b></font>", STYLES['TCell']), Paragraph("CHECK (risk_score)", STYLES['TCellMono']), Paragraph("risk_score = 85", STYLES['TCell']), Paragraph("Accepted and stored", STYLES['TCell']), Paragraph("<font color='#16A34A'><b>PASSED</b></font>", STYLES['TCell'])],
    ]
    t = Table([headers] + rows, colWidths=[90, 200, 260, 210, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_HEADER),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, SLATE_200),
    ]))
    w, h = t.wrap(860, 160)
    t.drawOn(c, 50, 235 - h)
    
    draw_footer(c, "13")
    c.restoreState()

def build_slide_14(c):
    """Slide 14: Conclusion & Review 2 Roadmap"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "10 / CONCLUSION & REVIEW 2", "Foundation first, procedures next", "Phase 1 delivers a verified 3NF base; Phase 2 adds procedural surveillance.")
    
    cw = 265
    ch = 120
    cy = 295
    
    draw_card(c, 50, cy, cw, ch, accent_color=AMBER)
    draw_para(c, "01 INTEGRITY", STYLES['CardTagAmber'], 68, cy + ch - 16, cw-30, 15)
    draw_para(c, "Zero orphan records", STYLES['CardTitle'], 68, cy + ch - 36, cw-30, 18)
    draw_para(c, "Cascading FKs ensure no orphan transactions, alerts or cases can exist.", STYLES['CardBody'], 68, cy + ch - 64, cw-30, 50)
    
    draw_card(c, 345, cy, cw, ch, accent_color=TEAL)
    draw_para(c, "02 NO ANOMALIES", STYLES['CardTagTeal'], 363, cy + ch - 16, cw-30, 15)
    draw_para(c, "Strict 3NF structure", STYLES['CardTitle'], 363, cy + ch - 36, cw-30, 18)
    draw_para(c, "Customer and investigator details live in one authoritative relation.", STYLES['CardBody'], 363, cy + ch - 64, cw-30, 50)
    
    draw_card(c, 640, cy, cw, ch, accent_color=NAVY_HEADER)
    draw_para(c, "03 DOMAIN DEFENCE", STYLES['CardTagNavy'], 658, cy + ch - 16, cw-30, 15)
    draw_para(c, "Database-level CHECKs", STYLES['CardTitle'], 658, cy + ch - 36, cw-30, 18)
    draw_para(c, "Named CHECKs block negative balances, zero amounts, and invalid statuses.", STYLES['CardBody'], 658, cy + ch - 64, cw-30, 50)
    
    headers = [Paragraph("Review 2 component", STYLES['THeader']), Paragraph("Planned implementation", STYLES['THeader']), Paragraph("Objective in FraudLens", STYLES['THeader'])]
    rows = [
        [Paragraph("Advanced subqueries", STYLES['TCellBold']), Paragraph("Correlated and multi-row (IN, ANY, ALL)", STYLES['TCell']), Paragraph("Flag accounts far above their own historical average", STYLES['TCell'])],
        [Paragraph("Database views", STYLES['TCellBold']), Paragraph("VW_HIGH_RISK_TRANSACTIONS, VW_INVESTIGATION_SUMMARY", STYLES['TCell']), Paragraph("Dashboards without complex application joins", STYLES['TCell'])],
        [Paragraph("PL/SQL procedures", STYLES['TCellBold']), Paragraph("SP_ASSIGN_INVESTIGATOR and case progression", STYLES['TCell']), Paragraph("Validate constraints before state transitions", STYLES['TCell'])],
        [Paragraph("User-defined functions", STYLES['TCellBold']), Paragraph("FN_GET_TOTAL_TX_AMOUNT, FN_CALCULATE_RISK_TIER", STYLES['TCell']), Paragraph("Dynamic customer risk tiers and account volume scoring", STYLES['TCell'])],
        [Paragraph("Triggers & audit logs", STYLES['TCellBold']), Paragraph("AFTER UPDATE row-level triggers to audit tables", STYLES['TCell']), Paragraph("Non-repudiation and forensic case lifecycle logging", STYLES['TCell'])],
    ]
    t = Table([headers] + rows, colWidths=[200, 320, 340])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_HEADER),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, SLATE_200),
    ]))
    w, h = t.wrap(860, 200)
    t.drawOn(c, 50, 280 - h)
    
    draw_footer(c, "14")
    c.restoreState()

def build_slide_15(c):
    """Slide 15: Concluding Slide"""
    c.saveState()
    c.setFillColor(DARK_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_para(c, "FRAUDLENS • REVIEW 1 COMPLETE", STYLES['DarkTitleCat'], 60, 475, 700, 15)
    draw_para(c, "Model correctly. Enforce in the engine.", STYLES['DarkMainTitle'], 60, 440, 800, 40)
    draw_para(c, "Keys and constraints protect relationships; queries turn clean data into fraud signals.", STYLES['DarkSubtitle'], 60, 385, 800, 25)
    
    # 2 Student Cards
    draw_card(c, 60, 180, 270, 120, bg_color=DARK_CARD)
    c.setStrokeColor(colors.HexColor("#331E24"))
    c.roundRect(60, 180, 270, 120, 6, stroke=1, fill=0)
    draw_para(c, "<b>D Joshua Daniel</b>", STYLES['DarkTeam'], 80, 180 + 120 - 18, 240, 20)
    draw_para(c, "Reg No: 24BCE0436<br/>B.Tech CSE • VIT Vellore", STYLES['DarkMetaVal'], 80, 180 + 120 - 45, 240, 40)
    
    draw_card(c, 360, 180, 270, 120, bg_color=DARK_CARD)
    c.setStrokeColor(colors.HexColor("#331E24"))
    c.roundRect(360, 180, 270, 120, 6, stroke=1, fill=0)
    draw_para(c, "<b>M Saryu</b>", STYLES['DarkTeam'], 380, 180 + 120 - 18, 240, 20)
    draw_para(c, "Reg No: 24BCE2524<br/>B.Tech CSE • VIT Vellore", STYLES['DarkMetaVal'], 380, 180 + 120 - 45, 240, 40)
    
    # Faculty Card
    draw_card(c, 660, 180, 250, 120, bg_color=DARK_CARD)
    c.setStrokeColor(colors.HexColor("#331E24"))
    c.roundRect(660, 180, 250, 120, 6, stroke=1, fill=0)
    draw_para(c, "<b>Kanagaraj K</b>", STYLES['DarkTeam'], 680, 180 + 120 - 18, 220, 20)
    draw_para(c, "Faculty Guide<br/>SCOPE • VIT Vellore", STYLES['DarkMetaVal'], 680, 180 + 120 - 45, 220, 40)
    
    draw_para(c, "<b>Thank you  /  Questions</b>", STYLES['DarkSubtitle'], 60, 115, 400, 25)
    
    c.restoreState()

# =============================================================================
# SLIDE BUILDERS (REVIEW 2 - COMBINED REPORT EXTENSIONS)
# =============================================================================

def build_slide_16(c):
    """Slide 16: Review 2 Transition / Title Slide"""
    c.saveState()
    c.setFillColor(DARK_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_para(c, "DATABASE MANAGEMENT SYSTEMS  /  CASE STUDY • REVIEW 2 EXTENSION", STYLES['DarkTitleCat'], 60, 485, 600, 15)
    draw_para(c, "Review 2: Advanced Implementation", STYLES['DarkMainTitle'], 60, 450, 600, 40)
    draw_para(c, "Procedural Intelligence, Automated Surveillance & Forensic Audit Defense", STYLES['DarkSubtitle'], 60, 395, 600, 25)
    
    p_desc = (
        "Transitioning from static 3NF relational modeling to active procedural database surveillance. "
        "Encompasses nested and correlated subqueries, multi-table surveillance views, PL/SQL stored "
        "procedures with strict state progression, deterministic scoring functions, row-level audit triggers, "
        "and complete exception recovery executed on Oracle 23ai Free."
    )
    draw_para(c, p_desc, STYLES['DarkDesc'], 60, 345, 590, 75)
    
    # Prominent Student & Registration Cards
    cw = 285
    ch = 95
    cy = 150
    
    # Student 1 Card
    draw_card(c, 60, cy, cw, ch, bg_color=DARK_CARD, accent_color=AMBER)
    c.setStrokeColor(colors.HexColor("#331E24"))
    c.roundRect(60, cy, cw, ch, 6, stroke=1, fill=0)
    draw_para(c, "<b>D Joshua Daniel</b>", STYLES['DarkTeam'], 78, cy + ch - 16, cw - 28, 18)
    p_s1 = "Registration No: <font color='#FB7185'><b>24BCE0436</b></font><br/>B.Tech CSE • SCOPE, VIT Vellore"
    draw_para(c, p_s1, STYLES['DarkMetaVal'], 78, cy + ch - 38, cw - 28, 45)
    
    # Student 2 Card
    draw_card(c, 365, cy, cw, ch, bg_color=DARK_CARD, accent_color=TEAL)
    c.setStrokeColor(colors.HexColor("#331E24"))
    c.roundRect(365, cy, cw, ch, 6, stroke=1, fill=0)
    draw_para(c, "<b>M Saryu</b>", STYLES['DarkTeam'], 383, cy + ch - 16, cw - 28, 18)
    p_s2 = "Registration No: <font color='#FB7185'><b>24BCE2524</b></font><br/>B.Tech CSE • SCOPE, VIT Vellore"
    draw_para(c, p_s2, STYLES['DarkMetaVal'], 383, cy + ch - 38, cw - 28, 45)
    
    # Faculty Guide & Course Meta
    draw_para(c, "Faculty Guide: <b>Prof. Kanagaraj K</b> &nbsp;&nbsp;|&nbsp;&nbsp; Course: <b>BCSE304L Database Management Systems</b>", STYLES['DarkMetaLabel'], 60, 115, 600, 18)
    
    # Right Modules Card
    draw_card(c, 675, 75, 235, 425, bg_color=DARK_CARD)
    c.setStrokeColor(colors.HexColor("#331E24"))
    c.roundRect(675, 75, 235, 425, 10, stroke=1, fill=0)
    
    draw_para(c, "REVIEW 2 MODULES", STYLES['DarkTitleCat'], 695, 475, 195, 15)
    
    mod_items = [
        "1. Advanced Subqueries",
        "2. Database Views",
        "3. PL/SQL Procedures",
        "4. Stored Functions",
        "5. Cursors & Batch Logic",
        "6. Audit Triggers",
        "7. Transaction Isolation",
        "8. Full System Workflow",
        "9. 13-Case Test Harness",
        "10. Compliance Matrix"
    ]
    curr_top = 450
    for mi in mod_items:
        draw_para(c, f"• {mi}", STYLES['DarkMetaVal'], 695, curr_top, 195, 16)
        curr_top -= 24
        
    c.restoreState()

def build_slide_17(c):
    """Slide 17: Review 2 Architecture & Component Overview"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "11 / REVIEW 2 ARCHITECTURE", "Layered procedural surveillance architecture", "Active database logic: from raw incoming transaction to tamper-evident audit record.")
    
    cw = 200
    ch = 340
    cy = 70
    
    # Layer 1
    draw_card(c, 50, cy, cw, ch, accent_color=BLUE)
    draw_para(c, "LAYER 1", STYLES['CardTagNavy'], 65, cy + ch - 16, cw-25, 12)
    draw_para(c, "Analytical Views", STYLES['CardTitle'], 65, cy + ch - 36, cw-25, 20)
    l1_desc = "<b>Surveillance & Triage:</b><br/><br/>• <b>VW_HIGH_RISK_TRANSACTIONS:</b> Aggregates transactions >50k or FLAGGED with customer details.<br/><br/>• <b>VW_INVESTIGATION_SUMMARY:</b> Computes case duration, severity, and investigator load.<br/><br/>• <b>VW_CUSTOMER_FRAUD_EXPOSURE:</b> Evaluates customer exposure."
    draw_para(c, l1_desc, STYLES['CardBodySm'], 65, cy + ch - 64, cw-25, 250)
    
    # Layer 2
    draw_card(c, 270, cy, cw, ch, accent_color=TEAL)
    draw_para(c, "LAYER 2", STYLES['CardTagTeal'], 285, cy + ch - 16, cw-25, 12)
    draw_para(c, "Stored Procedures", STYLES['CardTitle'], 285, cy + ch - 36, cw-25, 20)
    l2_desc = "<b>Lifecycle Enforcement:</b><br/><br/>• <b>SP_EVALUATE_AND_ALERT_TRANSACTION:</b> Checks compliance threshold and generates alert.<br/><br/>• <b>SP_ASSIGN_INVESTIGATOR:</b> Validates investigator active status.<br/><br/>• <b>SP_UPDATE_INVESTIGATION_STATUS:</b> Enforces valid state progression."
    draw_para(c, l2_desc, STYLES['CardBodySm'], 285, cy + ch - 64, cw-25, 250)
    
    # Layer 3
    draw_card(c, 490, cy, cw, ch, accent_color=AMBER)
    draw_para(c, "LAYER 3", STYLES['CardTagAmber'], 505, cy + ch - 16, cw-25, 12)
    draw_para(c, "PL/SQL Functions", STYLES['CardTitle'], 505, cy + ch - 36, cw-25, 20)
    l3_desc = "<b>Scoring & Aggregation:</b><br/><br/>• <b>FN_CALCULATE_RISK_TIER:</b> Deterministically maps risk score to LOW, MEDIUM, HIGH, CRITICAL brackets.<br/><br/>• <b>FN_GET_TOTAL_TX_AMOUNT:</b> Calculates cumulative transacted volume per account.<br/><br/>• <b>FN_GET_ACCOUNT_ALERT_COUNT:</b> Sums alert count."
    draw_para(c, l3_desc, STYLES['CardBodySm'], 505, cy + ch - 64, cw-25, 250)
    
    # Layer 4
    draw_card(c, 710, cy, cw, ch, accent_color=colors.HexColor("#DC2626"))
    draw_para(c, "LAYER 4", STYLES['CardTagAmber'], 725, cy + ch - 16, cw-25, 12)
    draw_para(c, "Audit Triggers", STYLES['CardTitle'], 725, cy + ch - 36, cw-25, 20)
    l4_desc = "<b>Forensic Audit Trail:</b><br/><br/>• <b>TRG_INVESTIGATION_STATUS_AUDIT:</b> Fires on case status change; writes old/new status, timestamp, and user to INVESTIGATION_AUDIT.<br/><br/>• <b>TRG_FRAUD_ALERT_AUDIT:</b> Captures alert severity escalations into ALERT_AUDIT table."
    draw_para(c, l4_desc, STYLES['CardBodySm'], 725, cy + ch - 64, cw-25, 250)
    
    draw_footer(c, "17")
    c.restoreState()

def build_slide_18(c):
    """Slide 18: Advanced SQL Subqueries"""
    build_screenshot_slide(c, "12", "SUBQUERIES", "Scalar & multi-row anomaly detection", "Comparing transaction amounts against system-wide averages and subquery filtering.", "ss_oracle_r2_subquery.png", "6", "Subquery identifying transactions exceeding overall system average", "18", full_category="12 / ADVANCED SUBQUERIES")

def build_slide_19(c):
    """Slide 19: Database Views"""
    build_screenshot_slide(c, "13", "VIEWS", "Surveillance & triage dashboards", "VW_HIGH_RISK_TRANSACTIONS and VW_INVESTIGATION_SUMMARY for instant operational reporting.", "ss_oracle_r2_views.png", "7", "High-risk transaction view query output in Oracle SQL*Plus", "19", full_category="13 / DATABASE VIEWS")

def build_slide_20(c):
    """Slide 20: Stored Procedures"""
    build_screenshot_slide(c, "14", "PROCEDURES", "Investigator allocation & case progression", "SP_ASSIGN_INVESTIGATOR and SP_UPDATE_INVESTIGATION_STATUS validating state rules.", "ss_oracle_r2_procedures.png", "8", "Execution of investigator assignment and case progression procedures", "20", full_category="14 / STORED PROCEDURES")

def build_slide_21(c):
    """Slide 21: PL/SQL Functions"""
    build_screenshot_slide(c, "15", "FUNCTIONS", "Risk tier scoring & turnover calculation", "FN_CALCULATE_RISK_TIER and FN_GET_TOTAL_TX_AMOUNT providing dynamic scoring.", "ss_oracle_r2_functions.png", "9", "Customer risk tier evaluation query using custom PL/SQL function", "21", full_category="15 / PL/SQL FUNCTIONS")

def build_slide_22(c):
    """Slide 22: Cursors & Batch Processing"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "16 / CURSORS", "Explicit parameter-driven batch surveillance", "From sql/09_cursors.sql; row-by-row anomaly analysis across large transaction sets.")
    
    cur_lines = [
        "-- Explicit Cursor with Parameter for Account Turnover Sweep",
        "DECLARE",
        "  CURSOR cur_high_ticket (p_min_amount NUMBER) IS",
        "    SELECT t.transaction_id, t.account_id, t.amount, t.channel",
        "    FROM TRANSACTIONS t",
        "    WHERE t.amount >= p_min_amount",
        "    ORDER BY t.amount DESC;",
        "  v_tx cur_high_ticket%ROWTYPE;",
        "BEGIN",
        "  OPEN cur_high_ticket(p_min_amount => 100000.00);",
        "  LOOP",
        "    FETCH cur_high_ticket INTO v_tx;",
        "    EXIT WHEN cur_high_ticket%NOTFOUND;",
        "    DBMS_OUTPUT.PUT_LINE('FLAGGED HIGH TICKET: ' || v_tx.transaction_id ||",
        "                         ' Amount: ' || v_tx.amount);",
        "  END LOOP;",
        "  CLOSE cur_high_ticket;",
        "END;"
    ]
    draw_code_box(c, 50, 75, 430, 345, "PL/SQL EXPLICIT CURSOR IMPLEMENTATION", cur_lines)
    
    cw = 400
    ch = 160
    
    draw_card(c, 510, 260, cw, ch, accent_color=TEAL)
    draw_para(c, "CURSOR DESIGN PATTERNS", STYLES['CardTagTeal'], 530, 260 + ch - 16, cw-30, 15)
    draw_para(c, "Memory efficient record traversal", STYLES['CardTitle'], 530, 260 + ch - 36, cw-30, 20)
    p_c1 = "• <b>Explicit Cursors:</b> Utilized for granular transaction inspection where each record requires complex rule evaluation.<br/>• <b>Parameterization:</b> Thresholds (such as minimum transaction amounts) are injected dynamically at open time.<br/>• <b>%ROWTYPE Record Buffering:</b> Ensures type-safe row retrieval directly mapped to table structure."
    draw_para(c, p_c1, STYLES['CardBodySm'], 530, 260 + ch - 64, cw-30, 95)
    
    draw_card(c, 510, 75, cw, ch, accent_color=AMBER)
    draw_para(c, "EXCEPTION RESILIENCE", STYLES['CardTagAmber'], 530, 75 + ch - 16, cw-30, 15)
    draw_para(c, "Guaranteed cursor resource cleanup", STYLES['CardTitle'], 530, 75 + ch - 36, cw-30, 20)
    p_c2 = "• <b>Resource Leak Prevention:</b> All cursor blocks include exception handlers that verify `IF cur%ISOPEN THEN CLOSE cur; END IF;`.<br/>• <b>Bulk Collect Optimization:</b> Demonstrated in batch modules with `LIMIT 100` clauses to balance PGA memory usage against context-switching overhead."
    draw_para(c, p_c2, STYLES['CardBodySm'], 530, 75 + ch - 64, cw-30, 95)
    
    draw_footer(c, "22")
    c.restoreState()

def build_slide_23(c):
    """Slide 23: Triggers & Audit Trails"""
    build_screenshot_slide(c, "17", "TRIGGERS", "Tamper-evident forensic audit trails", "TRG_INVESTIGATION_STATUS_AUDIT writing automated change records to INVESTIGATION_AUDIT.", "ss_oracle_r2_triggers.png", "10", "Forensic audit log records populated automatically by row-level database triggers", "23", full_category="17 / AUDIT TRIGGERS")

def build_slide_24(c):
    """Slide 24: Transaction Control & Exception Handling"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "18 / TRANSACTION CONTROL", "Deterministic isolation & failure recovery", "Strict ACID adherence, controlled savepoints, and custom application error ranges.")
    
    headers = [Paragraph("Exception Code", STYLES['THeader']), Paragraph("Error Name", STYLES['THeader']), Paragraph("Enforced Business Condition", STYLES['THeader'])]
    rows = [
        [Paragraph("-20001", STYLES['TCellMono']), Paragraph("ERR_INVALID_CASE", STYLES['TCellBold']), Paragraph("Target investigation ID does not exist in database.", STYLES['TCell'])],
        [Paragraph("-20002", STYLES['TCellMono']), Paragraph("ERR_CLOSED_CASE", STYLES['TCellBold']), Paragraph("Attempt to reassign or modify an already CLOSED investigation.", STYLES['TCell'])],
        [Paragraph("-20003", STYLES['TCellMono']), Paragraph("ERR_INVALID_INVESTIGATOR", STYLES['TCellBold']), Paragraph("Investigator ID does not exist in registry.", STYLES['TCell'])],
        [Paragraph("-20004", STYLES['TCellMono']), Paragraph("ERR_INACTIVE_OFFICER", STYLES['TCellBold']), Paragraph("Investigator active_status is 'INACTIVE'; allocation blocked.", STYLES['TCell'])],
        [Paragraph("-20005", STYLES['TCellMono']), Paragraph("ERR_INVALID_PROGRESSION", STYLES['TCellBold']), Paragraph("Illegal status leap (e.g. CLOSED to OPEN without review).", STYLES['TCell'])],
        [Paragraph("-20030", STYLES['TCellMono']), Paragraph("ERR_ACC_NOT_FOUND", STYLES['TCellBold']), Paragraph("Account ID missing during function execution.", STYLES['TCell'])],
    ]
    t = Table([headers] + rows, colWidths=[110, 160, 240])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_HEADER),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, SLATE_200),
    ]))
    w, h = t.wrap(510, 340)
    t.drawOn(c, 50, 420 - h)
    
    cw = 325
    ch = 160
    
    draw_card(c, 585, 265, cw, ch, accent_color=BLUE)
    draw_para(c, "ACID ISOLATION", STYLES['CardTagNavy'], 605, 265 + ch - 16, cw-30, 12)
    draw_para(c, "READ COMMITTED Guarantees", STYLES['CardTitle'], 605, 265 + ch - 36, cw-30, 20)
    p_a1 = "• <b>No Dirty Reads:</b> Transactions read only committed database rows.<br/>• <b>Surveillance Consistency:</b> Automated alert generation procedures run under autonomous transactions when necessary, ensuring alerts persist even if application sessions roll back."
    draw_para(c, p_a1, STYLES['CardBodySm'], 605, 265 + ch - 64, cw-30, 95)
    
    draw_card(c, 585, 85, cw, ch, accent_color=AMBER)
    draw_para(c, "RECOVERY MECHANISMS", STYLES['CardTagAmber'], 605, 85 + ch - 16, cw-30, 12)
    draw_para(c, "Granular Savepoints", STYLES['CardTitle'], 605, 85 + ch - 36, cw-30, 20)
    p_a2 = "• <b>Partial Rollback Capability:</b> Multi-step investigations use named savepoints before assigning officers or changing statuses.<br/>• <b>Data Integrity Guarantee:</b> Failed batch updates roll back cleanly without leaving orphan alert flags or corrupted ledger states."
    draw_para(c, p_a2, STYLES['CardBodySm'], 605, 85 + ch - 64, cw-30, 95)
    
    draw_footer(c, "24")
    c.restoreState()

def build_slide_25(c):
    """Slide 25: Master End-to-End System Integration Workflow"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "19 / SYSTEM WORKFLOW", "End-to-end fraud investigation lifecycle", "Step-by-step trace from transaction journal entry to immutable audit archiving.")
    
    step_w = 160
    step_h = 330
    step_y = 80
    
    steps = [
        ("1. INGEST", "Transaction Journal", "A financial transaction is posted to TRANSACTIONS. Engine verifies CHK_TX_AMOUNT (>0), valid account FK, and channel domain.", BLUE),
        ("2. SURVEILLANCE", "Rule Evaluation", "SP_EVALUATE_AND_ALERT_TRANSACTION or VW_HIGH_RISK_TRANSACTIONS detects high value (>50k) or suspicious channel activity.", TEAL),
        ("3. TRIAGE", "Alert Generation", "FRAUD_ALERT record generated with severity (LOW to CRITICAL). Triage officer reviews unassigned alert queue.", AMBER),
        ("4. ALLOCATION", "Investigator Assigned", "SP_ASSIGN_INVESTIGATOR validates officer active_status before creating case in INVESTIGATION. Case opens in 'OPEN' state.", NAVY_HEADER),
        ("5. RESOLUTION", "Forensic Audit Log", "Officer records outcome ('CONFIRMED_FRAUD'). Trigger fires automatically, logging old/new status, timestamp, and user to INVESTIGATION_AUDIT.", colors.HexColor("#059669"))
    ]
    
    for i, (tag, title, desc, acc_color) in enumerate(steps):
        sx = 50 + i * (step_w + 15)
        draw_card(c, sx, step_y, step_w, step_h, accent_color=acc_color)
        draw_para(c, tag, STYLES['CardTagAmber'], sx + 14, step_y + step_h - 16, step_w-20, 12)
        draw_para(c, title, STYLES['CardTitle'], sx + 14, step_y + step_h - 36, step_w-20, 36)
        draw_para(c, desc, STYLES['CardBodySm'], sx + 14, step_y + step_h - 80, step_w-20, 240)
        
    draw_footer(c, "25")
    c.restoreState()

def build_slide_26(c):
    """Slide 26: Master Verification Test Suite (13 Test Cases)"""
    build_screenshot_slide(c, "20", "TEST HARNESS", "Master 13-case verification test suite", "Live execution of 11_test_cases.sql: 7 positive workflows and 6 negative constraint catches.", "ss_oracle_r2_tests.png", "11", "Verbatim execution output of master test harness confirming 100% test pass rate", "26", full_category="20 / VERIFICATION TEST HARNESS")

def build_slide_27(c):
    """Slide 27: Implementation Results & Technical Compliance Matrix"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "21 / IMPLEMENTATION RESULTS", "Technical compliance & verification matrix", "Audit of all database objects executed and genuinely verified against Oracle 23ai Free.")
    
    headers = [Paragraph("Component Category", STYLES['THeader']), Paragraph("Oracle Database Object(s)", STYLES['THeader']), Paragraph("Verified Count / State", STYLES['THeader']), Paragraph("Compliance Verdict", STYLES['THeader'])]
    rows = [
        [Paragraph("Relational Tables", STYLES['TCellBold']), Paragraph("CUSTOMER, ACCOUNT, TRANSACTIONS, FRAUD_ALERT, INVESTIGATOR, INVESTIGATION", STYLES['TCell']), Paragraph("6 Core Tables (VALID)", STYLES['TCellMono']), Paragraph("<font color='#16A34A'><b>100% VERIFIED</b></font>", STYLES['TCell'])],
        [Paragraph("Audit Tables", STYLES['TCellBold']), Paragraph("INVESTIGATION_AUDIT, ALERT_AUDIT", STYLES['TCell']), Paragraph("2 Forensic Tables (VALID)", STYLES['TCellMono']), Paragraph("<font color='#16A34A'><b>100% VERIFIED</b></font>", STYLES['TCell'])],
        [Paragraph("Primary Key Sequences", STYLES['TCellBold']), Paragraph("seq_cust_id, seq_acc_id, seq_tx_id, seq_alert_id, seq_inves_id, seq_inves_audit_id", STYLES['TCell']), Paragraph("6 Sequences (VALID)", STYLES['TCellMono']), Paragraph("<font color='#16A34A'><b>100% VERIFIED</b></font>", STYLES['TCell'])],
        [Paragraph("Surveillance Views", STYLES['TCellBold']), Paragraph("VW_HIGH_RISK_TRANSACTIONS, VW_INVESTIGATION_SUMMARY, VW_CUSTOMER_FRAUD_EXPOSURE", STYLES['TCell']), Paragraph("4 Views (VALID)", STYLES['TCellMono']), Paragraph("<font color='#16A34A'><b>100% VERIFIED</b></font>", STYLES['TCell'])],
        [Paragraph("Stored Procedures", STYLES['TCellBold']), Paragraph("SP_ASSIGN_INVESTIGATOR, SP_UPDATE_INVESTIGATION_STATUS, SP_EVALUATE_AND_ALERT_TRANSACTION", STYLES['TCell']), Paragraph("3 Procedures (VALID)", STYLES['TCellMono']), Paragraph("<font color='#16A34A'><b>100% VERIFIED</b></font>", STYLES['TCell'])],
        [Paragraph("PL/SQL Functions", STYLES['TCellBold']), Paragraph("FN_GET_TOTAL_TX_AMOUNT, FN_CALCULATE_RISK_TIER, FN_GET_ACCOUNT_ALERT_COUNT", STYLES['TCell']), Paragraph("3 Functions (VALID)", STYLES['TCellMono']), Paragraph("<font color='#16A34A'><b>100% VERIFIED</b></font>", STYLES['TCell'])],
        [Paragraph("Database Triggers", STYLES['TCellBold']), Paragraph("TRG_INVESTIGATION_STATUS_AUDIT, TRG_FRAUD_ALERT_AUDIT", STYLES['TCell']), Paragraph("2 Triggers (ENABLED)", STYLES['TCellMono']), Paragraph("<font color='#16A34A'><b>100% VERIFIED</b></font>", STYLES['TCell'])],
        [Paragraph("Baseline Data Journal", STYLES['TCellBold']), Paragraph("10 Customers, 12 Accounts, 18 Transactions, 7 Alerts, 4 Investigators, 5 Cases", STYLES['TCell']), Paragraph("56 Baseline Records", STYLES['TCellMono']), Paragraph("<font color='#16A34A'><b>100% VERIFIED</b></font>", STYLES['TCell'])],
    ]
    t = Table([headers] + rows, colWidths=[150, 390, 180, 140])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), NAVY_HEADER),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, colors.HexColor("#F8FAFC")]),
        ('GRID', (0,0), (-1,-1), 0.5, SLATE_200),
    ]))
    w, h = t.wrap(860, 340)
    t.drawOn(c, 50, 420 - h)
    
    draw_footer(c, "27")
    c.restoreState()

def build_slide_28(c):
    """Slide 28: Conclusion, Limitations & Future Scope"""
    c.saveState()
    c.setFillColor(LIGHT_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_header(c, "22 / CONCLUSION & ROADMAP", "Production readiness & future enhancements", "Honest engineering assessment of current system deliverables and roadmap.")
    
    cw = 415
    ch = 340
    cy = 70
    
    draw_card(c, 50, cy, cw, ch, accent_color=TEAL)
    draw_para(c, "COMPLETED DELIVERABLES", STYLES['CardTagTeal'], 70, cy + ch - 16, cw-30, 12)
    
    achs = [
        "<b>Rigorous 3NF Architecture:</b> Eliminated data redundancy and update anomalies across customer demographics, accounts, and case allocations.",
        "<b>Engine-Enforced Constraints:</b> Strict CHECK, UNIQUE, and FOREIGN KEY constraints reject invalid or corrupt records at the database kernel.",
        "<b>Active Procedural Surveillance:</b> Multi-tiered PL/SQL procedures and views automate fraud detection thresholds and case assignments.",
        "<b>Non-Repudiation Audit Defense:</b> Automated row-level triggers track case status transitions in forensic audit logs.",
        "<b>100% Test Pass Rate:</b> Fully executed and verified test suite proving both positive operational workflows and negative constraint defense."
    ]
    curr_top = cy + ch - 40
    for ach in achs:
        w_used, h_used = draw_para(c, f"• {ach}", STYLES['CardBodySm'], 70, curr_top, cw-40, 50)
        curr_top -= 55
        
    draw_card(c, 495, cy, cw, ch, accent_color=AMBER)
    draw_para(c, "LIMITATIONS & FUTURE SCOPE", STYLES['CardTagAmber'], 515, cy + ch - 16, cw-30, 12)
    
    limits = [
        "<b>Current Limitation — Synchronous Triggers:</b> Heavy trigger-based auditing on high-frequency transactions may impact write latency in ultra-high TPS environments.",
        "<b>Future Enhancement — Kafka Stream Ingestion:</b> Decouple ingest via Apache Kafka topics and micro-batched loader routines.",
        "<b>Current Limitation — Rule-Based Detection:</b> Surveillance rules rely on fixed thresholds (>50k INR, channel type) rather than behavioural patterns.",
        "<b>Future Enhancement — Machine Learning Inference:</b> Embed Oracle Machine Learning (OML) algorithms or ONNX models for real-time anomaly inference inside the database.",
        "<b>Future Enhancement — Distributed Ledger:</b> Implement Oracle Blockchain Tables to provide cryptographic immutability for the forensic audit trail."
    ]
    curr_top = cy + ch - 40
    for lim in limits:
        w_used, h_used = draw_para(c, f"• {lim}", STYLES['CardBodySm'], 515, curr_top, cw-40, 50)
        curr_top -= 55
        
    draw_footer(c, "28")
    c.restoreState()

def build_slide_29(c):
    """Slide 29: Final Combined Project Sign-Off Slide"""
    c.saveState()
    c.setFillColor(DARK_BG)
    c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    
    draw_para(c, "FRAUDLENS • COMPREHENSIVE REVIEW 1 & REVIEW 2 COMPLETE", STYLES['DarkTitleCat'], 60, 475, 700, 15)
    draw_para(c, "FraudLens: Master Project Completion", STYLES['DarkMainTitle'], 60, 435, 800, 40)
    draw_para(c, "Financial Transaction & Fraud Investigation Management System", STYLES['DarkSubtitle'], 60, 380, 800, 25)
    
    p_desc = (
        "A complete, university-grade Database Management Systems implementation encompassing relational "
        "modelling, Third Normal Form schema engineering, named integrity constraints, analytical querying, "
        "PL/SQL procedural surveillance, automated case lifecycle triage, and forensic audit logging."
    )
    draw_para(c, p_desc, STYLES['DarkDesc'], 60, 320, 780, 45)
    
    draw_card(c, 60, 140, 340, 120, bg_color=DARK_CARD)
    c.setStrokeColor(colors.HexColor("#331E24"))
    c.roundRect(60, 140, 340, 120, 6, stroke=1, fill=0)
    draw_para(c, "<b>D Joshua Daniel</b>", STYLES['DarkTeam'], 80, 140 + 120 - 18, 300, 20)
    p_joshua = "Registration No: <b>24BCE0436</b><br/>Bachelor of Technology in Computer Science & Engineering<br/>School of Computer Science & Engineering (SCOPE)<br/>Vellore Institute of Technology (VIT), Vellore"
    draw_para(c, p_joshua, STYLES['DarkMetaVal'], 80, 140 + 120 - 42, 300, 60)
    
    draw_card(c, 430, 140, 340, 120, bg_color=DARK_CARD)
    c.setStrokeColor(colors.HexColor("#331E24"))
    c.roundRect(430, 140, 340, 120, 6, stroke=1, fill=0)
    draw_para(c, "<b>M Saryu</b>", STYLES['DarkTeam'], 450, 140 + 120 - 18, 300, 20)
    p_saryu = "Registration No: <b>24BCE2524</b><br/>Bachelor of Technology in Computer Science & Engineering<br/>School of Computer Science & Engineering (SCOPE)<br/>Vellore Institute of Technology (VIT), Vellore"
    draw_para(c, p_saryu, STYLES['DarkMetaVal'], 450, 140 + 120 - 42, 300, 60)
    
    draw_para(c, "<b>Course: BCSE304L Database Management Systems • Faculty Guide: Prof. Kanagaraj K</b>", STYLES['DarkSubtitle'], 60, 95, 750, 25)
    
    c.restoreState()

# =============================================================================
# MAIN BUILD DRIVERS
# =============================================================================

def build_review_1_pdf():
    print(f">>> Building: {PDF_R1_UPDATED} (15 Widescreen 16:9 Slides)...")
    c = canvas.Canvas(PDF_R1_UPDATED, pagesize=(PAGE_W, PAGE_H))
    
    slides = [
        build_slide_1,
        build_slide_2,
        build_slide_3,
        build_slide_4,
        build_slide_5,
        build_slide_6,
        build_slide_7,
        build_slide_8,
        build_slide_9,
        build_slide_10,
        build_slide_11,
        build_slide_12,
        build_slide_13,
        build_slide_14,
        build_slide_15,
    ]
    
    for i, slide_fn in enumerate(slides):
        slide_fn(c)
        c.showPage()
        
    c.save()
    print(f"[SUCCESS] Saved Review 1 Updated PDF: {PDF_R1_UPDATED}")

def build_combined_pdf():
    print(f">>> Building: {PDF_COMBINED} (29 Widescreen 16:9 Slides)...")
    c = canvas.Canvas(PDF_COMBINED, pagesize=(PAGE_W, PAGE_H))
    
    combined_slides = [
        # Part A: Review 1 Foundations (Slides 1 to 15)
        build_slide_1,
        build_slide_2,
        build_slide_3,
        build_slide_4,
        build_slide_5,
        build_slide_6,
        build_slide_7,
        build_slide_8,
        build_slide_9,
        build_slide_10,
        build_slide_11,
        build_slide_12,
        build_slide_13,
        build_slide_14,
        build_slide_15,
        # Part B: Review 2 Advanced Implementation (Slides 16 to 29)
        build_slide_16,
        build_slide_17,
        build_slide_18,
        build_slide_19,
        build_slide_20,
        build_slide_21,
        build_slide_22,
        build_slide_23,
        build_slide_24,
        build_slide_25,
        build_slide_26,
        build_slide_27,
        build_slide_28,
        build_slide_29,
    ]
    
    for i, slide_fn in enumerate(combined_slides):
        slide_fn(c)
        c.showPage()
        
    c.save()
    print(f"[SUCCESS] Saved Combined Review 1 & Review 2 PDF: {PDF_COMBINED}")

def build_review_2_presentation_pdf():
    print(f">>> Building: {PDF_R2_PRESENTATION} (14 Widescreen 16:9 Slides)...")
    c = canvas.Canvas(PDF_R2_PRESENTATION, pagesize=(PAGE_W, PAGE_H))
    
    r2_slides = [
        build_slide_16,
        build_slide_17,
        build_slide_18,
        build_slide_19,
        build_slide_20,
        build_slide_21,
        build_slide_22,
        build_slide_23,
        build_slide_24,
        build_slide_25,
        build_slide_26,
        build_slide_27,
        build_slide_28,
        build_slide_29,
    ]
    
    for i, slide_fn in enumerate(r2_slides):
        slide_fn(c)
        c.showPage()
        
    c.save()
    print(f"[SUCCESS] Saved Review 2 Presentation PDF: {PDF_R2_PRESENTATION}")

if __name__ == "__main__":
    build_review_1_pdf()
    build_combined_pdf()
    build_review_2_presentation_pdf()
    print(">>> Finished generating all FraudLens presentation deliverables successfully!")
