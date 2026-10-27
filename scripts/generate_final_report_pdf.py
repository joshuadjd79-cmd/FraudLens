"""
FraudLens: Generate Corrected Final Academic Report PDF
Builds FraudLens_DBMS_Case_Study_Report_Final.pdf via ReportLab in A4 format.
Implements all technical audit corrections:
1. Replaces exaggerated claims with rigorous, student-appropriate academic language.
2. Accurately reports host OS (Windows 11 Home Single Language) and hardware specs (Core i3, 8GB RAM).
3. Reconciles transaction-to-alert cardinality (schema 1:N vs procedure 1:1 deduplication guard).
4. Explains audit trigger capabilities and non-repudiation vs DBA privileges.
5. Evaluates ON DELETE CASCADE design in prototype vs production banking retention rules.
6. Details the 71 constraints reconciliation (17 explicit CHECK + 36 NOT NULL + 8 PK + 5 FK + 5 UK).
7. Clearly distinguishes procedurally implemented rules (High Amount > 50k) from sample-simulated rules.
8. Provides mathematically rigorous 1NF, 2NF, 3NF normalization proofs.
9. Reflects VIT institution and team members: D Joshua Daniel (24BCE0436) & M Saryu (24BCE2524).
10. Synchronizes Table of Contents page numbers with exact physical layout.
"""

import os
from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from report_content import (
    STUDENT_INFO, TEST_CASES, DB_INVENTORY, TABLE_DEFINITIONS
)

# Colors
C_NAVY = colors.HexColor("#1E3A8A")
C_BLUE = colors.HexColor("#0284C7")
C_SLATE = colors.HexColor("#0F172A")
C_TEXT = colors.HexColor("#1E293B")
C_MUTED = colors.HexColor("#64748B")
C_LIGHT_BG = colors.HexColor("#F8FAFC")
C_BORDER = colors.HexColor("#CBD5E1")
C_CALLOUT_BG = colors.HexColor("#F0F9FF")
C_CODE_BG = colors.HexColor("#0F172A")
C_CODE_TEXT = colors.HexColor("#F1F5F9")
WHITE = colors.HexColor("#FFFFFF")

PAGE_W, PAGE_H = A4
MARGIN = 45.0
PRINT_W = PAGE_W - (2 * MARGIN)  # 505.27 pt

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, total_pages):
        if self._pageNumber > 1:
            self.saveState()
            
            # Running Header
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(MARGIN, PAGE_H - 36, PAGE_W - MARGIN, PAGE_H - 36)

            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(C_NAVY)
            self.drawString(MARGIN, PAGE_H - 30, "FRAUDLENS: FINANCIAL TRANSACTION & FRAUD INVESTIGATION SYSTEM")

            self.setFont("Helvetica", 7.5)
            self.setFillColor(C_MUTED)
            self.drawRightString(PAGE_W - MARGIN, PAGE_H - 30, "DBMS CASE STUDY REPORT")

            # Running Footer
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.6)
            self.line(MARGIN, 38, PAGE_W - MARGIN, 38)

            self.setFont("Helvetica", 8)
            self.setFillColor(C_MUTED)
            self.drawString(MARGIN, 26, f"B.Tech CSE — {STUDENT_INFO['subject']} | Students: D Joshua Daniel (24BCE0436) & M Saryu (24BCE2524)")

            page_str = f"Page {self._pageNumber} of {total_pages}"
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(C_NAVY)
            self.drawRightString(PAGE_W - MARGIN, 26, page_str)

            self.restoreState()

def setup_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles['TitleMain'] = ParagraphStyle(
        'TitleMain', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=26, leading=32,
        textColor=C_NAVY, alignment=1
    )
    styles['TitleSub'] = ParagraphStyle(
        'TitleSub', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=17,
        textColor=C_BLUE, alignment=1
    )
    styles['TitleDocType'] = ParagraphStyle(
        'TitleDocType', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=14,
        textColor=C_SLATE, alignment=1
    )
    styles['InstName'] = ParagraphStyle(
        'InstName', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=17,
        textColor=C_NAVY, alignment=1
    )
    styles['DeptName'] = ParagraphStyle(
        'DeptName', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=14,
        textColor=C_MUTED, alignment=1
    )

    styles['H1'] = ParagraphStyle(
        'H1', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=13.5, leading=17.5,
        textColor=C_NAVY, spaceBefore=13, spaceAfter=5,
        keepWithNext=True
    )
    styles['H2'] = ParagraphStyle(
        'H2', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=14.5,
        textColor=C_BLUE, spaceBefore=9, spaceAfter=3.5,
        keepWithNext=True
    )
    styles['H3'] = ParagraphStyle(
        'H3', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=C_SLATE, spaceBefore=7, spaceAfter=2.5,
        keepWithNext=True
    )

    styles['Body'] = ParagraphStyle(
        'Body', parent=base['Normal'],
        fontName='Helvetica', fontSize=8.8, leading=12.5,
        textColor=C_TEXT, spaceAfter=4.5
    )
    styles['Bullet'] = ParagraphStyle(
        'Bullet', parent=base['Normal'],
        fontName='Helvetica', fontSize=8.4, leading=11.8,
        textColor=C_TEXT, leftIndent=11, firstLineIndent=-7, spaceAfter=2.5
    )

    styles['CalloutBody'] = ParagraphStyle(
        'CalloutBody', parent=base['Normal'],
        fontName='Helvetica', fontSize=8.4, leading=11.5,
        textColor=C_TEXT
    )

    styles['Code'] = ParagraphStyle(
        'Code', parent=base['Normal'],
        fontName='Courier', fontSize=7.0, leading=9.0,
        textColor=C_CODE_TEXT
    )

    styles['TH'] = ParagraphStyle(
        'TH', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=7.8, leading=10,
        textColor=WHITE, alignment=1
    )
    styles['TD'] = ParagraphStyle(
        'TD', parent=base['Normal'],
        fontName='Helvetica', fontSize=7.2, leading=9.5,
        textColor=C_TEXT
    )
    styles['TDBold'] = ParagraphStyle(
        'TDBold', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=7.2, leading=9.5,
        textColor=C_SLATE
    )
    styles['TDMono'] = ParagraphStyle(
        'TDMono', parent=base['Normal'],
        fontName='Courier', fontSize=6.8, leading=8.8,
        textColor=C_TEXT
    )

    styles['FigCap'] = ParagraphStyle(
        'FigCap', parent=base['Normal'],
        fontName='Helvetica-Oblique', fontSize=7.8, leading=10,
        textColor=C_MUTED, alignment=1, spaceBefore=3, spaceAfter=8
    )

    return styles

STYLES = setup_styles()

