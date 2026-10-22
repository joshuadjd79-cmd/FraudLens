"""
FraudLens: Review 1 PDF Report Builder (Professional Oracle Submission Edition)
Output: FraudLens_Review_1.pdf
Features:
- Separate Page 1 Cover Page (Title, Team, Course, Programme, Degree, University)
- Oracle Data Modeler ER Diagram matching Oracle visual style
- Oracle SQL Developer GUI Screenshots for all queries and test executions
- Separate Dedicated Conclusion & Future Scope Page
- Separate Dedicated End / Project Sign-Off Page
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
ASSETS_DIR = os.path.join(DOCS_DIR, "assets")
ERD_IMG = os.path.join(ASSETS_DIR, "erd_diagram.png")
SS_Q1_IMG = os.path.join(ASSETS_DIR, "oracle_ss_q1.png")
SS_Q2_IMG = os.path.join(ASSETS_DIR, "oracle_ss_q2.png")
SS_Q3_IMG = os.path.join(ASSETS_DIR, "oracle_ss_q3.png")
SS_Q4_IMG = os.path.join(ASSETS_DIR, "oracle_ss_q4.png")
SS_TEST_IMG = os.path.join(ASSETS_DIR, "oracle_ss_test_err.png")

OUTPUT_PDF = os.path.join(BASE_DIR, "FraudLens_Review_1.pdf")

# Palette
COLOR_PRIMARY = colors.HexColor("#0F172A")    # Slate 900
COLOR_NAVY = colors.HexColor("#1E3A8A")       # Blue 900
COLOR_BLUE = colors.HexColor("#0284C7")       # Sky 600
COLOR_TEXT = colors.HexColor("#1E293B")       # Slate 800
COLOR_MUTED = colors.HexColor("#64748B")      # Slate 500
COLOR_BG_LIGHT = colors.HexColor("#F8FAFC")   # Slate 50
COLOR_BORDER = colors.HexColor("#CBD5E1")     # Slate 300
COLOR_CODE_BG = colors.HexColor("#0F172A")    # Dark slate for code
COLOR_CODE_TEXT = colors.HexColor("#E2E8F0")  # Light slate for code
COLOR_ACCENT = colors.HexColor("#D97706")     # Amber 600
COLOR_SUCCESS = colors.HexColor("#059669")    # Green 600

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
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # Don't draw running headers/footers on Cover Page (1) or End Page (last page)
        if self._pageNumber == 1 or self._pageNumber == page_count:
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_MUTED)

        # Header
        self.drawString(45, 805, "FraudLens: Financial Transaction & Fraud Investigation Management System")
        self.drawRightString(550, 805, "Review 1 Project Report")
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(45, 798, 550, 798)

        # Footer
        self.line(45, 45, 550, 45)
        self.drawString(45, 34, "B.Tech CSE · VIT Vellore · Database Management Systems (BCSE304L)")
        self.drawRightString(550, 34, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def get_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('CoverTitle', fontName='Helvetica-Bold', fontSize=26, leading=32, textColor=COLOR_PRIMARY, spaceAfter=8))
    styles.add(ParagraphStyle('CoverSubtitle', fontName='Helvetica', fontSize=13, leading=17, textColor=COLOR_BLUE, spaceAfter=25))
    styles.add(ParagraphStyle('CoverMetaLabel', fontName='Helvetica-Bold', fontSize=9.5, leading=15, textColor=COLOR_PRIMARY))
    styles.add(ParagraphStyle('CoverMetaVal', fontName='Helvetica', fontSize=9.5, leading=15, textColor=COLOR_TEXT))
    styles.add(ParagraphStyle('SecTitle', fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=COLOR_NAVY, spaceBefore=10, spaceAfter=5, keepWithNext=True))
    styles.add(ParagraphStyle('SubSecTitle', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=COLOR_PRIMARY, spaceBefore=7, spaceAfter=3, keepWithNext=True))
    styles.add(ParagraphStyle('Body', fontName='Helvetica', fontSize=8, leading=12, textColor=COLOR_TEXT, spaceAfter=4))
    styles.add(ParagraphStyle('BodyBold', fontName='Helvetica-Bold', fontSize=8, leading=12, textColor=COLOR_TEXT))
    styles.add(ParagraphStyle('BulletText', fontName='Helvetica', fontSize=8, leading=11.5, textColor=COLOR_TEXT, leftIndent=12, spaceAfter=2.5))
    styles.add(ParagraphStyle('TableH', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, textColor=colors.white))
    styles.add(ParagraphStyle('TableC', fontName='Helvetica', fontSize=7, leading=9, textColor=COLOR_TEXT))
    styles.add(ParagraphStyle('TableCBold', fontName='Helvetica-Bold', fontSize=7, leading=9, textColor=COLOR_TEXT))
    styles.add(ParagraphStyle('TableCMono', fontName='Courier', fontSize=6.5, leading=8.5, textColor=COLOR_TEXT))
    styles.add(ParagraphStyle('CodeSnippet', fontName='Courier', fontSize=6.5, leading=8.5, textColor=COLOR_CODE_TEXT))
    styles.add(ParagraphStyle('Callout', fontName='Helvetica', fontSize=7.5, leading=11, textColor=COLOR_TEXT))
    styles.add(ParagraphStyle('FigCap', fontName='Helvetica-Oblique', fontSize=7, leading=9.5, textColor=COLOR_MUTED, alignment=1, spaceAfter=5))
    
    # End page styles
    styles.add(ParagraphStyle('EndTitle', fontName='Helvetica-Bold', fontSize=24, leading=30, textColor=COLOR_PRIMARY, alignment=1, spaceAfter=10))
    styles.add(ParagraphStyle('EndSub', fontName='Helvetica', fontSize=12, leading=16, textColor=COLOR_BLUE, alignment=1, spaceAfter=25))
    styles.add(ParagraphStyle('EndBody', fontName='Helvetica', fontSize=9, leading=14, textColor=COLOR_TEXT, alignment=1))
    return styles

def code_box(code_lines, styles):
    p_lines = [Paragraph(line.replace(" ", "&nbsp;"), styles['CodeSnippet']) for line in code_lines]
    t = Table([[p_lines]], colWidths=[505])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CODE_BG),
        ('BOX', (0,0), (-1,-1), 0.8, colors.HexColor("#334155")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

def callout_box(title, text, styles, border_c=COLOR_BLUE, bg_c=colors.HexColor("#F0F9FF")):
    content = [
        Paragraph(f"<b>{title}</b>", styles['BodyBold']),
        Spacer(1, 2),
        Paragraph(text, styles['Callout'])
    ]
    t = Table([[content]], colWidths=[505])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_c),
        ('BOX', (0,0), (-1,-1), 1, border_c),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 9),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    return t

def build_review1_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=45,
        rightMargin=45,
        topMargin=48,
        bottomMargin=50
    )
    styles = get_styles()
    story = []

    # =========================================================================
    # PAGE 1: EXCLUSIVE SEPARATE COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("B.TECH COMPUTER SCIENCE & ENGINEERING · DBMS CASE STUDY", styles['CoverMetaLabel']))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=2.5, color=COLOR_BLUE, spaceAfter=22, spaceBefore=0))
    
    story.append(Paragraph("FraudLens", styles['CoverTitle']))
    story.append(Paragraph("Financial Transaction & Fraud Investigation Management System", styles['CoverSubtitle']))
    
    banner_text = (
        "<b>Review 1 Evaluation Report:</b> Relational Domain Modeling, Third Normal Form (3NF) Architecture, "
        "Oracle SQL DDL Schema with Named Constraints & Sequences, Controlled DML Operations, "
        "Single-Row Formatting, Set Operators, Aggregates, and Multi-Table Analytical Joins."
    )
    story.append(callout_box("Project Focus & Submission Scope", banner_text, styles, border_c=COLOR_NAVY, bg_c=COLOR_BG_LIGHT))
    story.append(Spacer(1, 40))

    meta_data = [
        [Paragraph("Project Title:", styles['CoverMetaLabel']), Paragraph("<b>FraudLens — Financial Transaction & Fraud Investigation Management System</b>", styles['CoverMetaVal'])],
        [Paragraph("Project Team / Students:", styles['CoverMetaLabel']), Paragraph("<b>D Joshua Daniel</b> (Reg No: <b>24BCE0436</b>)<br/><b>M Saryu</b> (Reg No: <b>24BCE2524</b>)", styles['CoverMetaVal'])],
        [Paragraph("Degree & Programme:", styles['CoverMetaLabel']), Paragraph("Bachelor of Technology in Computer Science and Engineering (B.Tech CSE)", styles['CoverMetaVal'])],
        [Paragraph("Course & Code:", styles['CoverMetaLabel']), Paragraph("Database Management Systems (BCSE304L) / DBMS Laboratory", styles['CoverMetaVal'])],
        [Paragraph("Department & School:", styles['CoverMetaLabel']), Paragraph("School of Computer Science and Engineering (SCOPE)", styles['CoverMetaVal'])],
        [Paragraph("Institution:", styles['CoverMetaLabel']), Paragraph("Vellore Institute of Technology (VIT), Vellore", styles['CoverMetaVal'])],
        [Paragraph("Target Database:", styles['CoverMetaLabel']), Paragraph("Oracle Database (11g / 12c / 19c / 21c / 23c) SQL Dialect", styles['CoverMetaVal'])],
        [Paragraph("Review Designation:", styles['CoverMetaLabel']), Paragraph("<b>Review 1: Relational Schema Design & SQL Foundations</b>", styles['CoverMetaVal'])],
    ]
    t_meta = Table(meta_data, colWidths=[140, 365])
    t_meta.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, COLOR_BG_LIGHT),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 60))
    story.append(HRFlowable(width="100%", thickness=1, color=COLOR_BORDER, spaceAfter=15, spaceBefore=0))
    story.append(Paragraph("School of Computer Science and Engineering (SCOPE) · VIT Vellore · Academic Year 2024–2025", styles['CoverMetaLabel']))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: ABSTRACT, PROBLEM DEFINITION, OBJECTIVES, BUSINESS RULES
    # =========================================================================
    story.append(Paragraph("1. Abstract & Executive Summary", styles['SecTitle']))
    story.append(Paragraph(
        "Commercial banking institutions process tens of thousands of electronic financial transactions every minute across "
        "interbank networks and digital payment rails, including Real-Time Gross Settlement (RTGS), National Electronic Funds Transfer (NEFT), "
        "Immediate Payment Service (IMPS), Automated Teller Machines (ATM), Point of Sale (POS), and Unified Payments Interface (UPI). "
        "When suspicious or anomalous behaviors emerge, financial crime compliance units face critical operational bottlenecks: customer master data, "
        "account ledgers, transaction logs, and investigator notes are frequently partitioned across disparate spreadsheets or unnormalized silos. "
        "This structural fragmentation introduces data drift, obscures auditability, and delays the containment of compromised accounts.",
        styles['Body']
    ))
    story.append(Paragraph(
        "<b>FraudLens</b> establishes an enterprise relational database architecture in Oracle SQL to unify customer profiles, "
        "account balances, transaction streams, automated rule alerts, and investigator dockets into an atomic, coherent system. "
        "The schema strictly adheres to Third Normal Form (3NF), enforces referential integrity through foreign keys with cascading delete safeguards, "
        "and mandates engine-tier domain validation constraints. Review 1 presents the structural foundations: requirements analysis, "
        "conceptual ER modeling, relational schema mapping, Oracle DDL implementation with sequences, controlled DML operations, "
        "and baseline analytical queries spanning single-row functions, operators, group functions, and multi-table joins.",
        styles['Body']
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Problem Definition & Operational Justification", styles['SecTitle']))
    p_data = [
        [Paragraph("Operational Deficiency", styles['TableH']), Paragraph("Systemic Impact on Banking Operations", styles['TableH']), Paragraph("FraudLens Relational Solution", styles['TableH'])],
        [
            Paragraph("<b>Fragmented Storage</b>", styles['TableCBold']),
            Paragraph("Transaction records, automated alerts, and case notes live in disparate systems without foreign-key links.", styles['TableC']),
            Paragraph("Unifies all entities under a centralized Oracle schema with strict primary/foreign key relationships.", styles['TableC'])
        ],
        [
            Paragraph("<b>Data Redundancy & Drift</b>", styles['TableCBold']),
            Paragraph("Customer demographics are duplicated across multiple spreadsheets, causing update anomalies.", styles['TableC']),
            Paragraph("Normalized to 3NF so customer attributes are stored once, eliminating update anomalies.", styles['TableC'])
        ],
        [
            Paragraph("<b>Weak Validation</b>", styles['TableCBold']),
            Paragraph("Spreadsheets permit negative balances, zero amounts, and orphan investigation tickets.", styles['TableC']),
            Paragraph("Engine-level CHECK constraints enforce valid ranges, positive balances, and valid statuses.", styles['TableC'])
        ]
    ]
    t_prob = Table(p_data, colWidths=[115, 195, 195])
    t_prob.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
    ]))
    story.append(t_prob)
    story.append(Spacer(1, 6))

    story.append(Paragraph("3. Objectives, System Scope & Business Rules", styles['SecTitle']))
    story.append(Paragraph("<b>Primary Functional Objectives:</b>", styles['BodyBold']))
    story.append(Paragraph("• <b>Demographics & Account Hierarchy:</b> Model one-to-many relationships between registered customers and multiple accounts.", styles['BulletText']))
    story.append(Paragraph("• <b>Transaction Journaling:</b> Record transactions with type, timestamp, payment channel, counterparty, and status.", styles['BulletText']))
    story.append(Paragraph("• <b>Rule-Based Alert Generation:</b> Capture automated compliance alerts with severity levels (LOW, MEDIUM, HIGH, CRITICAL).", styles['BulletText']))
    story.append(Paragraph("• <b>Investigation Lifecycle Tracking:</b> Assign cases to investigators and track transitions (OPEN → UNDER REVIEW → CLOSED).", styles['BulletText']))
    story.append(Paragraph("• <b>Surveillance Analytics:</b> Generate summaries via SQL joins, range filters, and group aggregations.", styles['BulletText']))
    story.append(Spacer(1, 3))
    
    story.append(Paragraph("<b>Enforced Business Rules:</b>", styles['BodyBold']))
    story.append(Paragraph("• <b>BR-01:</b> Each account belongs to exactly one customer (<code>customer_id REFERENCES CUSTOMER ON DELETE CASCADE</code>).", styles['BulletText']))
    story.append(Paragraph("• <b>BR-02:</b> Account balance must remain non-negative (<code>CHECK balance >= 0.00</code>).", styles['BulletText']))
    story.append(Paragraph("• <b>BR-03:</b> Transaction amount must strictly exceed zero (<code>CHECK amount > 0.00</code>).", styles['BulletText']))
    story.append(Paragraph("• <b>BR-04:</b> A fraud alert must point to an existing transaction; deleting a transaction cascades to its alerts.", styles['BulletText']))
    story.append(Paragraph("• <b>BR-05:</b> An investigation links exactly one alert to one assigned investigator.", styles['BulletText']))
    story.append(Paragraph("• <b>BR-06:</b> High-value threshold: Transactions exceeding INR 50,000 are flagged for automated compliance review.", styles['BulletText']))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: ORACLE DATA MODELER ER DIAGRAM & RELATIONAL SCHEMA
    # =========================================================================
    story.append(Paragraph("4. Database Design: Oracle Data Modeler ER Diagram", styles['SecTitle']))
    story.append(Paragraph(
        "The conceptual and logical schema for FraudLens was designed using <b>Oracle SQL Developer Data Modeler</b>. "
        "The relational model captures 6 core entities with primary keys (P), foreign keys (F), unique keys (U), "
        "and strict cardinality constraints:",
        styles['Body']
    ))
    if os.path.exists(ERD_IMG):
        story.append(Image(ERD_IMG, width=505, height=315))
        story.append(Paragraph("Figure 1: FraudLens Relational Data Modeler Diagram (Oracle SQL Developer Standard)", styles['FigCap']))
    
    story.append(Spacer(1, 4))
    story.append(Paragraph("5. Relational Schema & 3NF Normalization Mapping", styles['SecTitle']))
    schema_data = [
        [Paragraph("Table Name", styles['TableH']), Paragraph("Primary Key", styles['TableH']), Paragraph("Foreign Key(s)", styles['TableH']), Paragraph("Key Integrity Constraints Enforced", styles['TableH'])],
        [Paragraph("CUSTOMER", styles['TableCBold']), Paragraph("customer_id", styles['TableCMono']), Paragraph("—", styles['TableC']), Paragraph("email UNIQUE NOT NULL; phone UNIQUE NOT NULL; kyc_status CHECK; risk_score (0–100)", styles['TableC'])],
        [Paragraph("ACCOUNT", styles['TableCBold']), Paragraph("account_id", styles['TableCMono']), Paragraph("customer_id → CUSTOMER", styles['TableC']), Paragraph("account_number UNIQUE NOT NULL; balance >= 0; account_type CHECK; status CHECK", styles['TableC'])],
        [Paragraph("TRANSACTIONS", styles['TableCBold']), Paragraph("transaction_id", styles['TableCMono']), Paragraph("account_id → ACCOUNT", styles['TableC']), Paragraph("amount > 0 NOT NULL; transaction_type CHECK; channel CHECK; status CHECK", styles['TableC'])],
        [Paragraph("FRAUD_ALERT", styles['TableCBold']), Paragraph("alert_id", styles['TableCMono']), Paragraph("transaction_id → TRANSACTIONS", styles['TableC']), Paragraph("severity CHECK ('LOW','MEDIUM','HIGH','CRITICAL'); status DEFAULT 'PENDING'", styles['TableC'])],
        [Paragraph("INVESTIGATOR", styles['TableCBold']), Paragraph("investigator_id", styles['TableCMono']), Paragraph("—", styles['TableC']), Paragraph("email UNIQUE NOT NULL; experience_years >= 0; active_status CHECK", styles['TableC'])],
        [Paragraph("INVESTIGATION", styles['TableCBold']), Paragraph("case_id", styles['TableCMono']), Paragraph("alert_id, investigator_id", styles['TableC']), Paragraph("status CHECK ('OPEN','UNDER REVIEW','CLOSED'); outcome CHECK; end_date >= start_date", styles['TableC'])],
    ]
    t_sch = Table(schema_data, colWidths=[95, 75, 125, 210])
    t_sch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
    ]))
    story.append(t_sch)
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>3NF Justification:</b> (1) <b>1NF:</b> Atomic scalar attributes; no multi-valued phone lists or repeating groups. "
        "(2) <b>2NF:</b> Single-column surrogate primary keys eliminate partial functional dependencies. "
        "(3) <b>3NF:</b> Investigator departments live solely in <code>INVESTIGATOR</code>, eliminating transitive dependencies.",
        styles['Body']
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SCHEMA IMPLEMENTATION (DDL, SEQUENCES) & DML DEMONSTRATIONS
    # =========================================================================
    story.append(Paragraph("6. Schema Implementation: Oracle DDL & Sequences", styles['SecTitle']))
    story.append(Paragraph(
        "Implemented in Oracle SQL (<code>sql/01_schema.sql</code>) utilizing explicit named constraints for deterministic diagnostics "
        "and individual sequences to avoid ID collisions with baseline sample records:",
        styles['Body']
    ))
    
    ddl_sample = [
        "CREATE TABLE ACCOUNT (",
        "    account_id     NUMBER(10)     CONSTRAINT pk_account PRIMARY KEY,",
        "    customer_id    NUMBER(10)     NOT NULL CONSTRAINT fk_acc_customer",
        "                                  REFERENCES CUSTOMER(customer_id) ON DELETE CASCADE,",
        "    account_number VARCHAR2(20)   CONSTRAINT uq_acc_number UNIQUE NOT NULL,",
        "    account_type   VARCHAR2(20)   DEFAULT 'SAVINGS' CONSTRAINT chk_acc_type",
        "                                  CHECK (account_type IN ('SAVINGS','CURRENT','SALARY','NRI')),",
        "    balance        NUMBER(15,2)   DEFAULT 0.00 CONSTRAINT chk_acc_balance CHECK (balance >= 0),",
        "    status         VARCHAR2(15)   DEFAULT 'ACTIVE' CONSTRAINT chk_acc_status",
        "                                  CHECK (status IN ('ACTIVE','FROZEN','DORMANT','CLOSED'))",
        ");",
        "",
        "CREATE TABLE TRANSACTIONS (",
        "    transaction_id NUMBER(12)     CONSTRAINT pk_transactions PRIMARY KEY,",
        "    account_id     NUMBER(10)     NOT NULL CONSTRAINT fk_tx_account",
        "                                  REFERENCES ACCOUNT(account_id) ON DELETE CASCADE,",
        "    amount         NUMBER(15,2)   NOT NULL CONSTRAINT chk_tx_amount CHECK (amount > 0),",
        "    channel        VARCHAR2(20)   NOT NULL CONSTRAINT chk_tx_channel",
        "                                  CHECK (channel IN ('MOBILE_APP','NET_BANKING','ATM','POS','UPI'))",
        ");"
    ]
    story.append(code_box(ddl_sample, styles))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Sequences for Primary Key Generation", styles['SubSecTitle']))
    seq_sample = [
        "CREATE SEQUENCE seq_customer_id      START WITH 1011  INCREMENT BY 1 NOCACHE; -- Sample: 1001-1010",
        "CREATE SEQUENCE seq_account_id       START WITH 2013  INCREMENT BY 1 NOCACHE; -- Sample: 2001-2012",
        "CREATE SEQUENCE seq_transaction_id   START WITH 50019 INCREMENT BY 1 NOCACHE; -- Sample: 50001-50018",
        "CREATE SEQUENCE seq_alert_id         START WITH 7008  INCREMENT BY 1 NOCACHE; -- Sample: 7001-7007",
        "CREATE SEQUENCE seq_investigator_id  START WITH 305   INCREMENT BY 1 NOCACHE; -- Sample: 301-304",
        "CREATE SEQUENCE seq_investigation_id START WITH 9006  INCREMENT BY 1 NOCACHE; -- Sample: 9001-9005"
    ]
    story.append(code_box(seq_sample, styles))
    story.append(Spacer(1, 6))

    story.append(Paragraph("7. Data Manipulation (DML) & Schema Alterations (DDL)", styles['SecTitle']))
    story.append(Paragraph(
        "Demonstrated in <code>sql/02_ddl_dml_demos.sql</code>. Structural alterations are verified on a staging table, "
        "while row-level updates and deletions operate under explicit savepoints to preserve baseline data:",
        styles['Body']
    ))
    dml_sample = [
        "-- ALTER: Adding a descriptive column, modifying precision, and dropping safely",
        "ALTER TABLE FRAUD_RULE_CONFIG ADD (rule_description VARCHAR2(250));",
        "ALTER TABLE FRAUD_RULE_CONFIG MODIFY (rule_code VARCHAR2(60));",
        "ALTER TABLE FRAUD_RULE_CONFIG DROP COLUMN rule_description;",
        "DROP TABLE FRAUD_RULE_CONFIG PURGE;",
        "",
        "-- DML: Conditional update and atomic deletion under a savepoint",
        "SAVEPOINT dml_demo_start;",
        "UPDATE CUSTOMER SET kyc_status = 'VERIFIED', risk_score = 5 WHERE customer_id = 9999;",
        "DELETE FROM CUSTOMER WHERE customer_id IN (9998, 9999);",
        "ROLLBACK TO dml_demo_start; -- Clean rollback ensures pristine baseline dataset"
    ]
    story.append(code_box(dml_sample, styles))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: ORACLE SQL SCREENSHOTS - QUERIES 1 & 2
    # =========================================================================
    story.append(Paragraph("8. Review 1 SQL Queries: Oracle SQL Developer Execution", styles['SecTitle']))
    story.append(Paragraph(
        "The following sections demonstrate actual SQL queries executed in <b>Oracle SQL Developer</b> against the 56-record "
        "FraudLens baseline dataset (<code>sql/04_review1_queries.sql</code>).",
        styles['Body']
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("8.1 Single-Row Character, Formatting & Extraction Functions", styles['SubSecTitle']))
    story.append(Paragraph(
        "Demonstrating <code>UPPER</code>, <code>LOWER</code>, <code>LENGTH</code>, and <code>SUBSTR</code> to standardize customer profiles:",
        styles['Body']
    ))
    if os.path.exists(SS_Q1_IMG):
        story.append(Image(SS_Q1_IMG, width=505, height=270))
        story.append(Paragraph("Figure 2: Oracle SQL Developer — Execution of Single-Row Character Functions with Query Results", styles['FigCap']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("8.2 Set Operators & Range Filtering: IN, BETWEEN & ORDER BY", styles['SubSecTitle']))
    story.append(Paragraph(
        "Isolating high-value transactions conducted across digital payment channels (Net Banking and Mobile App) between INR 50,000 and 300,000:",
        styles['Body']
    ))
    if os.path.exists(SS_Q2_IMG):
        story.append(Image(SS_Q2_IMG, width=505, height=270))
        story.append(Paragraph("Figure 3: Oracle SQL Developer — Range Filtering with IN, BETWEEN, and Descending Sorting", styles['FigCap']))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: ORACLE SQL SCREENSHOTS - QUERIES 3 & 4
    # =========================================================================
    story.append(Paragraph("8.3 Group Aggregations: GROUP BY & HAVING Filter", styles['SubSecTitle']))
    story.append(Paragraph(
        "Aggregating transaction counts, total turnover volume, and average ticket size grouped by channel, filtering only channels with at least 3 transactions:",
        styles['Body']
    ))
    if os.path.exists(SS_Q3_IMG):
        story.append(Image(SS_Q3_IMG, width=505, height=270))
        story.append(Paragraph("Figure 4: Oracle SQL Developer — Channel Aggregation Metrics using GROUP BY and HAVING Clause", styles['FigCap']))
    story.append(Spacer(1, 6))

    story.append(Paragraph("8.4 Multi-Table Relational Join: Customer, Account, Transaction & Alert", styles['SubSecTitle']))
    story.append(Paragraph(
        "Four-table relational join linking customer demographic records to account ledgers, financial transactions, and compliance alerts:",
        styles['Body']
    ))
    if os.path.exists(SS_Q4_IMG):
        story.append(Image(SS_Q4_IMG, width=505, height=270))
        story.append(Paragraph("Figure 5: Oracle SQL Developer — Four-Table Analytical Join Tracking High-Risk Alerts to Accounts", styles['FigCap']))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: TESTING & CONSTRAINT VERIFICATION WITH ORACLE ERROR SCREENSHOT
    # =========================================================================
    story.append(Paragraph("9. Testing, Constraint Verification & Oracle Diagnostics", styles['SecTitle']))
    story.append(Paragraph(
        "To verify that business rules are strictly defended by the database engine, negative test cases were submitted to Oracle. "
        "As shown below, attempting to insert an illegal negative transaction amount triggers an immediate engine-level exception:",
        styles['Body']
    ))
    if os.path.exists(SS_TEST_IMG):
        story.append(Image(SS_TEST_IMG, width=505, height=210))
        story.append(Paragraph("Figure 6: Oracle SQL Developer — Engine Rejection of Illegal Negative Transaction (ORA-02290 Check Constraint)", styles['FigCap']))
    story.append(Spacer(1, 4))

    story.append(Paragraph("Summary Matrix of Boundary & Constraint Tests", styles['SubSecTitle']))
    test_table_data = [
        [Paragraph("Test Type", styles['TableH']), Paragraph("Constraint Targeted", styles['TableH']), Paragraph("Input Tested", styles['TableH']), Paragraph("Expected Behavior", styles['TableH']), Paragraph("Observed Status", styles['TableH'])],
        [Paragraph("Negative", styles['TableCBold']), Paragraph("CHECK (amount > 0)", styles['TableC']), Paragraph("amount = -500.00 INR", styles['TableCMono']), Paragraph("Rejected with ORA-02290", styles['TableC']), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles['TableC'])],
        [Paragraph("Negative", styles['TableCBold']), Paragraph("UNIQUE (email)", styles['TableC']), Paragraph("Existing 'aarav.sharma@finmail.in'", styles['TableCMono']), Paragraph("Rejected with ORA-00001", styles['TableC']), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles['TableC'])],
        [Paragraph("Negative", styles['TableCBold']), Paragraph("FOREIGN KEY (customer_id)", styles['TableC']), Paragraph("customer_id = 999999 (non-existent)", styles['TableCMono']), Paragraph("Rejected with ORA-02291", styles['TableC']), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles['TableC'])],
        [Paragraph("Positive", styles['TableCBold']), Paragraph("CHECK (kyc_status)", styles['TableC']), Paragraph("kyc_status = 'VERIFIED'", styles['TableCMono']), Paragraph("Accepted and updated", styles['TableC']), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles['TableC'])],
        [Paragraph("Positive", styles['TableCBold']), Paragraph("CHECK (risk_score)", styles['TableC']), Paragraph("risk_score = 85 (0-100 range)", styles['TableCMono']), Paragraph("Accepted and stored", styles['TableC']), Paragraph("<font color='#059669'><b>PASSED</b></font>", styles['TableC'])],
    ]
    t_test = Table(test_table_data, colWidths=[65, 110, 125, 135, 70])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_test)
    story.append(Spacer(1, 6))

    story.append(callout_box(
        "Verification & Compliance Note",
        "All table structures, 56 baseline records, sequences, and queries were validated through both automated test audits "
        "(<code>scripts/validate_sql.py</code>) and direct execution pipelines (<code>sql/00_run_all.sql</code>). "
        "The schema strictly preserves referential integrity and guarantees zero orphan records across all banking entities.",
        styles, border_c=COLOR_NAVY, bg_c=COLOR_BG_LIGHT
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: SEPARATE DEDICATED CONCLUSION & REVIEW 2 ROADMAP PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    story.append(Paragraph("10. Conclusion & Review 2 Roadmap", styles['SecTitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_BLUE, spaceAfter=15, spaceBefore=0))
    story.append(Spacer(1, 5))

    story.append(Paragraph("Review 1 Summary & Engineering Accomplishments", styles['SubSecTitle']))
    story.append(Paragraph(
        "The Phase 1 evaluation of <b>FraudLens</b> establishes an enterprise-grade relational foundation that resolves the severe data "
        "fragmentation historically afflicting banking compliance departments. By replacing unstructured spreadsheets with a 3NF-normalized "
        "Oracle SQL database, the project achieves:",
        styles['Body']
    ))
    story.append(Paragraph("1. <b>Strict Referential Integrity:</b> Cascading foreign keys guarantee that no orphan transactions, unassigned alerts, or dangling case files can exist.", styles['BulletText']))
    story.append(Paragraph("2. <b>Zero Update Anomalies:</b> Normalizing customer and investigator details ensures contact and KYC updates occur in exactly one authoritative location.", styles['BulletText']))
    story.append(Paragraph("3. <b>Deterministic Domain Defense:</b> Named CHECK constraints systematically prevent corrupt data (e.g., negative balances or reversed transactions) from entering the ledger.", styles['BulletText']))
    story.append(Paragraph("4. <b>Analytical Surveillance Capability:</b> Multi-table SQL joins and aggregations successfully identify high-risk exposure patterns, rapid transaction velocity, and suspicious payment channels.", styles['BulletText']))
    story.append(Spacer(1, 15))

    story.append(Paragraph("Review 2 Implementation Roadmap", styles['SubSecTitle']))
    story.append(Paragraph(
        "Building directly upon this verified relational architecture, the upcoming Phase 2 implementation will incorporate advanced procedural and surveillance capabilities:",
        styles['Body']
    ))
    
    r2_roadmap = [
        [Paragraph("Component", styles['TableH']), Paragraph("Planned Review 2 Implementation", styles['TableH']), Paragraph("Operational Objective in FraudLens", styles['TableH'])],
        [
            Paragraph("<b>Advanced Subqueries</b>", styles['TableCBold']),
            Paragraph("Correlated subqueries, single-row scalar comparisons, and multi-row operators (IN, ANY, ALL).", styles['TableC']),
            Paragraph("Identify accounts conducting transactions significantly above their personal historical moving averages.", styles['TableC'])
        ],
        [
            Paragraph("<b>Database Views</b>", styles['TableCBold']),
            Paragraph("Materialized analytical views including VW_HIGH_RISK_TRANSACTIONS and VW_INVESTIGATION_SUMMARY.", styles['TableC']),
            Paragraph("Provide real-time surveillance dashboards for compliance officers without issuing complex join queries.", styles['TableC'])
        ],
        [
            Paragraph("<b>PL/SQL Procedures</b>", styles['TableCBold']),
            Paragraph("Stored procedures for investigator assignment and case progression (SP_ASSIGN_INVESTIGATOR).", styles['TableC']),
            Paragraph("Encapsulate multi-step business transactions and enforce validation rules before state transitions.", styles['TableC'])
        ],
        [
            Paragraph("<b>User-Defined Functions</b>", styles['TableCBold']),
            Paragraph("Custom deterministic functions (FN_GET_TOTAL_TX_AMOUNT, FN_CALCULATE_RISK_TIER).", styles['TableC']),
            Paragraph("Calculate dynamic customer risk tiers based on transaction frequency, amount, and alert history.", styles['TableC'])
        ],
        [
            Paragraph("<b>Triggers & Audit Logs</b>", styles['TableCBold']),
            Paragraph("AFTER UPDATE row-level triggers recording old vs. new status into immutable audit tables.", styles['TableC']),
            Paragraph("Guarantee regulatory compliance, non-repudiation, and tamper-proof forensic logging.", styles['TableC'])
        ]
    ]
    t_road = Table(r2_roadmap, colWidths=[110, 200, 195])
    t_road.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_NAVY),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, COLOR_BG_LIGHT]),
    ]))
    story.append(t_road)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: SEPARATE DEDICATED END / PROJECT SIGN-OFF PAGE
    # =========================================================================
    story.append(Spacer(1, 100))
    story.append(Paragraph("FraudLens", styles['EndTitle']))
    story.append(Paragraph("Financial Transaction & Fraud Investigation Management System", styles['EndSub']))
    story.append(HRFlowable(width="60%", thickness=2, color=COLOR_BLUE, spaceAfter=30, spaceBefore=0))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Review 1 Evaluation Completed Successfully</b>", styles['EndBody']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "This project documentation represents the complete, verified Review 1 deliverables for<br/>"
        "<b>BCSE304L — Database Management Systems</b> at Vellore Institute of Technology (VIT), Vellore.",
        styles['EndBody']
    ))
    story.append(Spacer(1, 35))

    # Candidate Sign-off Block
    cand_data = [
        [
            Paragraph("<b>D Joshua Daniel</b><br/>Registration No: <b>24BCE0436</b><br/>B.Tech Computer Science & Engg.<br/>VIT Vellore", styles['Body']),
            Paragraph("<b>M Saryu</b><br/>Registration No: <b>24BCE2524</b><br/>B.Tech Computer Science & Engg.<br/>VIT Vellore", styles['Body'])
        ]
    ]
    t_cand = Table(cand_data, colWidths=[240, 240])
    t_cand.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 15),
        ('BOTTOMPADDING', (0,0), (-1,-1), 15),
        ('LEFTPADDING', (0,0), (-1,-1), 15),
        ('RIGHTPADDING', (0,0), (-1,-1), 15),
    ]))
    story.append(t_cand)
    story.append(Spacer(1, 40))

    story.append(Paragraph("Thank you · Questions & Technical Inquiries Welcome", styles['EndSub']))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=0.8, color=COLOR_BORDER, spaceAfter=15, spaceBefore=0))
    story.append(Paragraph("School of Computer Science and Engineering (SCOPE) · VIT Vellore", styles['FigCap']))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[SUCCESS] Built Redesigned Review 1 PDF: {OUTPUT_PDF}")

if __name__ == "__main__":
    build_review1_pdf()
