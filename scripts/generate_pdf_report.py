"""
FraudLens: Complete PDF Academic Report Generator
Builds FraudLens_DBMS_Case_Study_Report.pdf via ReportLab in A4 portrait format.
Includes running headers/footers with 'Page X of Y' (NumberedCanvas),
academic cover page, table of contents, all 31 academic sections,
high-resolution diagrams, genuine Oracle execution screenshots,
syntax-highlighted code blocks, and structured data tables.
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
PRINT_W = PAGE_W - (2 * MARGIN)  # 595.27 - 90 = 505.27 pt

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas that computes total pages and prints running headers/footers."""
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
        # Skip header and footer on cover page (page 1)
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
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=C_NAVY, alignment=1
    )
    styles['DeptName'] = ParagraphStyle(
        'DeptName', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=C_MUTED, alignment=1
    )

    styles['H1'] = ParagraphStyle(
        'H1', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=C_NAVY, spaceBefore=14, spaceAfter=6,
        keepWithNext=True
    )
    styles['H2'] = ParagraphStyle(
        'H2', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=11.5, leading=15,
        textColor=C_BLUE, spaceBefore=10, spaceAfter=4,
        keepWithNext=True
    )
    styles['H3'] = ParagraphStyle(
        'H3', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=9.5, leading=13,
        textColor=C_SLATE, spaceBefore=7, spaceAfter=3,
        keepWithNext=True
    )

    styles['Body'] = ParagraphStyle(
        'Body', parent=base['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=C_TEXT, spaceAfter=5
    )
    styles['Bullet'] = ParagraphStyle(
        'Bullet', parent=base['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=C_TEXT, leftIndent=12, firstLineIndent=-8, spaceAfter=3
    )

    styles['CalloutTitle'] = ParagraphStyle(
        'CalloutTitle', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=C_NAVY
    )
    styles['CalloutBody'] = ParagraphStyle(
        'CalloutBody', parent=base['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11.5,
        textColor=C_TEXT
    )

    styles['Code'] = ParagraphStyle(
        'Code', parent=base['Normal'],
        fontName='Courier', fontSize=7.2, leading=9.2,
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
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
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
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def make_scaled_image(img_path, max_w=PRINT_W, max_h=320):
    if not os.path.exists(img_path):
        return None
    with Image.open(img_path) as im:
        orig_w, orig_h = im.size
    scale = min(max_w / orig_w, max_h / orig_h, 1.0)
    w = orig_w * scale
    h = orig_h * scale
    return RLImage(img_path, width=w, height=h)

def generate_pdf():
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FraudLens_Report_Assets"))
    output_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FraudLens_DBMS_Case_Study_Report.pdf"))

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
    story.append(Spacer(1, 20))
    story.append(Paragraph(STUDENT_INFO["institution"].upper(), STYLES['InstName']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", STYLES['DeptName']))
    story.append(Spacer(1, 40))

    story.append(Paragraph("FRAUDLENS", STYLES['TitleMain']))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Financial Transaction and Fraud Investigation Management System", STYLES['TitleSub']))
    story.append(Spacer(1, 14))
    story.append(Paragraph("A COMPREHENSIVE DATABASE MANAGEMENT SYSTEMS CASE STUDY REPORT", STYLES['TitleDocType']))
    story.append(Spacer(1, 35))

    # Meta Box Table
    meta_rows = [
        [Paragraph("<b>Institution:</b>", STYLES['TDBold']), Paragraph(STUDENT_INFO["institution"], STYLES['TD'])],
        [Paragraph("<b>Submitted By:</b>", STYLES['TDBold']), 
         Paragraph("1. D Joshua Daniel (Reg No: 24BCE0436)<br/>2. M Saryu (Reg No: 24BCE2524)", STYLES['TD'])],
        [Paragraph("<b>Degree & Branch:</b>", STYLES['TDBold']), Paragraph(STUDENT_INFO["degree"], STYLES['TD'])],
        [Paragraph("<b>Subject:</b>", STYLES['TDBold']), Paragraph(STUDENT_INFO["subject"], STYLES['TD'])],
        [Paragraph("<b>Faculty Evaluator:</b>", STYLES['TDBold']), Paragraph(STUDENT_INFO["guide"], STYLES['TD'])],
        [Paragraph("<b>Database Platform:</b>", STYLES['TDBold']), Paragraph(STUDENT_INFO["db_platform"], STYLES['TD'])],
        [Paragraph("<b>PDB & Schema:</b>", STYLES['TDBold']), Paragraph(f"{STUDENT_INFO['container']} / {STUDENT_INFO['schema']}", STYLES['TD'])],
    ]
    t_meta = Table(meta_rows, colWidths=[150, 315])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1.0, C_NAVY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_meta)

    story.append(Spacer(1, 40))
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
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, C_LIGHT_BG])
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # =========================================================================
    # SECTION 2: ABSTRACT
    # =========================================================================
    story.append(Paragraph("2. Abstract", STYLES['H1']))
    story.append(Paragraph(
        "Modern digital banking ecosystems process tens of millions of financial transactions daily across "
        "Unified Payments Interface (UPI), Internet Net-Banking, Mobile Applications, Point-of-Sale (POS), "
        "and Automated Teller Machines (ATMs). High transactional velocity must coexist with rigorous Anti-Money "
        "Laundering (AML) controls and forensic accountability. <b>FraudLens: Financial Transaction and Fraud "
        "Investigation Management System</b> is a comprehensive academic relational database project designed to model financial "
        "movements, automate anomaly detection thresholds, dispatch triage alerts, and coordinate forensic case "
        "investigations within a fully auditable database architecture.",
        STYLES['Body']
    ))
    story.append(Paragraph(
        "A foundational design principle of FraudLens is the strict operational decoupling of automated alert "
        "signals from legal proof of fraud: an automated alert is an investigative trigger, not definitive proof of "
        "culpability. Built natively on Oracle AI Database 26ai Free Release 23.26.3.0.0 (container FREEPDB1), "
        "FraudLens implements 8 relational tables strictly normalized to Third Normal Form (3NF), 8 sequences, "
        "4 analytical surveillance views, 3 stored procedures, 3 stored functions, 2 database triggers, and 71 integrity "
        "constraints. An automated 13-case test harness verified the expected operational workflows and constraint "
        "rejections across the documented execution run with a 13/13 (100%) recorded pass rate, validating baseline "
        "functional integrity without claiming exhaustive verification.",
        STYLES['Body']
    ))
    story.append(make_callout(
        "Core Academic Takeaway",
        "FraudLens demonstrates that transactional integrity (ACID properties), business rule enforcement, and forensic "
        "auditing can be maintained directly inside the database tier through normalized relational modeling, "
        "declarative constraints, and PL/SQL procedural intelligence."
    ))

    # =========================================================================
    # SECTION 3: INTRODUCTION
    # =========================================================================
    story.append(Paragraph("3. Introduction", STYLES['H1']))
    story.append(Paragraph(
        "The exponential adoption of digital retail payments has transformed retail banking into a 24x7 real-time "
        "environment. While this enables frictionless payments, it exposes banking platforms to sophisticated cyber-threats, "
        "including authorized push payment fraud, credential stuffing, rapid account draining, smurfing (structuring), "
        "and unauthorized international cross-border transfers. Traditional flat-file logging and decentralized application "
        "logic fail to satisfy modern regulatory standards set by central banks and financial intelligence units.",
        STYLES['Body']
    ))
    story.append(Paragraph(
        "Database Management Systems (DBMS) serve as the bedrock of dependable financial platforms. Through structured "
        "schema design, ACID guarantees (Atomicity, Consistency, Isolation, Durability), and declarative integrity constraints, "
        "an enterprise RDBMS prevents double spending, guarantees balance veracity, and maintains auditable event trails. "
        "FraudLens models this end-to-end banking pipeline, bridging high-volume payment processing with forensic investigation "
        "management.",
        STYLES['Body']
    ))

    # =========================================================================
    # SECTION 4: PROBLEM STATEMENT
    # =========================================================================
    story.append(Paragraph("4. Problem Statement", STYLES['H1']))
    story.append(Paragraph("Contemporary commercial banking systems face four critical relational and operational dilemmas:", STYLES['Body']))
    story.append(Paragraph("• <b>High-Velocity Anomaly Detection:</b> Financial databases must process high-frequency transactions without incurring prohibitive latency, while simultaneously checking each event against surveillance thresholds.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Alert vs. Proof Distinction:</b> Automated rule engines produce false positives. Labeling a customer transaction as fraudulent without forensic validation causes unwarranted account freezes and reputational damage. Systems require structured hand-offs from automated signals to human compliance officers.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Caseworker Allocation & Lifecycle Tracking:</b> Surveillance alerts must be allocated to certified, active investigators according to specialization, tracking case lifecycle from initiation to final verdict.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Trigger-Based Forensic Auditability:</b> Financial regulations mandate that every state transition in a fraud investigation must be historically preserved with user session identification and precise timestamps.", STYLES['Bullet']))

    # =========================================================================
    # SECTION 5: OBJECTIVES OF THE PROJECT
    # =========================================================================
    story.append(Paragraph("5. Objectives of the Project", STYLES['H1']))
    story.append(Paragraph("• <b>1. Schema Normalization:</b> Design a normalized Third Normal Form (3NF) relational schema modeling customers, accounts, transactions, fraud alerts, investigators, and investigation cases.", STYLES['Bullet']))
    story.append(Paragraph("• <b>2. Declarative Integrity:</b> Enforce referential integrity, multi-column unique keys, and domain check constraints (amount > 0, balance >= 0, status domains) natively within Oracle Database.", STYLES['Bullet']))
    story.append(Paragraph("• <b>3. Procedural Automation:</b> Develop stored procedures for automated high-value surveillance (> INR 50,000 threshold), case allocation, and lifecycle state management.", STYLES['Bullet']))
    story.append(Paragraph("• <b>4. Analytical Intelligence:</b> Implement reusable stored functions for customer risk tier classification, transacted volume aggregation, and account alert counts.", STYLES['Bullet']))
    story.append(Paragraph("• <b>5. Data Abstraction & Views:</b> Construct database views providing real-time transaction surveillance, customer risk postures, and triage queues.", STYLES['Bullet']))
    story.append(Paragraph("• <b>6. Trigger-Based Audit Trails:</b> Build row-level database triggers that capture chronological audit event streams on investigation and alert state transitions.", STYLES['Bullet']))
    story.append(Paragraph("• <b>7. Empirical Verification:</b> Verify all DDL, DML, queries, and PL/SQL subprograms natively against Oracle AI Database 26ai Free.", STYLES['Bullet']))

    # =========================================================================
    # SECTION 6: EXISTING SYSTEM AND ITS LIMITATIONS
    # =========================================================================
    story.append(Paragraph("6. Existing System and Its Limitations", STYLES['H1']))
    story.append(Paragraph("In many traditional banking and legacy institutional setups, transaction tracking and fraud surveillance suffer from severe architectural shortcomings:", STYLES['Body']))
    story.append(Paragraph("• <b>Flat & Denormalized Ledgers:</b> Customer demographic information, account balances, and transaction logs are stored in loosely structured tables, leading to update anomalies and data redundancy.", STYLES['Bullet']))
    story.append(Paragraph("• <b>External Application Reliance:</b> Fraud detection logic is implemented purely in external application code, bypassing database-tier constraint enforcement.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Spreadsheet-Based Triage:</b> Compliance teams manually copy suspicious records into external spreadsheets, resulting in lost evidence, unassigned cases, and zero accountability.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Absence of Immutable Audit Logs:</b> Status modifications can be executed without leaving an audit trail, creating severe vulnerabilities to internal collusion and compliance penalties.", STYLES['Bullet']))

    # =========================================================================
    # SECTION 7: PROPOSED SYSTEM — FRAUDLENS
    # =========================================================================
    story.append(Paragraph("7. Proposed System — FraudLens", STYLES['H1']))
    story.append(Paragraph("FraudLens integrates transaction processing, surveillance rules, and caseworker management into a single cohesive, auditable Oracle Database architecture. Key innovations include:", STYLES['Body']))
    story.append(Paragraph("• <b>Decoupled 3-Tier Relational Model:</b> Explicit separation of customer identities, bank accounts, monetary movements, anomaly signals, and forensic cases.", STYLES['Bullet']))
    story.append(Paragraph("• <b>In-Database Anomaly Evaluation:</b> Transactions exceeding INR 50,000 or exhibiting suspicious channels automatically invoke stored procedures that generate fraud alert signals.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Rigorous Casework Dossier:</b> High-severity alerts are formally escalated into an investigation dossier, strictly assignable only to active, qualified investigators.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Autonomous Forensic Auditing:</b> Database triggers intercept every status change, logging previous/new states, database user credentials, and precise timestamps to dedicated audit tables.", STYLES['Bullet']))

    # =========================================================================
    # SECTION 8: SCOPE OF THE PROJECT
    # =========================================================================
    story.append(Paragraph("8. Scope of the Project", STYLES['H1']))
    story.append(Paragraph("The functional scope of FraudLens encompasses:", STYLES['Body']))
    story.append(Paragraph("• <b>Customer Management:</b> KYC status tracking (VERIFIED, PENDING, REJECTED) and baseline credit/fraud risk score management.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Account Administration:</b> Multi-account ownership per customer (Savings, Current, Salary, NRI) with non-negative balance checks.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Transaction Processing:</b> Financial debits, credits, transfers, and payments across Mobile App, Net Banking, ATM, POS, and UPI.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Surveillance & Alerting:</b> Threshold breaches (> INR 50k), velocity tracking, off-hour transactions, and smurfing detection.", STYLES['Bullet']))
    story.append(Paragraph("• <b>Investigation Management:</b> Casework assignment, status progression (OPEN -> UNDER REVIEW -> CLOSED), and definitive verdict enforcement.", STYLES['Bullet']))
    story.append(Paragraph("<b>Scope Boundaries:</b> Real-time distributed Kafka streaming, advanced machine-learning classification models, and multi-node graph databases are designated as future architectural enhancements.", STYLES['Body']))

    # =========================================================================
    # SECTION 9: SOFTWARE AND HARDWARE REQUIREMENTS
    # =========================================================================
    story.append(Paragraph("9. Software and Hardware Requirements", STYLES['H1']))
    story.append(Paragraph("9.1 Software Requirements", STYLES['H2']))
    story.append(Paragraph("• <b>Database Management System:</b> Oracle AI Database 26ai Free Release 23.26.3.0.0 (Container: FREEPDB1, Schema: FRAUDLENS_USER)", STYLES['Bullet']))
    story.append(Paragraph("• <b>Database Client Interfaces:</b> Oracle SQL*Plus 23.26.0.0.0 and Oracle SQL Developer 23.x / 24.x", STYLES['Bullet']))
    story.append(Paragraph("• <b>Database Languages:</b> Oracle SQL (DDL, DML, DQL) and Oracle PL/SQL (Procedures, Functions, Cursors, Triggers)", STYLES['Bullet']))
    story.append(Paragraph("• <b>Supporting Tools:</b> Python 3.10+ (reportlab, python-docx, Pillow) for offline validation and academic report generation", STYLES['Bullet']))
    story.append(Paragraph("• <b>Host Operating System:</b> Microsoft Windows 11 64-bit Professional", STYLES['Bullet']))

    story.append(Paragraph("9.2 Hardware Requirements", STYLES['H2']))
    story.append(Paragraph("• <b>Processor:</b> Intel Core i7 / AMD Ryzen 7 Multi-core Processor (x86_64 architecture)", STYLES['Bullet']))
    story.append(Paragraph("• <b>Primary Memory (RAM):</b> 16 GB RAM (minimum 8 GB dedicated to Oracle SGA/PGA pools)", STYLES['Bullet']))
    story.append(Paragraph("• <b>Secondary Storage:</b> 50 GB Solid State Drive (NVMe SSD recommended for redo logs and tablespaces)", STYLES['Bullet']))

    # =========================================================================
    # SECTION 10: SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("10. System Architecture", STYLES['H1']))
    story.append(Paragraph(
        "The FraudLens architecture is structured into four decoupled layers, providing clear separation between transactional "
        "ingestion, anomaly surveillance, caseworker management, and forensic audit logging. Figure 1 illustrates this end-to-end flow.",
        STYLES['Body']
    ))
    img_arch = make_scaled_image(os.path.join(assets_dir, "architecture_flow.png"), max_w=PRINT_W, max_h=240)
    if img_arch:
        story.append(img_arch)
        story.append(Paragraph("Figure 1: FraudLens End-to-End System Architecture Flow Diagram", STYLES['FigCap']))
    story.append(Paragraph(
        "<b>Architecture Flow Breakdown:</b><br/>"
        "1. <b>Ingestion Layer:</b> Banking clients initiate financial transactions across digital channels (Mobile App, UPI, Net-Banking, ATM, POS). "
        "Transactions are recorded in the TRANSACTIONS table with immediate ACID atomicity.<br/>"
        "2. <b>Surveillance & Rule Engine:</b> Stored procedure <code>SP_EVALUATE_AND_ALERT_TRANSACTION</code> is explicitly "
        "invoked via application logic, batch runs, or test harness calls (not via an automated table trigger). "
        "For transactions breaching threshold limits (> INR 50,000), it updates transaction status to FLAGGED and generates an alert in FRAUD_ALERT.<br/>"
        "3. <b>Investigation Subsystem:</b> Triage officers review unassigned alerts via VW_UNASSIGNED_ALERTS and open an INVESTIGATION case dossier. "
        "Procedure SP_ASSIGN_INVESTIGATOR validates investigator credentials and assigns lead responsibility.<br/>"
        "4. <b>Trigger-Based Audit Subsystem:</b> As investigations transition across lifecycle states, row-level database triggers intercept "
        "the UPDATE statement and write an automated snapshot to INVESTIGATION_AUDIT.",
        STYLES['Body']
    ))

    # =========================================================================
    # SECTION 11: ENTITY-RELATIONSHIP (ER) DIAGRAM
    # =========================================================================
    story.append(Paragraph("11. Entity-Relationship (ER) Diagram", STYLES['H1']))
    story.append(Paragraph(
        "The conceptual database design of FraudLens models 6 core entities and 2 supporting audit event streams. "
        "Figure 2 presents the complete Entity-Relationship diagram with primary keys, foreign keys, and cardinalities.",
        STYLES['Body']
    ))
    img_erd = make_scaled_image(os.path.join(assets_dir, "erd_diagram.png"), max_w=PRINT_W, max_h=300)
    if img_erd:
        story.append(img_erd)
        story.append(Paragraph("Figure 2: FraudLens Entity-Relationship (ER) Diagram (Oracle Data Modeler Standard)", STYLES['FigCap']))
    story.append(Paragraph(
        "<b>Entity Cardinality Specifications:</b><br/>"
        "• <b>CUSTOMER to ACCOUNT (1 : N):</b> One customer may own one or multiple bank accounts; each account belongs to exactly one customer.<br/>"
        "• <b>ACCOUNT to TRANSACTIONS (1 : N):</b> One account maintains multiple financial transaction records; each transaction debits/credits a single account.<br/>"
        "• <b>TRANSACTIONS to FRAUD_ALERT (1 : N):</b> A transaction can generate zero, one, or multiple fraud alerts across distinct surveillance rules.<br/>"
        "• <b>FRAUD_ALERT to INVESTIGATION (1 : 1):</b> Each formal investigation dossier corresponds uniquely to exactly one fraud alert (enforced via UNIQUE FK).<br/>"
        "• <b>INVESTIGATOR to INVESTIGATION (1 : N):</b> One forensic investigator manages multiple assigned investigation cases.<br/>"
        "• <b>INVESTIGATION to INVESTIGATION_AUDIT (1 : N):</b> Each investigation generates a chronological stream of audit records.",
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
        "and ensures that all functional dependencies adhere to relational theory.",
        STYLES['Body']
    ))
    story.append(Paragraph("13.1 First Normal Form (1NF)", STYLES['H2']))
    story.append(Paragraph(
        "A relation is in 1NF if and only if every attribute contains only atomic (indivisible) values, and there are no repeating "
        "groups or arrays. FraudLens satisfies 1NF because customer names are split into first_name and last_name, phone numbers "
        "are singular, and each table possesses an explicit single-column primary key.",
        STYLES['Body']
    ))
    story.append(Paragraph("13.2 Second Normal Form (2NF)", STYLES['H2']))
    story.append(Paragraph(
        "A relation is in 2NF if it is in 1NF and every non-prime attribute is fully functionally dependent on the primary key. "
        "Because all tables in FraudLens utilize single-column synthetic primary keys (e.g. customer_id, account_id), partial "
        "functional dependencies cannot exist mathematically.",
        STYLES['Body']
    ))
    story.append(Paragraph("13.3 Third Normal Form (3NF)", STYLES['H2']))
    story.append(Paragraph(
        "A relation is in 3NF if it is in 2NF and no non-prime attribute is transitively dependent on the candidate key. "
        "FraudLens satisfies 3NF by ensuring that non-key attributes depend strictly on the primary key. For example, customer demographic "
        "data is not stored in TRANSACTIONS, and investigator department details reside exclusively in INVESTIGATOR.",
        STYLES['Body']
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

        # Data Table
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
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, C_LIGHT_BG])
        ]))
        t_story.append(t_col)
        t_story.append(Spacer(1, 6))
        story.append(KeepTogether(t_story))

    # =========================================================================
    # SECTION 15: BUSINESS RULES AND CONSTRAINTS
    # =========================================================================
    story.append(Paragraph("15. Business Rules and Constraints", STYLES['H1']))
    story.append(Paragraph(
        "Data integrity in FraudLens is enforced declaratively through 71 constraints compiled in the Oracle data dictionary. "
        "Table 1 inventories all verified database objects.",
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
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, C_LIGHT_BG])
    ]))
    story.append(t_inv)
    story.append(Paragraph("Table 1: FraudLens Database Object Inventory Verified in Oracle AI Database 26ai", STYLES['FigCap']))

    # =========================================================================
    # SECTION 16: SQL IMPLEMENTATION
    # =========================================================================
    story.append(Paragraph("16. SQL Implementation", STYLES['H1']))
    story.append(Paragraph(
        "The project follows a modular, numbered architecture designed for clean execution order. Master driver script "
        "00_run_all.sql compiles and verifies all modules:",
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
        "Script 02_ddl_dml_demos.sql validates data definition statements (ALTER, ADD, DROP, RENAME) and data manipulation "
        "operations within transaction boundaries (SAVEPOINT, ROLLBACK).",
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
        "FraudLens includes a rich library of analytical queries demonstrating single-row functions, multi-table joins, "
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
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
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
        "the acting database user, and precise timestamps into INVESTIGATION_AUDIT and ALERT_AUDIT.",
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

    # =========================================================================
    # SECTION 23: FRAUD DETECTION AND ALERT MANAGEMENT LOGIC
    # =========================================================================
    story.append(Paragraph("23. Fraud Detection and Alert Management Logic", STYLES['H1']))
    story.append(Paragraph(
        "FraudLens detects anomalies across six core rules: (1) HIGH_AMOUNT (> INR 50,000 threshold), "
        "(2) RAPID_VELOCITY (rapid successive account drains), (3) SUSPICIOUS_CHANNEL (inconsistent channels), "
        "(4) UNUSUAL_HOURS (midnight debits), (5) CROSS_BORDER (international foreign transfers), and "
        "(6) STRUCTURING (smurfing below regulatory limits).",
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
    img_flow = make_scaled_image(os.path.join(assets_dir, "workflow_lifecycle.png"), max_w=PRINT_W, max_h=200)
    if img_flow:
        story.append(img_flow)
        story.append(Paragraph("Figure 3: FraudLens Investigation Lifecycle and Forensic Workflow State Transition Diagram", STYLES['FigCap']))

    # =========================================================================
    # SECTION 25: TESTING METHODOLOGY AND TEST CASES
    # =========================================================================
    story.append(Paragraph("25. Testing Methodology and Test Cases", STYLES['H1']))
    story.append(Paragraph(
        "Table 2 documents the complete 13-case test harness executed natively against Oracle AI Database 26ai Free. "
        "The harness verified 100% of functional workflows and constraint rejections.",
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
    story.append(Paragraph("Table 2: FraudLens Automated Positive and Negative Test Case Verification Matrix", STYLES['FigCap']))

    # =========================================================================
    # SECTION 26: ACTUAL EXECUTION SCREENSHOTS AND SAMPLE OUTPUTS
    # =========================================================================
    story.append(PageBreak())
    story.append(Paragraph("26. Actual Execution Screenshots and Sample Outputs", STYLES['H1']))
    story.append(Paragraph(
        "All visual evidence below represents genuine console executions captured directly from Oracle SQL*Plus "
        "and Oracle SQL Developer in the active schema FRAUDLENS_USER on container FREEPDB1.",
        STYLES['Body']
    ))

    screenshots = [
        ("01_oracle_connection_and_pdb.png", "Figure 4: Oracle SQL*Plus Terminal Connection, Container FREEPDB1, and Schema FRAUDLENS_USER", 220),
        ("02_table_creation_and_list.png", "Figure 5: Table Creation and Data Dictionary Status Verification (USER_TABLES: All 8 Tables VALID)", 220),
        ("03_sample_data_row_counts.png", "Figure 6: Baseline Sample Dataset Record Counts (56 Total Operational Records Across 8 Tables)", 200),
        ("04_join_and_groupby_queries.png", "Figure 7: Execution of Multi-Table Relational Joins and Channel Aggregation (GROUP BY & HAVING)", 220),
        ("05_constraint_rejection_test.png", "Figure 8: Database Engine Blocking Check Constraint Violation (Negative Amount Rejected with ORA-02290)", 180),
        ("06_main_script_execution.png", "Figure 9: Master Test Pipeline Completion Banner — 100% Automated Test Suite Passing Status", 220),
        ("oracle_ss_q1.png", "Figure 10: Oracle SQL Developer Execution Grid — Single-Row Customer Normalization Functions", 220),
        ("oracle_ss_q4.png", "Figure 11: Oracle SQL Developer Master 6-Table Relational Dossier Output", 220),
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
        "• <b>Schema Integrity:</b> All 8 tables, 8 sequences, 4 views, 3 procedures, 3 functions, and 2 triggers compiled without errors.\n"
        "• <b>Constraint Robustness:</b> All 71 integrity constraints operated deterministically. Negative tests 2.1 through 2.6 proved that "
        "negative amounts, duplicate emails, orphan accounts, inactive investigator assignments, and incomplete closures are trapped.\n"
        "• <b>Transactional Control & Recovery:</b> Master test scripts executed with transactional savepoints and clean rollbacks, verifying that "
        "operational data integrity is preserved during negative test failure and batch pipeline execution.",
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

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[PDF] Generated report successfully: {output_pdf}")

if __name__ == "__main__":
    generate_pdf()