def make_callout(title, text):
    content = [
        Paragraph(f"<b>{title}:</b> {text}", STYLES['CalloutBody'])
    ]
    t = Table([[content]], colWidths=[PRINT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CALLOUT_BG),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('LINELEFT', (0,0), (0,-1), 3.0, C_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    return t

def make_code_box(code_text):
    clean_lines = [line.rstrip() for line in code_text.strip().split("\n")]
    formatted_code = "<br/>".join([line.replace(" ", "&nbsp;").replace("<", "&lt;").replace(">", "&gt;") for line in clean_lines])
    p = Paragraph(formatted_code, STYLES['Code'])
    t = Table([[p]], colWidths=[PRINT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#334155")),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    return t

def make_scaled_image(img_path, max_w=PRINT_W, max_h=300):
    if not os.path.exists(img_path):
        return None
    with Image.open(img_path) as im:
        orig_w, orig_h = im.size
    scale = min(max_w / orig_w, max_h / orig_h, 1.0)
    w = orig_w * scale
    h = orig_h * scale
    return RLImage(img_path, width=w, height=h)

def generate_final_pdf():
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FraudLens_Report_Assets"))
    output_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FraudLens_DBMS_Case_Study_Report_Final.pdf"))

    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )

    story = []

    # =========================================================================
    # SECTION 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 15))
    story.append(Paragraph(STUDENT_INFO["institution"].upper(), STYLES['InstName']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", STYLES['DeptName']))
    story.append(Spacer(1, 35))

    story.append(Paragraph("FRAUDLENS", STYLES['TitleMain']))
    story.append(Spacer(1, 7))
    story.append(Paragraph("Financial Transaction and Fraud Investigation Management System", STYLES['TitleSub']))
    story.append(Spacer(1, 12))
    story.append(Paragraph("A COMPREHENSIVE DATABASE MANAGEMENT SYSTEMS CASE STUDY REPORT", STYLES['TitleDocType']))
    story.append(Spacer(1, 30))

    meta_rows = [
        [Paragraph("<b>Institution:</b>", STYLES['TDBold']), Paragraph(STUDENT_INFO["institution"], STYLES['TD'])],
        [Paragraph("<b>Submitted By:</b>", STYLES['TDBold']), 
         Paragraph("1. D Joshua Daniel (Reg No: 24BCE0436)<br/>2. M Saryu (Reg No: 24BCE2524)", STYLES['TD'])],
        [Paragraph("<b>Degree & Branch:</b>", STYLES['TDBold']), Paragraph(STUDENT_INFO["degree"], STYLES['TD'])],
        [Paragraph("<b>Subject:</b>", STYLES['TDBold']), Paragraph(STUDENT_INFO["subject"], STYLES['TD'])],
        [Paragraph("<b>Faculty Evaluator:</b>", STYLES['TDBold']), Paragraph(STUDENT_INFO["guide"], STYLES['TD'])],
        [Paragraph("<b>Database Platform:</b>", STYLES['TDBold']), Paragraph(STUDENT_INFO["db_platform"], STYLES['TD'])],
        [Paragraph("<b>PDB & Schema:</b>", STYLES['TDBold']), Paragraph(f"{STUDENT_INFO['container']} / {STUDENT_INFO['schema']}", STYLES['TD'])],
        [Paragraph("<b>Host Platform:</b>", STYLES['TDBold']), Paragraph("Microsoft Windows 11 Home Single Language | 8.0 GB RAM | Core i3-1115G4", STYLES['TD'])],
    ]
    t_meta = Table(meta_rows, colWidths=[130, 335])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1.0, C_NAVY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 9),
    ]))
    story.append(t_meta)

    story.append(Spacer(1, 35))
    story.append(Paragraph(f"<b>Submission Date:</b> {STUDENT_INFO['submission_date']} | Evaluated via Native Oracle SQL*Plus Engine", STYLES['FigCap']))
    story.append(PageBreak())

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    story.append(Paragraph("Table of Contents", STYLES['H1']))
    story.append(Spacer(1, 4))
    toc_data = [
        [Paragraph("<b>Section Title</b>", STYLES['TH']), Paragraph("<b>Page</b>", STYLES['TH'])]
    ]
    toc_entries = [
        ("1. Cover Page", "1"), ("2. Abstract", "3"), ("3. Introduction", "3"),
        ("4. Problem Statement", "3"), ("5. Objectives of the Project", "3"),
        ("6. Existing System and Its Limitations", "4"), ("7. Proposed System — FraudLens", "4"),
        ("8. Scope of the Project", "4"), ("9. Software and Hardware Requirements", "4"),
        ("10. System Architecture", "5"), ("11. Entity-Relationship (ER) Diagram", "5"),
        ("12. Relational Schema", "6"), ("13. Database Design and Normalization (1NF, 2NF, 3NF)", "7"),
        ("14. Table Structures and Relationships", "7"), ("15. Business Rules and Constraints", "11"),
        ("16. SQL Implementation", "12"), ("17. DDL and DML Operations", "12"),
        ("18. SQL Queries, Joins, Subqueries, and Aggregate Functions", "12"),
        ("19. Database Views", "13"), ("20. Stored Procedures and Functions", "13"),
        ("21. Database Cursors", "13"), ("22. Database Triggers and Audit Management", "14"),
        ("23. Fraud Detection and Alert Management Logic", "14"),
        ("24. Investigation Management and Workflow", "14"),
        ("25. Testing Methodology and Test Cases", "14"),
        ("26. Actual Execution Screenshots and Sample Outputs", "16"),
        ("27. Results and Discussion", "19"), ("28. Advantages and Limitations", "19"),
        ("29. Future Enhancements", "19"), ("30. Conclusion", "19"), ("31. References", "20"),
    ]
    for s_title, p_num in toc_entries:
        toc_data.append([Paragraph(s_title, STYLES['TD']), Paragraph(p_num, STYLES['TDBold'])])
    
    t_toc = Table(toc_data, colWidths=[430, 75])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, C_LIGHT_BG])
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 2: ABSTRACT
    # =========================================================================
    story.append(Paragraph("2. Abstract", STYLES['H1']))
    story.append(Paragraph(
        "Modern digital banking platforms process tens of millions of financial transactions daily across "
        "Unified Payments Interface (UPI), Internet Net-Banking, Mobile Applications, Point-of-Sale (POS), "
        "and Automated Teller Machines (ATMs). Ensuring low-latency payment execution while simultaneously maintaining "
        "rigorous Anti-Money Laundering (AML) surveillance presents a fundamental database design challenge. "
        "<b>FraudLens: Financial Transaction and Fraud Investigation Management System</b> is a comprehensive academic "
        "database case study developed for B.Tech Computer Science and Engineering, demonstrating how enterprise relational "
        "database principles solve these dual requirements.",
        STYLES['Body']
    ))
    story.append(Paragraph(
        "A foundational principle of FraudLens is the explicit decoupling of automated risk signals from legal proof of fraud: "
        "<b>a fraud alert indicates an anomaly requiring review; it does not prove criminal culpability</b>. Implemented on "
        "Oracle AI Database 26ai Free Release 23.26.3.0.0 (container <code>FREEPDB1</code>, schema <code>FRAUDLENS_USER</code>), "
        "FraudLens organizes data into 8 relational tables normalized to Third Normal Form (3NF), 8 synthetic primary key sequences, "
        "4 analytical surveillance views, 3 PL/SQL stored procedures, 3 stored functions, 2 row-level audit triggers, and "
        "71 data-dictionary integrity constraints. An automated 13-case test harness verified the expected operational "
        "workflows and constraint rejections across the documented execution run with a 13/13 (100%) recorded pass rate, "
        "validating baseline functional integrity without claiming exhaustive verification.",
        STYLES['Body']
    ))
    story.append(make_callout(
        "Academic Classification & Scope",
        "FraudLens is designed as an educational, auditable relational prototype demonstrating ACID transactional consistency, "
        "declarative constraint enforcement, and in-database procedural automation. It does not claim enterprise production-grade "
        "scalability or external regulatory compliance, but provides a fully reproducible reference architecture for academic evaluation."
    ))

    # =========================================================================
    # SECTION 3: INTRODUCTION
    # =========================================================================
    story.append(Paragraph("3. Introduction", STYLES['H1']))
    story.append(Paragraph(
        "The digital transformation of retail banking has replaced batch-clearing systems with round-the-clock instant payment rails. "
        "In India, platforms like UPI handle billions of monthly transactions, demanding sub-second ledger updates. Concurrently, financial "
        "institutions face sophisticated cyber threats including automated account takeover, rapid velocity cash draining, smurfing (structuring "
        "transfers below regulatory thresholds), and unauthorized cross-border transactions. Handling these operational complexities requires "
        "a reliable Database Management System (DBMS) that enforces ACID properties (Atomicity, Consistency, Isolation, Durability).",
        STYLES['Body']
    ))
    story.append(Paragraph(
        "FraudLens bridges the gap between high-throughput transaction recording and forensic casework. By embedding surveillance threshold "
        "evaluation and audit logging directly into Oracle's relational engine via constraints, views, and PL/SQL subprograms, FraudLens "
        "ensures that ledger movements, anomaly flags, investigator assignments, and state transitions remain consistent, auditable, and traceable.",
        STYLES['Body']
    ))

    # =========================================================================
    # SECTION 4: PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("4. Problem Statement", STYLES['H1']))
    story.append(Paragraph("Contemporary commercial and educational banking systems face four critical relational challenges:", STYLES['Body']))
    story.append(Paragraph("• <b>High-Velocity Anomaly Detection:</b> Transactions must be checked against risk thresholds without introducing prohibitive locking or latency into the core ledger.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Alert vs. Proof Distinction:</b> Automated surveillance engines trigger probabilistic alerts. Labeling a customer transaction as fraudulent without forensic review leads to wrongful account freezing. Systems require structured handoffs from automated signals to qualified human caseworkers.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Casework Allocation & State Progression:</b> Surveillance alerts must be formally escalated into investigations, allocated strictly to active, qualified investigators, and tracked through verified lifecycle states.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Application-Level Forensic Auditability:</b> Every case state transition must be historically captured with session identification and timestamps, preventing unauthorized case alterations.", STYLES['Bullet']))

    # =========================================================================
    # SECTION 5: OBJECTIVES OF THE PROJECT
    # =========================================================================
    story.append(Paragraph("5. Objectives of the Project", STYLES['H1']))
    story.append(Paragraph("• <b>1. Schema Normalization:</b> Design a normalized Third Normal Form (3NF) relational schema for customers, accounts, transactions, alerts, investigators, and investigations.", STYLES['Bullet']))
    story.append(Paragraph("• <b>2. Declarative Integrity:</b> Enforce domain check constraints (positive amounts, non-negative balances, valid enums) and referential integrity directly within the Oracle engine.", STYLES['Bullet']))
    story.append(Paragraph("• <b>3. Procedural Surveillance Automation:</b> Develop a PL/SQL stored procedure to evaluate high-ticket transactions (> INR 50,000) and dispatch alerts automatically.", STYLES['Bullet']))
    story.append(Paragraph("• <b>4. Case Lifecycle Management:</b> Implement procedures that enforce investigator qualification checks and mandate a definitive verdict prior to case closure.", STYLES['Bullet']))
    story.append(Paragraph("• <b>5. Analytical Views:</b> Create database views that abstract complex multi-table joins for operational triage and risk reporting.", STYLES['Bullet']))
    story.append(Paragraph("• <b>6. Trigger-Based Event Auditing:</b> Construct row-level triggers to populate decoupled audit tables on every status modification.", STYLES['Bullet']))
    story.append(Paragraph("• <b>7. Native Oracle Verification:</b> Validate all DDL, DML, queries, and PL/SQL subprograms natively against Oracle AI Database 26ai Free.", STYLES['Bullet']))

    # =========================================================================
    # SECTION 6: EXISTING SYSTEM AND ITS LIMITATIONS
    # =========================================================================
    story.append(Paragraph("6. Existing System and Its Limitations", STYLES['H1']))
    story.append(Paragraph("Traditional institutional and legacy student DBMS projects exhibit several critical design flaws:", STYLES['Body']))
    story.append(Paragraph("• <b>Denormalized/Flat Ledgers:</b> Customer personal details and transaction histories are merged into flat tables, causing update anomalies and massive redundancy.", STYLES['Bullet']))
    story.append(Paragraph("• <b>External Application Reliance:</b> Business rules (e.g. positive balances, threshold alerts) are implemented solely in application code, leaving the database vulnerable to corrupted data if queried directly.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Unlinked Casework:</b> Alerts are logged without formal linkage to certified investigators, resulting in lost accountability.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Lack of Audit Trails:</b> Status fields are updated in-place (UPDATE status = 'CLOSED') without preserving historical transitions, preventing retrospective compliance reviews.", STYLES['Bullet']))

    # =========================================================================
    # SECTION 7: PROPOSED SYSTEM — FRAUDLENS
    # =========================================================================
    story.append(Paragraph("7. Proposed System — FraudLens", STYLES['H1']))
    story.append(Paragraph("FraudLens addresses these shortcomings through a structured, auditable database architecture:", STYLES['Body']))
    story.append(Paragraph("• <b>Decoupled Relational Model:</b> Strict separation of customer profiles, bank accounts, monetary movements, anomaly alerts, and forensic casework across 8 tables.", STYLES['Bullet']))
    story.append(Paragraph("• <b>In-Database Surveillance Logic:</b> Stored procedure <code>SP_EVALUATE_AND_ALERT_TRANSACTION</code> executes within the database tier, evaluating high-value thresholds and flagging transactions deterministically.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Controlled Investigation Dossier:</b> Formal 1:1 linkage between alerts and investigations, assignable only to investigators verified as active.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Autonomous Event Auditing:</b> Row-level triggers intercept updates on <code>INVESTIGATION</code> and <code>FRAUD_ALERT</code>, capturing old/new status, acting database user, and timestamp into dedicated audit logs.", STYLES['Bullet']))

    # =========================================================================
    # SECTION 8: SCOPE OF THE PROJECT
    # =========================================================================
    story.append(Paragraph("8. Scope of the Project", STYLES['H1']))
    story.append(Paragraph("The functional scope of the FraudLens prototype encompasses:", STYLES['Body']))
    story.append(Paragraph("• <b>Customer Onboarding:</b> KYC status tracking (VERIFIED, PENDING, REJECTED) and baseline credit/fraud risk score management.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Multi-Account Management:</b> Savings, Current, Salary, and NRI accounts with non-negative balance checks.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Multi-Channel Movements:</b> Recording deposits, withdrawals, transfers, and payments across Mobile App, Net Banking, ATM, POS, and UPI.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Automated High-Value Alerting:</b> Detection of transactions exceeding INR 50,000 threshold and alert generation via stored procedure.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Investigation Progression:</b> Case assignment, state transitions (OPEN -> UNDER REVIEW -> CLOSED), and definitive verdict recording.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Transaction Engine Demarcation:</b> FraudLens functions as a surveillance and forensic tracking system. It records transaction events, channel metadata, and surveillance flags in <code>TRANSACTIONS</code>, with account balance snapshots in <code>ACCOUNT.balance</code>. It does not perform automated general ledger debit/credit balance mutations upon insert.", STYLES['Bullet']))
    story.append(Paragraph("• <b>ACID Testing Scope:</b> The test harness explicitly verified Atomicity (atomic PL/SQL execution and savepoint rollbacks) and Consistency (71 integrity constraints). Multi-user concurrency isolation and recovery testing were not performed.", STYLES['Bullet']))
    story.append(Paragraph("<b>Scope Demarcation (Future Scope):</b> Real-time Kafka streaming, machine learning classification, biometric hashes, and distributed graph databases represent planned future extensions.", STYLES['Body']))

    # =========================================================================
    # SECTION 9: SOFTWARE AND HARDWARE REQUIREMENTS
    # =========================================================================
    story.append(Paragraph("9. Software and Hardware Requirements", STYLES['H1']))
    story.append(Paragraph("9.1 Software Requirements", STYLES['H2']))
    story.append(Paragraph("• <b>Database Management System:</b> Oracle AI Database 26ai Free Release 23.26.3.0.0 (Container: <code>FREEPDB1</code>, Schema: <code>FRAUDLENS_USER</code>)", STYLES['Bullet']))
    story.append(Paragraph("• <b>Client Interfaces:</b> Oracle SQL*Plus 23.26.0.0.0, Oracle SQL Developer 23.x / 24.x", STYLES['Bullet']))
    story.append(Paragraph("• <b>Database Languages:</b> Oracle SQL (DDL, DML, DQL) and Oracle PL/SQL (Procedures, Functions, Cursors, Triggers)", STYLES['Bullet']))
    story.append(Paragraph("• <b>Validation & Reporting Environment:</b> Python 3.10+ (reportlab, python-docx, Pillow, pypdf)", STYLES['Bullet']))
    story.append(Paragraph("• <b>Verified Host Operating System:</b> Microsoft Windows 11 Home Single Language (64-bit, Build 26200)", STYLES['Bullet']))

    story.append(Paragraph("9.2 Hardware Specifications: Host Environment vs System Sizing", STYLES['H2']))
    hw_rows = [
        [Paragraph("<b>Hardware Component</b>", STYLES['TH']), Paragraph("<b>Verified Host Machine (Actual)</b>", STYLES['TH']), Paragraph("<b>Minimum Required Specs</b>", STYLES['TH']), Paragraph("<b>Enterprise Recommended Specs</b>", STYLES['TH'])],
        [Paragraph("Processor (CPU)", STYLES['TDBold']), Paragraph("11th Gen Intel Core i3-1115G4 @ 3.00GHz (2 Cores, 4 Threads)", STYLES['TD']), Paragraph("Dual-Core x86_64 CPU (2.0 GHz)", STYLES['TD']), Paragraph("Intel Xeon / Core i7 (8+ Cores)", STYLES['TD'])],
        [Paragraph("Primary Memory (RAM)", STYLES['TDBold']), Paragraph("8.0 GB RAM (SGA/PGA dynamic pool)", STYLES['TD']), Paragraph("4.0 GB RAM", STYLES['TD']), Paragraph("16.0+ GB RAM", STYLES['TD'])],
        [Paragraph("Secondary Storage", STYLES['TDBold']), Paragraph("256 GB NVMe SSD (NTFS File System)", STYLES['TD']), Paragraph("20 GB Storage Space", STYLES['TD']), Paragraph("50+ GB Enterprise NVMe SSD", STYLES['TD'])],
    ]
    t_hw = Table(hw_rows, colWidths=[105, 135, 120, 145])
    t_hw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, C_LIGHT_BG])
    ]))
    story.append(t_hw)
    story.append(Paragraph("Table 1: Hardware Specifications: Actual Host Environment vs Minimum and Recommended Sizing", STYLES['FigCap']))

    # =========================================================================
    # SECTION 10: SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("10. System Architecture", STYLES['H1']))
    story.append(Paragraph(
        "The FraudLens architecture is structured into four decoupled layers, providing clean separation between transactional "
        "ingestion, anomaly surveillance, caseworker management, and forensic audit logging. Figure 1 illustrates this end-to-end flow.",
        STYLES['Body']
    ))
    img_arch = make_scaled_image(os.path.join(assets_dir, "architecture_flow.png"), max_w=PRINT_W, max_h=230)
    if img_arch:
        story.append(img_arch)
        story.append(Paragraph("Figure 1: FraudLens End-to-End System Architecture Flow Diagram", STYLES['FigCap']))
    story.append(Paragraph(
        "<b>Architecture Flow Breakdown:</b><br/>"
        "1. <b>Ingestion Layer:</b> Banking clients execute transactions across digital channels (Mobile App, UPI, Net-Banking, ATM, POS). "
        "Transactions are recorded in the <code>TRANSACTIONS</code> table with immediate ACID atomicity.<br/>"
        "2. <b>Surveillance & Rule Engine:</b> Stored procedure <code>SP_EVALUATE_AND_ALERT_TRANSACTION</code> is explicitly "
        "invoked via application logic, batch runs, or test harness calls (not via an automated table trigger). "
        "For transactions exceeding the INR 50,000 threshold, it updates transaction status to <code>FLAGGED</code> and generates an alert in <code>FRAUD_ALERT</code>.<br/>"
        "3. <b>Investigation Subsystem:</b> Triage officers review unassigned alerts via <code>VW_UNASSIGNED_ALERTS</code> and open an <code>INVESTIGATION</code> dossier. "
        "Procedure <code>SP_ASSIGN_INVESTIGATOR</code> verifies investigator eligibility and assigns lead responsibility.<br/>"
        "4. <b>Audit Subsystem:</b> Row-level database triggers intercept <code>UPDATE</code> statements, recording state changes into <code>INVESTIGATION_AUDIT</code>.",
        STYLES['Body']
    ))

    # =========================================================================
    # SECTION 11: ENTITY-RELATIONSHIP (ER) DIAGRAM
    # =========================================================================
    story.append(Paragraph("11. Entity-Relationship (ER) Diagram", STYLES['H1']))
    story.append(Paragraph(
        "The conceptual design of FraudLens models 6 core entities and 2 supporting audit event streams. "
        "Figure 2 presents the complete Entity-Relationship diagram with primary keys, foreign keys, and cardinalities.",
        STYLES['Body']
    ))
    img_erd = make_scaled_image(os.path.join(assets_dir, "erd_diagram.png"), max_w=PRINT_W, max_h=280)
    if img_erd:
        story.append(img_erd)
        story.append(Paragraph("Figure 2: FraudLens Entity-Relationship (ER) Diagram (Oracle Data Modeler Standard)", STYLES['FigCap']))
    story.append(Paragraph(
        "<b>Entity Cardinality Specifications & Architectural Reconciliation:</b><br/>"
        "• <b>CUSTOMER to ACCOUNT (1 : N):</b> One customer owns one or multiple bank accounts; each account belongs to exactly one customer.<br/>"
        "• <b>ACCOUNT to TRANSACTIONS (1 : N):</b> One account maintains multiple financial transaction records; each transaction belongs to a single account.<br/>"
        "• <b>TRANSACTIONS to FRAUD_ALERT (Structural 1 : N vs Procedural 1 : 1 Guard):</b> In the relational DDL, <code>transaction_id</code> is a non-unique foreign key in <code>FRAUD_ALERT</code>, structurally allowing multiple alerts (e.g. from different rule engines) per transaction. Procedurally, <code>SP_EVALUATE_AND_ALERT_TRANSACTION</code> executes a transaction-level deduplication check (<code>WHERE transaction_id = p_transaction_id</code>) that exits if ANY alert exists for the transaction, operating as 1:0..1 to prevent duplicate alerts regardless of rule type.<br/>"
        "• <b>FRAUD_ALERT to INVESTIGATION (1 : 0..1):</b> In the relational schema, <code>INVESTIGATION.alert_id</code> is defined with both a Foreign Key referencing <code>FRAUD_ALERT(alert_id)</code> and a <code>UNIQUE NOT NULL</code> constraint (<code>uq_inv_alert</code>). This guarantees that each investigation docket references exactly one alert, and no alert can be linked to multiple investigations. The relationship is <b>1 : 0..1</b> because an alert can exist without an investigation (e.g., pending triage or dismissed alerts like Alert 7005 and 7007, tracked via <code>VW_UNASSIGNED_ALERTS</code>).<br/>"
        "• <b>INVESTIGATOR to INVESTIGATION (1 : N):</b> One investigator manages multiple assigned investigation cases.<br/>"
        "• <b>INVESTIGATION to INVESTIGATION_AUDIT (1 : N):</b> Each investigation generates a chronological stream of audit event records.",
        STYLES['Body']
    ))

    # =========================================================================
    # SECTION 12: RELATIONAL SCHEMA
    # =========================================================================
    story.append(Paragraph("12. Relational Schema", STYLES['H1']))
    story.append(Paragraph(
        "The formal relational schema of FraudLens is expressed below, where Primary Keys are enclosed in bold brackets [PK] "
        "and Foreign Keys are marked with [FK]:",
        STYLES['Body']
    ))
    schema_text = (
        "CUSTOMER ([customer_id PK], first_name, last_name, email [UK], phone [UK], kyc_status, risk_score, created_at)\n\n"
        "ACCOUNT ([account_id PK], customer_id [FK -> CUSTOMER], account_number [UK], account_type, balance, currency, status, created_at)\n\n"
        "TRANSACTIONS ([transaction_id PK], account_id [FK -> ACCOUNT], transaction_type, amount, transaction_date, channel, status, counterparty_account, description)\n\n"
        "FRAUD_ALERT ([alert_id PK], transaction_id [FK -> TRANSACTIONS], alert_type, severity, rule_triggered, alert_date, status)\n\n"
        "INVESTIGATOR ([investigator_id PK], first_name, last_name, email [UK], department, experience_years, active_status)\n\n"
        "INVESTIGATION ([investigation_id PK], alert_id [FK -> FRAUD_ALERT, UK], investigator_id [FK -> INVESTIGATOR], start_date, end_date, status, outcome, notes)\n\n"
        "INVESTIGATION_AUDIT ([audit_id PK], investigation_id, old_status, new_status, changed_by, change_timestamp, change_action)\n\n"
        "ALERT_AUDIT ([audit_id PK], alert_id, old_status, new_status, changed_by, change_timestamp, remarks)"
    )
    story.append(make_code_box(schema_text))

    # =========================================================================
    # SECTION 13: DATABASE DESIGN AND NORMALIZATION
    # =========================================================================
    story.append(Paragraph("13. Database Design and Normalization (1NF, 2NF, 3NF)", STYLES['H1']))
    story.append(Paragraph(
        "Database normalization systematically eliminates data redundancy, prevents insertion, update, and deletion anomalies, "
        "and ensures that all non-trivial functional dependencies adhere to relational database theory.",
        STYLES['Body']
    ))
    story.append(Paragraph("13.1 First Normal Form (1NF)", STYLES['H2']))
    story.append(Paragraph(
        "<b>Definition:</b> A relation R is in 1NF if and only if the domain of each attribute contains only atomic (indivisible) values, "
        "and there are no repeating groups, arrays, or multi-valued attributes.<br/>"
        "<b>Application to FraudLens:</b> All attributes in FraudLens hold atomic scalar values. Customer names are decomposed into "
        "<code>first_name</code> and <code>last_name</code> rather than composite strings. Phone numbers and email addresses are atomic. "
        "Each table possesses an explicitly designated single-column primary key, ensuring tuple distinctness.",
        STYLES['Body']
    ))
    story.append(Paragraph("13.2 Second Normal Form (2NF)", STYLES['H2']))
    story.append(Paragraph(
        "<b>Definition:</b> A relation R is in 2NF if it is in 1NF and every non-prime attribute is fully functionally dependent on each candidate key. "
        "A partial dependency occurs when a non-prime attribute depends on a proper subset of a composite candidate key.<br/>"
        "<b>Application to FraudLens:</b> In FraudLens, every table utilizes a single-attribute synthetic primary key (e.g. <code>customer_id</code>, "
        "<code>account_id</code>, <code>transaction_id</code>). Since a proper subset of a single-attribute key is the empty set, "
        "partial functional dependencies cannot exist mathematically. Therefore, all non-prime attributes are fully functionally dependent on the candidate key.",
        STYLES['Body']
    ))
    story.append(Paragraph("13.3 Third Normal Form (3NF)", STYLES['H2']))
    story.append(Paragraph(
        "<b>Definition:</b> A relation R is in 3NF if it is in 2NF and for every non-trivial functional dependency X -> Y, either X is a superkey, "
        "or Y is a prime attribute (part of a candidate key). This eliminates transitive functional dependencies (X -> Y and Y -> Z).<br/>"
        "<b>Proof Across FraudLens Entities:</b><br/>"
        "• <code>CUSTOMER</code>: Functional dependencies are <code>customer_id -> {first_name, last_name, email, phone, kyc_status, risk_score, created_at}</code>, "
        "<code>email -> customer_id</code>, and <code>phone -> customer_id</code>. Since the determinants are candidate keys, no transitive dependencies exist.<br/>"
        "• <code>ACCOUNT</code>: Functional dependency is <code>account_id -> {customer_id, account_number, account_type, balance, currency, status, created_at}</code>. "
        "Customer demographics (names, risk scores) are not stored here, eliminating transitive dependencies through <code>customer_id</code>.<br/>"
        "• <code>TRANSACTIONS</code>: Functional dependency is <code>transaction_id -> {account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description}</code>. "
        "Account balances and customer information are strictly excluded and accessed via joins through <code>account_id</code>.<br/>"
        "• <code>FRAUD_ALERT</code>: Transaction details (amount, channel) reside in <code>TRANSACTIONS</code>, avoiding transitive redundancy.<br/>"
        "• <code>INVESTIGATION</code>: Investigator department and experience depend strictly on <code>investigator_id</code> and are not stored in the case docket.<br/>"
        "<b>Verification of Non-Key Determinants:</b> A single-column primary key guarantees 2NF, but 3NF additionally requires that non-key attributes do not determine each other. In FraudLens, independent non-key attributes (e.g., <code>kyc_status</code> and <code>risk_score</code> in CUSTOMER, or <code>account_type</code> and <code>currency</code> in ACCOUNT) have no functional dependency between them, ensuring every determinant is a candidate superkey.",
        STYLES['Body']
    ))
    story.append(make_callout(
        "Decoupled Design of Audit Tables",
        "The audit tables (INVESTIGATION_AUDIT and ALERT_AUDIT) are append-only historical ledgers with surrogate primary keys (audit_id). "
        "They intentionally omit restrictive foreign keys to remain decoupled, ensuring audit records persist even if parent records are archived."
    ))

    # =========================================================================
    # SECTION 14: TABLE STRUCTURES AND RELATIONSHIPS
    # =========================================================================
    story.append(Paragraph("14. Table Structures and Relationships", STYLES['H1']))
    story.append(Paragraph(
        "FraudLens comprises 8 relational tables. The schema definitions, data types, constraints, and operational purposes "
        "for each table are detailed below.",
        STYLES['Body']
    ))

    for idx, tbl_def in enumerate(TABLE_DEFINITIONS):
        t_story = []
        t_story.append(Paragraph(f"14.{idx + 1} Table: {tbl_def['name']}", STYLES['H2']))
        t_story.append(Paragraph(f"<b>Purpose:</b> {tbl_def['purpose']}", STYLES['Body']))
        t_story.append(Paragraph(f"• <b>Primary Key:</b> {tbl_def['pk']} | <b>Foreign Keys:</b> {tbl_def['fks']}", STYLES['Bullet']))
        t_story.append(Paragraph(f"• <b>Check Constraints:</b> {tbl_def['checks']}", STYLES['Bullet']))

        table_rows = [
            [Paragraph("<b>Column</b>", STYLES['TH']), Paragraph("<b>Data Type</b>", STYLES['TH']), Paragraph("<b>Null?</b>", STYLES['TH']),
             Paragraph("<b>Default</b>", STYLES['TH']), Paragraph("<b>Constraint</b>", STYLES['TH']), Paragraph("<b>Description</b>", STYLES['TH'])]
        ]
        for col in tbl_def["columns"]:
            table_rows.append([
                Paragraph(col[0], STYLES['TDMono']),
                Paragraph(col[1], STYLES['TD']),
                Paragraph(col[2], STYLES['TD']),
                Paragraph(col[3], STYLES['TD']),
                Paragraph(col[4], STYLES['TDBold']),
                Paragraph(col[5], STYLES['TD']),
            ])
        t_col = Table(table_rows, colWidths=[90, 80, 35, 55, 105, 140])
        t_col.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), C_NAVY),
            ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, C_LIGHT_BG])
        ]))
        t_story.append(t_col)
        t_story.append(Spacer(1, 5))
        story.append(KeepTogether(t_story))

    story.append(make_callout(
        "Statutory Retention & Critical Evaluation of ON DELETE CASCADE",
        "The prototype defines ON DELETE CASCADE on foreign keys linking customers, accounts, transactions, and alerts as an academic testing convenience "
        "to enable clean test harness rollbacks. In production banking, physical record deletion is strictly prohibited: Section 12(1)(a) of the Prevention "
        "of Money Laundering Act (PMLA) 2002, Rule 3 of the PML Rules 2005 (amended by Finance Act 2019), Chapter VII of the RBI KYC Master Direction 2016 "
        "(Updated 2023), and FATF Recommendation 11 legally mandate a minimum 5-year retention period for transaction records from the transaction date "
        "and customer identification records from the cessation of the relationship. Production banking schemas mandate ON DELETE RESTRICT and logical soft deletion (status = 'CLOSED')."
    ))

    # =========================================================================
    # SECTION 15: BUSINESS RULES AND CONSTRAINTS
    # =========================================================================
    story.append(Paragraph("15. Business Rules and Constraints", STYLES['H1']))
    story.append(Paragraph(
        "Data integrity in FraudLens is enforced declaratively through 71 constraints compiled in Oracle's data dictionary. "
        "Table 2 categorizes all verified database objects, and Table 3 details the exact constraint breakdown.",
        STYLES['Body']
    ))
    inv_rows = [
        [Paragraph("<b>Object Type</b>", STYLES['TH']), Paragraph("<b>Count</b>", STYLES['TH']), Paragraph("<b>Status</b>", STYLES['TH']), Paragraph("<b>Verified Objects / Notes</b>", STYLES['TH'])]
    ]
    for row in DB_INVENTORY:
        inv_rows.append([
            Paragraph(row[0], STYLES['TDBold']),
            Paragraph(row[1], STYLES['TD']),
            Paragraph(row[2], STYLES['TDBold']),
            Paragraph(row[3], STYLES['TD']),
        ])
    t_inv = Table(inv_rows, colWidths=[100, 45, 60, 300])
    t_inv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, C_LIGHT_BG])
    ]))
    story.append(t_inv)
    story.append(Paragraph("Table 2: FraudLens Database Object Inventory Verified in Oracle AI Database 26ai", STYLES['FigCap']))

    # Constraint Reconciliation Sub-table
    c_breakdown_rows = [
        [Paragraph("<b>Constraint Type in USER_CONSTRAINTS</b>", STYLES['TH']), Paragraph("<b>Count</b>", STYLES['TH']), Paragraph("<b>Composition Details & Business Rules</b>", STYLES['TH'])],
        [Paragraph("Type 'C' (Check / NOT NULL Constraints)", STYLES['TDBold']), Paragraph("53", STYLES['TD']), Paragraph("17 explicit domain business rules (amount > 0, balance >= 0, status enums, dates) + 36 column NOT NULL integrity checks", STYLES['TD'])],
        [Paragraph("Type 'P' (Primary Keys)", STYLES['TDBold']), Paragraph("8", STYLES['TD']), Paragraph("Single-column primary keys for all 8 tables (pk_customer, pk_account, etc.)", STYLES['TD'])],
        [Paragraph("Type 'R' (Referential Integrity / Foreign Keys)", STYLES['TDBold']), Paragraph("5", STYLES['TD']), Paragraph("Foreign keys: fk_acc_customer, fk_tx_account, fk_alert_tx, fk_inv_alert, fk_inv_investigator", STYLES['TD'])],
        [Paragraph("Type 'U' (Unique Keys)", STYLES['TDBold']), Paragraph("5", STYLES['TD']), Paragraph("Unique keys: uq_customer_email, uq_customer_phone, uq_acc_number, uq_inv_email, uq_inv_alert", STYLES['TD'])],
        [Paragraph("<b>TOTAL VERIFIED CONSTRAINTS</b>", STYLES['TDBold']), Paragraph("<b>71</b>", STYLES['TDBold']), Paragraph("<b>All 71 constraints verified active in Oracle data dictionary (USER_CONSTRAINTS)</b>", STYLES['TDBold'])],
    ]
    t_cb = Table(c_breakdown_rows, colWidths=[150, 45, 310])
    t_cb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [WHITE, C_LIGHT_BG]),
        ('BACKGROUND', (0,-1), (-1,-1), C_LIGHT_BG),
    ]))
    story.append(t_cb)
    story.append(Paragraph("Table 3: Exact Reconciliation of 71 Oracle Data Dictionary Integrity Constraints", STYLES['FigCap']))

    # =========================================================================
    # SECTION 16: SQL IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("16. SQL Implementation", STYLES['H1']))
    story.append(Paragraph(
        "The FraudLens SQL implementation is organized into 12 numbered scripts executed in dependency order. "
        "The master pipeline script <code>00_run_all.sql</code> controls compilation and testing:",
        STYLES['Body']
    ))
    p_code = (
        "-- Master Driver Pipeline: 00_run_all.sql\n"
        "SET DEFINE OFF;\n"
        "SET SERVEROUTPUT ON SIZE 1000000;\n"
        "PROMPT >>> Executing 01_schema.sql (Tables, Sequences, Constraints)\n"
        "@@sql/01_schema.sql\n"
        "PROMPT >>> Executing 02_ddl_dml_demos.sql (Review 1 DDL/DML Demonstrations)\n"
        "@@sql/02_ddl_dml_demos.sql\n"
        "PROMPT >>> Executing 03_sample_data.sql (Seed Data: 56 Baseline Records)\n"
        "@@sql/03_sample_data.sql\n"
        "PROMPT >>> Executing 04_review1_queries.sql (Single-Row Functions & Joins)\n"
        "@@sql/04_review1_queries.sql\n"
        "PROMPT >>> Executing 05_review2_subqueries_joins.sql (Subqueries & Joins)\n"
        "@@sql/05_review2_subqueries_joins.sql\n"
        "PROMPT >>> Executing 06_views.sql (Analytical & Triage Views)\n"
        "@@sql/06_views.sql\n"
        "PROMPT >>> Executing 07_procedures.sql (Stored Procedures)\n"
        "@@sql/07_procedures.sql\n"
        "PROMPT >>> Executing 08_functions.sql (Stored Functions)\n"
        "@@sql/08_functions.sql\n"
        "PROMPT >>> Executing 09_cursors.sql (Explicit & Parameterized Cursors)\n"
        "@@sql/09_cursors.sql\n"
        "PROMPT >>> Executing 10_triggers_audit.sql (Row-Level Audit Triggers)\n"
        "@@sql/10_triggers_audit.sql\n"
        "PROMPT >>> Executing 11_test_cases.sql (13 Automated Test Cases)\n"
        "@@sql/11_test_cases.sql"
    )
    story.append(make_code_box(p_code))

    # =========================================================================
    # SECTION 17: DDL AND DML OPERATIONS
    # =========================================================================
    story.append(Paragraph("17. DDL and DML Operations", STYLES['H1']))
    story.append(Paragraph(
        "Script <code>02_ddl_dml_demos.sql</code> demonstrates schema modifications (ALTER, ADD, DROP, RENAME) and safe DML operations "
        "isolated within transactional savepoints to avoid polluting seed data.",
        STYLES['Body']
    ))
    ddl_snip = (
        "-- Review 1 DDL Modifications & Constraint Alterations\n"
        "ALTER TABLE CUSTOMER ADD (middle_name VARCHAR2(50));\n"
        "ALTER TABLE CUSTOMER MODIFY (middle_name VARCHAR2(100));\n"
        "ALTER TABLE CUSTOMER RENAME COLUMN middle_name TO secondary_name;\n"
        "ALTER TABLE CUSTOMER DROP COLUMN secondary_name;\n\n"
        "-- Safe DML with Transaction Control\n"
        "SAVEPOINT sp_before_dml_demo;\n"
        "INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score)\n"
        "VALUES (seq_customer_id.NEXTVAL, 'Test', 'User', 'temp.test@demo.in', '+919999988888', 'PENDING', 20);\n"
        "UPDATE CUSTOMER SET kyc_status = 'VERIFIED' WHERE email = 'temp.test@demo.in';\n"
        "ROLLBACK TO sp_before_dml_demo;"
    )
    story.append(make_code_box(ddl_snip))

    # =========================================================================
    # SECTION 18: SQL QUERIES, JOINS, SUBQUERIES, AND AGGREGATE FUNCTIONS
    # =========================================================================
    story.append(Paragraph("18. SQL Queries, Joins, Subqueries, and Aggregate Functions", STYLES['H1']))
    story.append(Paragraph(
        "FraudLens includes a rich suite of analytical queries demonstrating single-row functions, multi-table joins, "
        "group aggregations, and subqueries.",
        STYLES['Body']
    ))
    story.append(Paragraph("18.1 Channel Aggregation (GROUP BY & HAVING)", STYLES['H2']))
    q_grp = (
        "SELECT channel, COUNT(transaction_id) AS total_tx,\n"
        "       SUM(amount) AS total_volume, ROUND(AVG(amount), 2) AS avg_ticket\n"
        "FROM TRANSACTIONS GROUP BY channel HAVING SUM(amount) > 100000\n"
        "ORDER BY total_volume DESC;"
    )
    story.append(make_code_box(q_grp))
    q2_rows = [
        [Paragraph("<b>Channel</b>", STYLES['TH']), Paragraph("<b>Total Txns</b>", STYLES['TH']), Paragraph("<b>Total Volume (INR)</b>", STYLES['TH']), Paragraph("<b>Average Ticket (INR)</b>", STYLES['TH'])],
        [Paragraph("NET_BANKING", STYLES['TD']), Paragraph("8", STYLES['TD']), Paragraph("1,820,000.00", STYLES['TDBold']), Paragraph("227,500.00", STYLES['TD'])],
        [Paragraph("ATM", STYLES['TD']), Paragraph("3", STYLES['TD']), Paragraph("262,000.00", STYLES['TDBold']), Paragraph("87,333.33", STYLES['TD'])],
        [Paragraph("UPI", STYLES['TD']), Paragraph("4", STYLES['TD']), Paragraph("128,500.00", STYLES['TDBold']), Paragraph("32,125.00", STYLES['TD'])],
    ]
    t_q2 = Table(q2_rows, colWidths=[120, 80, 150, 155])
    t_q2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, C_LIGHT_BG])
    ]))
    story.append(t_q2)

    # =========================================================================
    # SECTION 19: DATABASE VIEWS
    # =========================================================================
    story.append(Paragraph("19. Database Views", STYLES['H1']))
    story.append(Paragraph(
        "Four operational database views provide real-time transaction surveillance, customer risk postures, and case triage queues:",
        STYLES['Body']
    ))
    v_code = (
        "-- 1. VW_HIGH_RISK_TRANSACTIONS: Real-time high-ticket surveillance\n"
        "CREATE OR REPLACE VIEW VW_HIGH_RISK_TRANSACTIONS AS\n"
        "SELECT t.transaction_id, a.account_number, c.first_name || ' ' || c.last_name AS customer_name,\n"
        "       t.amount, t.channel, t.status AS tx_status, fa.alert_id, fa.severity AS alert_severity\n"
        "FROM TRANSACTIONS t\n"
        "JOIN ACCOUNT a ON t.account_id = a.account_id\n"
        "JOIN CUSTOMER c ON a.customer_id = c.customer_id\n"
        "LEFT JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id\n"
        "WHERE t.amount > 50000.00 OR t.status = 'FLAGGED';\n\n"
        "-- 2. VW_UNASSIGNED_ALERTS: Real-time triage queue for pending signals\n"
        "CREATE OR REPLACE VIEW VW_UNASSIGNED_ALERTS AS\n"
        "SELECT fa.alert_id, fa.transaction_id, t.amount, t.channel, fa.alert_type, fa.severity\n"
        "FROM FRAUD_ALERT fa\n"
        "JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id\n"
        "WHERE fa.alert_id NOT IN (SELECT alert_id FROM INVESTIGATION);"
    )
    story.append(make_code_box(v_code))

    # =========================================================================
    # SECTION 20: STORED PROCEDURES AND FUNCTIONS
    # =========================================================================
    story.append(Paragraph("20. Stored Procedures and Functions", STYLES['H1']))
    story.append(Paragraph(
        "PL/SQL stored subprograms automate surveillance and case operations directly inside the database tier:",
        STYLES['Body']
    ))
    sp_snip = (
        "-- Stored Procedure: SP_EVALUATE_AND_ALERT_TRANSACTION\n"
        "CREATE OR REPLACE PROCEDURE SP_EVALUATE_AND_ALERT_TRANSACTION (\n"
        "    p_transaction_id IN NUMBER, p_new_alert_id OUT NUMBER\n"
        ") AS\n"
        "    v_amount NUMBER(15,2); v_existing NUMBER; v_next_id NUMBER;\n"
        "BEGIN\n"
        "    SELECT amount INTO v_amount FROM TRANSACTIONS WHERE transaction_id = p_transaction_id;\n"
        "    SELECT COUNT(*) INTO v_existing FROM FRAUD_ALERT WHERE transaction_id = p_transaction_id;\n"
        "    IF v_existing > 0 THEN p_new_alert_id := NULL; RETURN; END IF;\n"
        "    IF v_amount > 50000.00 THEN\n"
        "        SELECT seq_alert_id.NEXTVAL INTO v_next_id FROM DUAL;\n"
        "        INSERT INTO FRAUD_ALERT (alert_id, transaction_id, alert_type, severity, rule_triggered, status)\n"
        "        VALUES (v_next_id, p_transaction_id, 'HIGH_AMOUNT', 'HIGH',\n"
        "                'Rule 101: Transaction amount ' || TO_CHAR(v_amount, 'FM999,990.00') || ' INR exceeds 50k threshold', 'PENDING');\n"
        "        UPDATE TRANSACTIONS SET status = 'FLAGGED' WHERE transaction_id = p_transaction_id;\n"
        "        p_new_alert_id := v_next_id;\n"
        "    END IF;\n"
        "END SP_EVALUATE_AND_ALERT_TRANSACTION;"
    )
    story.append(make_code_box(sp_snip))

    # =========================================================================
    # SECTION 21: CURSORS
    # =========================================================================
    story.append(Paragraph("21. Database Cursors", STYLES['H1']))
    story.append(Paragraph(
        "FraudLens implements explicit cursors (OPEN, FETCH, %NOTFOUND, CLOSE) for high-risk surveillance and "
        "parameterized cursor FOR loops for batch-processing active investigation queues.",
        STYLES['Body']
    ))
    cur_snip = (
        "-- Explicit Cursor: High-Risk Alert Surveillance\n"
        "DECLARE\n"
        "    CURSOR cur_high_risk_alerts IS\n"
        "        SELECT fa.alert_id, fa.severity, t.amount, a.account_number\n"
        "        FROM FRAUD_ALERT fa\n"
        "        JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id\n"
        "        JOIN ACCOUNT a ON t.account_id = a.account_id\n"
        "        WHERE fa.severity IN ('CRITICAL', 'HIGH');\n"
        "    v_rec cur_high_risk_alerts%ROWTYPE;\n"
        "BEGIN\n"
        "    OPEN cur_high_risk_alerts;\n"
        "    LOOP\n"
        "        FETCH cur_high_risk_alerts INTO v_rec; EXIT WHEN cur_high_risk_alerts%NOTFOUND;\n"
        "        DBMS_OUTPUT.PUT_LINE('Alert ' || v_rec.alert_id || ' | Severity: ' || v_rec.severity);\n"
        "    END LOOP;\n"
        "    CLOSE cur_high_risk_alerts;\n"
        "END;"
    )
    story.append(make_code_box(cur_snip))

    # =========================================================================
    # SECTION 22: TRIGGERS AND AUDIT MANAGEMENT
    # =========================================================================
    story.append(Paragraph("22. Database Triggers and Audit Management", STYLES['H1']))
    story.append(Paragraph(
        "Row-level database triggers record an automated chronological audit log by capturing previous and new states, "
        "the acting database user, and precise timestamps into <code>INVESTIGATION_AUDIT</code> and <code>ALERT_AUDIT</code>.",
        STYLES['Body']
    ))
    trg_snip = (
        "CREATE OR REPLACE TRIGGER TRG_INVESTIGATION_STATUS_AUDIT\n"
        "AFTER UPDATE OF status ON INVESTIGATION FOR EACH ROW\n"
        "WHEN (OLD.status != NEW.status)\n"
        "DECLARE v_next_id NUMBER;\n"
        "BEGIN\n"
        "    SELECT seq_inves_audit_id.NEXTVAL INTO v_next_id FROM DUAL;\n"
        "    INSERT INTO INVESTIGATION_AUDIT (audit_id, investigation_id, old_status, new_status, changed_by, change_timestamp)\n"
        "    VALUES (v_next_id, :NEW.investigation_id, :OLD.status, :NEW.status, USER, SYSTIMESTAMP);\n"
        "END;"
    )
    story.append(make_code_box(trg_snip))
    story.append(make_callout(
        "Trigger-Based Audit Logging vs Privileged Administrator Access",
        "Row-level database triggers provide autonomous, application-level audit logging and non-repudiation against standard user sessions "
        "by capturing USER and SYSTIMESTAMP upon every status modification. However, triggers do not make audit tables tamper-proof or immutable. "
        "Privileged database administrators (DBA / SYSDBA) possess the authority to disable triggers (ALTER TRIGGER ... DISABLE), truncate tables, "
        "or directly alter audit rows. In regulated banking environments, true regulatory immutability against administrator tampering requires "
        "cryptographic ledger tables (such as Oracle Blockchain Tables) or write-once-read-many (WORM) storage appliances."
    ))

    # =========================================================================
    # SECTION 23: FRAUD DETECTION AND ALERT MANAGEMENT LOGIC
    # =========================================================================
    story.append(Paragraph("23. Fraud Detection and Alert Management Logic", STYLES['H1']))
    story.append(Paragraph(
        "FraudLens defines six heuristic risk classifications in its domain constraints. <b>Procedural Automation Scope:</b> In the current "
        "prototype, the <code>HIGH_AMOUNT</code> rule (> INR 50,000 threshold) is actively evaluated and automated by procedure "
        "<code>SP_EVALUATE_AND_ALERT_TRANSACTION</code>. The remaining five categories are modeled in sample seed data to demonstrate "
        "forensic triage and reporting, representing proposed future procedural rules:",
        STYLES['Body']
    ))
    story.append(Paragraph("• <b>1. HIGH_AMOUNT (Active Stored Procedure):</b> Flags single transactions exceeding INR 50,000 threshold. Sets status to FLAGGED and generates Alert with HIGH severity.", STYLES['Bullet']))
    story.append(Paragraph("• <b>2. RAPID_VELOCITY (Seed-Modeled / Proposed Rule):</b> Flags rapid successive fund movements indicating automated account draining.", STYLES['Bullet']))
    story.append(Paragraph("• <b>3. SUSPICIOUS_CHANNEL (Seed-Modeled / Proposed Rule):</b> Flags unexpected channel usage (e.g. Net-Banking for dormant customer).", STYLES['Bullet']))
    story.append(Paragraph("• <b>4. UNUSUAL_HOURS (Seed-Modeled / Proposed Rule):</b> Flags high-value debits during non-standard hours (02:00 AM - 04:30 AM).", STYLES['Bullet']))
    story.append(Paragraph("• <b>5. CROSS_BORDER (Seed-Modeled / Proposed Rule):</b> Flags international transfers without travel notices.", STYLES['Bullet']))
    story.append(Paragraph("• <b>6. STRUCTURING (Seed-Modeled / Proposed Rule):</b> Flags smurfing transfers split just under the INR 50,000 reporting threshold (e.g. INR 49,500).", STYLES['Bullet']))
    story.append(Paragraph(
        "<b>Alert Deduplication Guard Analysis:</b> Procedure <code>SP_EVALUATE_AND_ALERT_TRANSACTION</code> executes "
        "<code>SELECT COUNT(*) INTO v_existing_alerts FROM FRAUD_ALERT WHERE transaction_id = p_transaction_id;</code>. "
        "If any alert already exists for the transaction, the procedure immediately exits without generating another alert. "
        "This operates as <b>transaction-level deduplication</b> (suppressing all subsequent alerts for that transaction, regardless of rule type) "
        "to prevent duplicate alerts from repeated batch runs, preserving a clean 1:0..1 procedure-to-alert relationship.",
        STYLES['Body']
    ))

    # =========================================================================
    # SECTION 24: INVESTIGATION MANAGEMENT
    # =========================================================================
    story.append(Paragraph("24. Investigation Management and Workflow", STYLES['H1']))
    story.append(Paragraph(
        "Investigations transition through OPEN -> UNDER REVIEW -> CLOSED. Closure requires a definitive verdict "
        "(CONFIRMED_FRAUD, FALSE_POSITIVE, INCONCLUSIVE). Figure 3 depicts this forensic lifecycle.",
        STYLES['Body']
    ))
    img_flow = make_scaled_image(os.path.join(assets_dir, "workflow_lifecycle.png"), max_w=PRINT_W, max_h=190)
    if img_flow:
        story.append(img_flow)
        story.append(Paragraph("Figure 3: FraudLens Investigation Lifecycle and Forensic Workflow State Transition Diagram", STYLES['FigCap']))

    # =========================================================================
    # SECTION 25: TESTING METHODOLOGY AND TEST CASES
    # =========================================================================
    story.append(Paragraph("25. Testing Methodology and Test Cases", STYLES['H1']))
    story.append(Paragraph(
        "Table 4 documents the 13-case test harness executed natively against Oracle AI Database 26ai Free. "
        "The FraudLens implementation passed all 13 documented test cases in the recorded execution run. "
        "These tests demonstrate the expected behavior of the selected operational workflows and constraint checks. "
        "They do not constitute exhaustive correctness verification or a formal performance benchmark.",
        STYLES['Body']
    ))
    test_rows = [
        [Paragraph("<b>ID</b>", STYLES['TH']), Paragraph("<b>Category</b>", STYLES['TH']), Paragraph("<b>Target Operation</b>", STYLES['TH']),
         Paragraph("<b>Expected Oracle Behavior</b>", STYLES['TH']), Paragraph("<b>Actual Verified Result</b>", STYLES['TH']), Paragraph("<b>Status</b>", STYLES['TH'])]
    ]
    for tc in TEST_CASES:
        test_rows.append([
            Paragraph(tc["id"], STYLES['TDBold']),
            Paragraph(tc["category"], STYLES['TD']),
            Paragraph(tc["operation"], STYLES['TDMono']),
            Paragraph(tc["expected"], STYLES['TD']),
            Paragraph(tc["actual"], STYLES['TD']),
            Paragraph(tc["status"], STYLES['TDBold']),
        ])
    t_tests = Table(test_rows, colWidths=[25, 65, 125, 115, 135, 40])
    t_tests.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, C_LIGHT_BG])
    ]))
    story.append(t_tests)
    story.append(Paragraph("Table 4: FraudLens Automated Positive and Negative Test Case Verification Matrix", STYLES['FigCap']))

    # =========================================================================
    # SECTION 26: ACTUAL EXECUTION SCREENSHOTS AND SAMPLE OUTPUTS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("26. Actual Execution Screenshots and Sample Outputs", STYLES['H1']))
    story.append(Paragraph(
        "All visual evidence below represents genuine console executions captured directly from Oracle SQL*Plus "
        "and Oracle SQL Developer in the active schema <code>FRAUDLENS_USER</code> on container <code>FREEPDB1</code>.",
        STYLES['Body']
    ))

    screenshots = [
        ("01_oracle_connection_and_pdb.png", "Figure 4: Oracle SQL*Plus Terminal Connection, Container FREEPDB1, and Schema FRAUDLENS_USER", 215),
        ("02_table_creation_and_list.png", "Figure 5: Table Creation and Data Dictionary Status Verification (USER_TABLES: All 8 Tables VALID)", 215),
        ("03_sample_data_row_counts.png", "Figure 6: Baseline Sample Dataset Record Counts (56 Total Operational Records Across 8 Tables)", 195),
        ("04_join_and_groupby_queries.png", "Figure 7: Execution of Multi-Table Relational Joins and Channel Aggregation (GROUP BY & HAVING)", 215),
        ("05_constraint_rejection_test.png", "Figure 8: Database Engine Blocking Check Constraint Violation (Negative Amount Rejected with ORA-02290)", 175),
        ("06_main_script_execution.png", "Figure 9: Master Test Pipeline Completion Banner — 100% Automated Test Suite Passing Status", 215),
        ("oracle_ss_q1.png", "Figure 10: Oracle SQL Developer Execution Grid — Single-Row Customer Normalization Functions", 215),
        ("oracle_ss_q4.png", "Figure 11: Oracle SQL Developer Master 6-Table Relational Dossier Output", 215),
    ]

    for fname, caption, mh in screenshots:
        fpath = os.path.join(assets_dir, fname)
        img = make_scaled_image(fpath, max_w=PRINT_W, max_h=mh)
        if img:
            ss_story = [img, Paragraph(caption, STYLES['FigCap']), Spacer(1, 4)]
            story.append(KeepTogether(ss_story))

    # =========================================================================
    # SECTION 27: RESULTS AND DISCUSSION
    # =========================================================================
    story.append(Paragraph("27. Results and Discussion", STYLES['H1']))
    story.append(Paragraph(
        "The FraudLens implementation passed all 13 documented test cases in the recorded execution run. These tests demonstrate "
        "the expected behavior of the selected operational workflows and constraint checks, without constituting exhaustive correctness verification:\n"
        "• <b>Schema Compilation:</b> All 8 tables, 8 sequences, 4 views, 3 procedures, 3 functions, and 2 triggers compiled without errors.\n"
        "• <b>Constraint Robustness:</b> All 71 integrity constraints operated deterministically. Negative tests 2.1 through 2.6 proved that "
        "negative amounts, duplicate emails, orphan accounts, inactive investigator assignments, and incomplete closures are trapped.\n"
        "• <b>Transactional Control & ACID Scope:</b> Master test scripts executed with transactional savepoints and clean rollbacks, verifying that "
        "operational data integrity and atomicity are preserved during negative test failure and batch pipeline execution. Oracle's underlying MVCC engine guarantees statement-level read consistency and durability; multi-user concurrency stress testing and crash recovery experiments were outside the scope of this student project.",
        STYLES['Body']
    ))

    # =========================================================================
    # SECTION 28: ADVANTAGES AND LIMITATIONS
    # =========================================================================
    story.append(Paragraph("28. Advantages and Limitations", STYLES['H1']))
    story.append(Paragraph("28.1 Advantages", STYLES['H2']))
    story.append(Paragraph("• <b>Normalized Design:</b> Third Normal Form schema eliminates duplicate storage of customer and investigator demographics.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Database-Tier Enforcement:</b> Integrity constraints (CHECK, UNIQUE, FK CASCADE) prevent invalid data entry at the database engine level.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Procedural Automation:</b> Automated threshold surveillance eliminates manual triage delays for high-value transactions.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Trigger-Based Audit Logging:</b> Row-level database triggers automatically record state transitions into dedicated audit tables, preserving chronological event history against application-tier alteration (while recognizing that privileged SYSDBA administrators retain database-level alteration authority).", STYLES['Bullet']))

    story.append(Paragraph("28.2 Limitations", STYLES['H2']))
    story.append(Paragraph("• <b>Static Rule Thresholds:</b> Thresholds (e.g. INR 50,000) are hardcoded and do not adapt dynamically to customer behavioral changes.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Batch/In-DB Processing:</b> PL/SQL evaluates transactions after or during commit; it is not a distributed real-time streaming engine like Apache Flink.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Single-Node Architecture:</b> The current implementation runs on a single Oracle pluggable database rather than a globally distributed multi-region cluster.", STYLES['Bullet']))

    # =========================================================================
    # SECTION 29: FUTURE ENHANCEMENTS
    # =========================================================================
    story.append(Paragraph("29. Future Enhancements", STYLES['H1']))
    story.append(Paragraph("• <b>1. Machine Learning Integration:</b> Integrate machine learning models (e.g. Isolation Forests, XGBoost) via Oracle Machine Learning (OML) for dynamic risk scoring.", STYLES['Bullet']))
    story.append(Paragraph("• <b>2. Graph Database Modeling:</b> Incorporate graph database structures (Oracle Property Graph / Neo4j) to uncover cyclic fund routing and money-mule networks.", STYLES['Bullet']))
    story.append(Paragraph("• <b>3. Distributed Event Streaming:</b> Deploy Apache Kafka and Kafka Connect for real-time low-latency transaction ingestion and event streaming.", STYLES['Bullet']))
    story.append(Paragraph("• <b>4. Biometric & Device Forensics:</b> Incorporate biometric verification timestamps and device fingerprint hashes into the TRANSACTIONS table.", STYLES['Bullet']))

    # =========================================================================
    # SECTION 30: CONCLUSION
    # =========================================================================
    story.append(Paragraph("30. Conclusion", STYLES['H1']))
    story.append(Paragraph(
        "FraudLens: Financial Transaction and Fraud Investigation Management System demonstrates the practical application of "
        "enterprise database management principles to modern financial security. Through rigorous Third Normal Form schema design, "
        "declarative constraints, procedural PL/SQL surveillance, analytical views, and autonomous audit triggers, FraudLens provides "
        "a resilient, auditable platform for transaction monitoring and forensic case management.",
        STYLES['Body']
    ))
    story.append(Paragraph(
        "By executing against Oracle AI Database 26ai Free Release 23.26.3.0.0 and validating the 13 documented operational test cases, "
        "this project illustrates how foundational relational modeling and procedural constraints provide dependable operational integrity for transactional monitoring systems.",
        STYLES['Body']
    ))

    # =========================================================================
    # SECTION 31: REFERENCES
    # =========================================================================
    story.append(Paragraph("31. References", STYLES['H1']))
    refs = [
        "1. Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). Database System Concepts (7th ed.). McGraw-Hill Education.",
        "2. Elmasri, R., & Navathe, S. B. (2016). Fundamentals of Database Systems (7th ed.). Pearson.",
        "3. Oracle Corporation. (2024). Oracle Database 23ai / 26ai SQL Language Reference (Release 23c/26ai). Oracle Help Center.",
        "4. Oracle Corporation. (2024). Oracle Database PL/SQL Language Reference (Release 23c/26ai). Oracle Help Center.",
        "5. Reserve Bank of India (RBI). (2023). Master Direction - Know Your Customer (KYC) Direction, 2016 (Updated 2023). RBI Guidelines.",
        "6. Financial Action Task Force (FATF). (2022). Guidance on Risk-Based Approach for the Banking Sector. FATF/OECD.",
        "7. Codd, E. F. (1970). A Relational Model of Data for Large Shared Data Banks. Communications of the ACM, 13(6), 377-387.",
        "8. Date, C. J. (2004). An Introduction to Database Systems (8th ed.). Addison-Wesley."
    ]
    for r in refs:
        story.append(Paragraph(r, STYLES['Body']))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[FINAL PDF] Successfully generated: {output_pdf}")

if __name__ == "__main__":
    generate_final_pdf()
