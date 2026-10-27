"""
FraudLens: Generate Complete DOCX Case Study Report
Generates FraudLens_DBMS_Case_Study_Report.docx with all 31 academic sections,
tables, formatted code blocks, callouts, and embedded figures.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from report_content import (
    STUDENT_INFO, TEST_CASES, DB_INVENTORY, TABLE_DEFINITIONS
)

COLOR_NAVY = RGBColor(0x1E, 0x3A, 0x8A)      # Primary #1E3A8A
COLOR_SLATE = RGBColor(0x0F, 0x17, 0x2A)     # Dark Slate #0F172A
COLOR_BLUE = RGBColor(0x02, 0x84, 0xC7)      # Slate Blue #0284C7
COLOR_TEXT = RGBColor(0x1E, 0x29, 0x3B)      # Body text
COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)     # Muted text
COLOR_CODE = RGBColor(0x0F, 0x17, 0x2A)      # Code text

NAVY_HEX = "1E3A8A"
LIGHT_BG_HEX = "F8FAFC"
CODE_BG_HEX = "0F172A"
CALLOUT_BG_HEX = "F0F9FF"
BORDER_HEX = "CBD5E1"
CALLOUT_BORDER_HEX = "0284C7"

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_callout(doc, title, text, border_color=CALLOUT_BORDER_HEX, bg_color=CALLOUT_BG_HEX):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>'
        f'<w:top w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    run_t = p.add_run(f"{title}: ")
    run_t.bold = True
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = COLOR_NAVY

    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = COLOR_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, CODE_BG_HEX)
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)

    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="334155"/>'
        f'<w:left w:val="single" w:sz="6" w:space="0" w:color="334155"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="334155"/>'
        f'<w:right w:val="single" w:sz="6" w:space="0" w:color="334155"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_str.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0xEA, 0xE8, 0xE8)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def format_table(tbl, col_widths, headers, data, is_small=False):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    # Header Row
    hdr_cells = tbl.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_background(hdr_cells[i], NAVY_HEX)
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(8.5 if is_small else 9)
            run.bold = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    # Data Rows
    for row_idx, row_data in enumerate(data):
        row_cells = tbl.add_row().cells
        bg = LIGHT_BG_HEX if row_idx % 2 == 1 else "FFFFFF"
        for i, val in enumerate(row_data):
            row_cells[i].text = str(val)
            set_cell_background(row_cells[i], bg)
            set_cell_margins(row_cells[i], top=60, bottom=60, left=100, right=100)
            p = row_cells[i].paragraphs[0]
            for run in p.runs:
                run.font.name = "Calibri"
                run.font.size = Pt(8 if is_small else 8.5)
                run.font.color.rgb = COLOR_TEXT

    # Apply Column Widths
    for row in tbl.rows:
        for idx, w in enumerate(col_widths):
            row.cells[idx].width = Inches(w)

def add_heading_1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(16)
    run.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_heading_2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(13)
    run.bold = True
    run.font.color.rgb = COLOR_BLUE
    return p

def add_heading_3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.bold = True
    run.font.color.rgb = COLOR_SLATE
    return p

def add_body(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(10)
    run.font.color.rgb = COLOR_TEXT
    return p

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(9.5)
        r_pre.font.color.rgb = COLOR_SLATE
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(9.5)
    run.font.color.rgb = COLOR_TEXT
    return p

def add_image_figure(doc, img_path, caption, width_in=6.0):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(2)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Inches(width_in))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(8)
        run_cap = p_cap.add_run(caption)
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(8.5)
        run_cap.italic = True
        run_cap.font.color.rgb = COLOR_MUTED
    else:
        p_ph = doc.add_paragraph()
        p_ph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p_ph.add_run(f"[FIGURE PLACEHOLDER: {caption} — Image file not found at {img_path}]")
        run.italic = True
        run.font.color.rgb = RGBColor(0xD9, 0x77, 0x06)

def generate_docx():
    doc = Document()
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FraudLens_Report_Assets"))

    # =========================================================================
    # SECTION 1: COVER PAGE
    # =========================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(24)
    p_inst.paragraph_format.space_after = Pt(4)
    r_inst = p_inst.add_run(STUDENT_INFO["institution"].upper())
    r_inst.font.name = "Calibri"
    r_inst.font.size = Pt(13)
    r_inst.bold = True
    r_inst.font.color.rgb = COLOR_NAVY

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(36)
    r_dept = p_dept.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING")
    r_dept.font.name = "Calibri"
    r_dept.font.size = Pt(10.5)
    r_dept.bold = True
    r_dept.font.color.rgb = COLOR_MUTED

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("FRAUDLENS")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(28)
    r_title.bold = True
    r_title.font.color.rgb = COLOR_NAVY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(20)
    r_sub = p_sub.add_run("Financial Transaction and Fraud Investigation Management System")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(15)
    r_sub.bold = True
    r_sub.font.color.rgb = COLOR_BLUE

    p_rep = doc.add_paragraph()
    p_rep.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rep.paragraph_format.space_after = Pt(40)
    r_rep = p_rep.add_run("A DATABASE MANAGEMENT SYSTEMS CASE STUDY REPORT")
    r_rep.font.name = "Calibri"
    r_rep.font.size = Pt(11)
    r_rep.bold = True
    r_rep.font.color.rgb = COLOR_SLATE

    # Metadata Card Box
    meta_tbl = doc.add_table(rows=1, cols=1)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_tbl.autofit = False
    meta_tbl.columns[0].width = Inches(5.8)
    c = meta_tbl.cell(0, 0)
    set_cell_background(c, "F8FAFC")
    set_cell_margins(c, top=140, bottom=140, left=180, right=180)

    tcPr = c._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="12" w:space="0" w:color="{NAVY_HEX}"/>'
        f'<w:left w:val="single" w:sz="12" w:space="0" w:color="{NAVY_HEX}"/>'
        f'<w:bottom w:val="single" w:sz="12" w:space="0" w:color="{NAVY_HEX}"/>'
        f'<w:right w:val="single" w:sz="12" w:space="0" w:color="{NAVY_HEX}"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)

    meta_p = c.paragraphs[0]
    meta_p.paragraph_format.space_before = Pt(2)
    meta_p.paragraph_format.space_after = Pt(2)
    meta_p.paragraph_format.line_spacing = 1.3

    meta_lines = [
        ("Institution: ", f"{STUDENT_INFO['institution']}"),
        ("Submitted By: ", "1. D Joshua Daniel (Reg No: 24BCE0436)\n   2. M Saryu (Reg No: 24BCE2524)"),
        ("Degree & Branch: ", STUDENT_INFO["degree"]),
        ("Subject: ", STUDENT_INFO["subject"]),
        ("Faculty Evaluator: ", STUDENT_INFO["guide"]),
        ("Database Environment: ", STUDENT_INFO["db_platform"]),
        ("Container & Schema: ", f"{STUDENT_INFO['container']} / {STUDENT_INFO['schema']}"),
    ]
    for lbl, val in meta_lines:
        r_l = meta_p.add_run(lbl)
        r_l.bold = True
        r_l.font.name = "Calibri"
        r_l.font.size = Pt(9.5)
        r_l.font.color.rgb = COLOR_NAVY
        r_v = meta_p.add_run(f"{val}\n")
        r_v.font.name = "Calibri"
        r_v.font.size = Pt(9.5)
        r_v.font.color.rgb = COLOR_TEXT

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(45)
    r_foot = p_foot.add_run(f"{STUDENT_INFO['submission_date']} — Evaluated via Native Oracle SQL*Plus Engine")
    r_foot.font.name = "Calibri"
    r_foot.font.size = Pt(9.5)
    r_foot.italic = True
    r_foot.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # =========================================================================
    # TABLE OF CONTENTS
    # =========================================================================
    add_heading_1(doc, "Table of Contents")
    toc_items = [
        ("1. Cover Page", "1"),
        ("2. Abstract", "3"),
        ("3. Introduction", "3"),
        ("4. Problem Statement", "3"),
        ("5. Objectives of the Project", "3"),
        ("6. Existing System and Its Limitations", "4"),
        ("7. Proposed System — FraudLens", "4"),
        ("8. Scope of the Project", "4"),
        ("9. Software and Hardware Requirements", "4"),
        ("10. System Architecture", "5"),
        ("11. Entity-Relationship (ER) Diagram", "5"),
        ("12. Relational Schema", "6"),
        ("13. Database Design and Normalization (1NF, 2NF, 3NF)", "7"),
        ("14. Table Structures and Relationships", "7"),
        ("15. Business Rules and Constraints", "11"),
        ("16. SQL Implementation", "12"),
        ("17. DDL and DML Operations", "12"),
        ("18. SQL Queries, Joins, Subqueries, and Aggregate Functions", "12"),
        ("19. Database Views", "13"),
        ("20. Stored Procedures and Functions", "13"),
        ("21. Database Cursors", "13"),
        ("22. Database Triggers and Audit Management", "14"),
        ("23. Fraud Detection and Alert Management Logic", "14"),
        ("24. Investigation Management and Workflow", "14"),
        ("25. Testing Methodology and Test Cases", "14"),
        ("26. Actual Execution Screenshots and Sample Outputs", "16"),
        ("27. Results and Discussion", "19"),
        ("28. Advantages and Limitations", "19"),
        ("29. Future Enhancements", "19"),
        ("30. Conclusion", "19"),
        ("31. References", "20"),
    ]
    tbl_toc = doc.add_table(rows=1, cols=2)
    format_table(tbl_toc, [5.2, 1.3], ["Section Title", "Page"], toc_items)
    doc.add_page_break()

    # =========================================================================
    # SECTION 2: ABSTRACT
    # =========================================================================
    add_heading_1(doc, "2. Abstract")
    add_body(
        doc,
        "Modern digital banking ecosystems process tens of millions of financial transactions daily across "
        "Unified Payments Interface (UPI), Internet Net-Banking, Mobile Applications, Point-of-Sale (POS), "
        "and Automated Teller Machines (ATMs). High transactional velocity must coexist with rigorous Anti-Money "
        "Laundering (AML) controls and forensic accountability. FraudLens: Financial Transaction and Fraud "
        "Investigation Management System is a comprehensive academic relational database project designed to model financial "
        "movements, automate anomaly detection thresholds, dispatch triage alerts, and coordinate forensic case "
        "investigations within a fully auditable database architecture."
    )
    add_body(
        doc,
        "A foundational design principle of FraudLens is the strict operational decoupling of automated alert "
        "signals from legal proof of fraud: an automated alert is an investigative trigger, not definitive proof of "
        "culpability. Built natively on Oracle AI Database 26ai Free Release 23.26.3.0.0 (container FREEPDB1), "
        "FraudLens implements 8 relational tables strictly normalized to Third Normal Form (3NF), 8 sequences, "
        "4 analytical surveillance views, 3 stored procedures, 3 stored functions, 2 database triggers, and 71 integrity "
        "constraints. An automated 13-case test harness verified the expected operational workflows and constraint "
        "rejections across the documented execution run with a 13/13 (100%) recorded pass rate, validating baseline "
        "functional integrity without claiming exhaustive verification."
    )
    add_callout(
        doc,
        "Core Academic Takeaway",
        "FraudLens proves that transactional integrity (ACID properties), business rule enforcement, and forensic "
        "auditing can be maintained directly inside the database tier through normalized relational modeling, "
        "declarative constraints, and PL/SQL procedural intelligence."
    )

    # =========================================================================
    # SECTION 3: INTRODUCTION
    # =========================================================================
    add_heading_1(doc, "3. Introduction")
    add_body(
        doc,
        "The exponential adoption of digital retail payments has transformed retail banking into a 24x7 real-time "
        "environment. While this enables frictionless payments, it exposes banking platforms to sophisticated cyber-threats, "
        "including authorized push payment fraud, credential stuffing, rapid account draining, smurfing (structuring), "
        "and unauthorized international cross-border transfers. Traditional flat-file logging and decentralized application "
        "logic fail to satisfy modern regulatory standards set by central banks and financial intelligence units."
    )
    add_body(
        doc,
        "Database Management Systems (DBMS) serve as the bedrock of dependable financial platforms. Through structured "
        "schema design, ACID guarantees (Atomicity, Consistency, Isolation, Durability), and declarative integrity constraints, "
        "an enterprise RDBMS prevents double spending, guarantees balance veracity, and maintains auditable event trails. "
        "FraudLens models this end-to-end banking pipeline, bridging high-volume payment processing with forensic investigation "
        "management."
    )

    # =========================================================================
    # SECTION 4: PROBLEM STATEMENT
    # =========================================================================
    add_heading_1(doc, "4. Problem Statement")
    add_body(
        doc,
        "Contemporary commercial banking systems face four critical relational and operational dilemmas:"
    )
    add_bullet(
        doc,
        "Financial databases must process high-frequency transactions without incurring prohibitive latency, while simultaneously checking each event against surveillance thresholds.",
        "High-Velocity Anomaly Detection: "
    )
    add_bullet(
        doc,
        "Automated rule engines produce false positives. Labeling a customer transaction as fraudulent without forensic validation causes unwarranted account freezes and reputational damage. Systems require structured hand-offs from automated signals to human compliance officers.",
        "Alert vs. Proof Distinction: "
    )
    add_bullet(
        doc,
        "Surveillance alerts must be allocated to certified, active investigators according to specialization, tracking case lifecycle from initiation to final verdict.",
        "Caseworker Allocation & Lifecycle Tracking: "
    )
    add_bullet(
        doc,
        "Financial regulations mandate that every state transition in a fraud investigation must be historically preserved with user session identification and precise timestamps.",
        "Trigger-Based Forensic Auditability: "
    )

    # =========================================================================
    # SECTION 5: OBJECTIVES OF THE PROJECT
    # =========================================================================
    add_heading_1(doc, "5. Objectives of the Project")
    add_bullet(doc, "Design a normalized Third Normal Form (3NF) relational schema modeling customers, accounts, transactions, fraud alerts, investigators, and investigation cases.", "1. Schema Normalization: ")
    add_bullet(doc, "Enforce referential integrity, multi-column unique keys, and domain check constraints (amount > 0, balance >= 0, status domains) natively within Oracle Database.", "2. Declarative Integrity: ")
    add_bullet(doc, "Develop stored procedures for automated high-value surveillance (> INR 50,000 threshold), case allocation, and lifecycle state management.", "3. Procedural Automation: ")
    add_bullet(doc, "Implement reusable stored functions for customer risk tier classification, transacted volume aggregation, and account alert counts.", "4. Analytical Intelligence: ")
    add_bullet(doc, "Construct database views providing real-time transaction surveillance, customer risk postures, and triage queues.", "5. Data Abstraction & Views: ")
    add_bullet(doc, "Build row-level database triggers that capture chronological audit event streams on investigation and alert state transitions.", "6. Trigger-Based Audit Trails: ")
    add_bullet(doc, "Verify all DDL, DML, queries, and PL/SQL subprograms natively against Oracle AI Database 26ai Free.", "7. Empirical Verification: ")

    # =========================================================================
    # SECTION 6: EXISTING SYSTEM AND ITS LIMITATIONS
    # =========================================================================
    add_heading_1(doc, "6. Existing System and Its Limitations")
    add_body(
        doc,
        "In many traditional banking and legacy institutional setups, transaction tracking and fraud surveillance "
        "suffer from severe architectural shortcomings:"
    )
    add_bullet(doc, "Customer demographic information, account balances, and transaction logs are stored in loosely structured tables, leading to update anomalies and data redundancy.", "Flat & Denormalized Ledgers: ")
    add_bullet(doc, "Fraud detection logic is implemented purely in external application code, bypassing database-tier constraint enforcement.", "External Application Reliance: ")
    add_bullet(doc, "Compliance teams manually copy suspicious records into external spreadsheets, resulting in lost evidence, unassigned cases, and zero accountability.", "Spreadsheet-Based Triage: ")
    add_bullet(doc, "Status modifications can be executed without leaving an audit trail, creating severe vulnerabilities to internal collusion and compliance penalties.", "Absence of Immutable Audit Logs: ")

    # =========================================================================
    # SECTION 7: PROPOSED SYSTEM — FRAUDLENS
    # =========================================================================
    add_heading_1(doc, "7. Proposed System — FraudLens")
    add_body(
        doc,
        "FraudLens overcomes these limitations by integrating transaction processing, surveillance rules, and caseworker "
        "management into a single cohesive, auditable Oracle Database architecture. The proposed system features:"
    )
    add_bullet(doc, "Explicit separation of customer identities, bank accounts, monetary movements, anomaly signals, and forensic cases.", "Decoupled 3-Tier Relational Model: ")
    add_bullet(doc, "Transactions exceeding INR 50,000 or exhibiting suspicious channels automatically invoke stored procedures that generate fraud alert signals.", "In-Database Anomaly Evaluation: ")
    add_bullet(doc, "High-severity alerts are formally escalated into an investigation dossier, strictly assignable only to active, qualified investigators.", "Rigorous Casework Dossier: ")
    add_bullet(doc, "Database triggers intercept every status change, logging previous/new states, database user credentials, and precise timestamps to dedicated audit tables.", "Autonomous Forensic Auditing: ")

    # =========================================================================
    # SECTION 8: SCOPE OF THE PROJECT
    # =========================================================================
    add_heading_1(doc, "8. Scope of the Project")
    add_body(
        doc,
        "The functional scope of FraudLens encompasses:"
    )
    add_bullet(doc, "KYC status tracking (VERIFIED, PENDING, REJECTED) and baseline credit/fraud risk score management.", "Customer Management: ")
    add_bullet(doc, "Multi-account ownership per customer (Savings, Current, Salary, NRI) with non-negative balance checks.", "Account Administration: ")
    add_bullet(doc, "Financial debits, credits, transfers, and payments across Mobile App, Net Banking, ATM, POS, and UPI.", "Transaction Processing: ")
    add_bullet(doc, "Automated detection of transactions exceeding INR 50,000 threshold and alert generation via stored procedure.", "Surveillance & Alerting: ")
    add_bullet(doc, "Casework assignment, status progression (OPEN -> UNDER REVIEW -> CLOSED), and definitive verdict enforcement.", "Investigation Management: ")
    add_bullet(doc, "FraudLens functions as a surveillance and forensic tracking system. It records transaction events, channel metadata, and surveillance flags in TRANSACTIONS, with account balance snapshots in ACCOUNT.balance. It does not perform automated general ledger debit/credit balance mutations upon insert.", "Transaction Engine Demarcation: ")
    add_bullet(doc, "The test harness explicitly verified Atomicity (atomic PL/SQL execution and savepoint rollbacks) and Consistency (71 integrity constraints). Multi-user concurrency isolation and crash recovery testing were not performed.", "ACID Testing Scope: ")
    add_body(
        doc,
        "Scope Boundaries: Real-time distributed Kafka streaming, advanced machine-learning classification models, "
        "and multi-node graph databases are designated as future architectural enhancements."
    )

    # =========================================================================
    # SECTION 9: SOFTWARE AND HARDWARE REQUIREMENTS
    # =========================================================================
    add_heading_1(doc, "9. Software and Hardware Requirements")
    add_heading_2(doc, "9.1 Software Requirements")
    add_bullet(doc, "Oracle AI Database 26ai Free Release 23.26.3.0.0 (Container: FREEPDB1, Schema: FRAUDLENS_USER)", "Database Management System: ")
    add_bullet(doc, "Oracle SQL*Plus 23.26.0.0.0 and Oracle SQL Developer 23.x / 24.x", "Database Client Interfaces: ")
    add_bullet(doc, "Oracle SQL (DDL, DML, DQL) and Oracle PL/SQL (Procedures, Functions, Cursors, Triggers)", "Database Languages: ")
    add_bullet(doc, "Python 3.10+ (reportlab, python-docx, Pillow) for offline validation and academic report generation", "Supporting Tools: ")
    add_bullet(doc, "Microsoft Windows 11 Home Single Language (64-bit, Build 26200)", "Host Operating System: ")

    add_heading_2(doc, "9.2 Hardware Requirements: Host Machine vs System Sizing")
    add_bullet(doc, "Host Machine: 11th Gen Intel Core i3-1115G4 @ 3.00GHz (2 Cores, 4 Threads) | Minimum: Dual-Core x86_64 CPU (2.0 GHz) | Recommended: Intel Xeon / Core i7 (8+ Cores)", "Processor (CPU): ")
    add_bullet(doc, "Host Machine: 8.0 GB RAM (dynamic SGA/PGA allocation) | Minimum: 4.0 GB RAM | Recommended: 16.0+ GB RAM", "Primary Memory (RAM): ")
    add_bullet(doc, "Host Machine: 256 GB NVMe SSD (NTFS File System) | Minimum: 20 GB Storage Space | Recommended: 50+ GB Enterprise NVMe SSD", "Secondary Storage: ")

    # =========================================================================
    # SECTION 10: SYSTEM ARCHITECTURE
    # =========================================================================
    add_heading_1(doc, "10. System Architecture")
    add_body(
        doc,
        "The FraudLens architecture is structured into four decoupled layers, providing clear separation between transactional "
        "ingestion, anomaly surveillance, caseworker management, and forensic audit logging. Figure 1 illustrates this end-to-end flow."
    )
    arch_img = os.path.join(assets_dir, "architecture_flow.png")
    add_image_figure(doc, arch_img, "Figure 1: FraudLens End-to-End System Architecture Flow Diagram", width_in=6.2)
    add_body(
        doc,
        "Architecture Flow Breakdown:\n"
        "1. Ingestion Layer: Banking clients initiate financial transactions across digital channels (Mobile App, UPI, Net-Banking, ATM, POS). "
        "Transactions are recorded in the TRANSACTIONS table with immediate ACID atomicity.\n"
        "2. Surveillance & Rule Engine: Stored procedure SP_EVALUATE_AND_ALERT_TRANSACTION is explicitly invoked via application logic, batch runs, or test harness calls (not via an automated table trigger). "
        "For transactions breaching threshold limits (> INR 50,000), it updates transaction status to FLAGGED and generates an alert in FRAUD_ALERT.\n"
        "3. Investigation Subsystem: Triage officers review unassigned alerts via VW_UNASSIGNED_ALERTS and open an INVESTIGATION case dossier. "
        "Procedure SP_ASSIGN_INVESTIGATOR validates investigator credentials and assigns lead responsibility.\n"
        "4. Trigger-Based Audit Subsystem: As investigations transition across lifecycle states, row-level database triggers intercept "
        "the UPDATE statement and write an automated snapshot to INVESTIGATION_AUDIT."
    )

    # =========================================================================
    # SECTION 11: ENTITY-RELATIONSHIP (ER) DIAGRAM
    # =========================================================================
    add_heading_1(doc, "11. Entity-Relationship (ER) Diagram")
    add_body(
        doc,
        "The conceptual database design of FraudLens models 6 core entities and 2 supporting audit event streams. "
        "Figure 2 presents the complete Entity-Relationship diagram with primary keys, foreign keys, and cardinalities."
    )
    erd_img = os.path.join(assets_dir, "erd_diagram.png")
    add_image_figure(doc, erd_img, "Figure 2: FraudLens Entity-Relationship (ER) Diagram (Oracle Data Modeler Standard)", width_in=6.2)
    add_body(
        doc,
        "Entity Cardinality Specifications & Architectural Reconciliation:\n"
        "• CUSTOMER to ACCOUNT (1 : N): One customer may own one or multiple bank accounts; each account belongs to exactly one customer.\n"
        "• ACCOUNT to TRANSACTIONS (1 : N): One account maintains multiple financial transaction records; each transaction belongs to a single account.\n"
        "• TRANSACTIONS to FRAUD_ALERT (Structural 1 : N vs Procedural 1 : 1 Guard): In the relational DDL, transaction_id is a non-unique foreign key in FRAUD_ALERT, structurally allowing multiple alerts (e.g. from different rule engines) per transaction. Procedurally, SP_EVALUATE_AND_ALERT_TRANSACTION executes a transaction-level deduplication check (WHERE transaction_id = p_transaction_id) that exits if ANY alert exists for the transaction, operating as 1:0..1 to suppress duplicate alerts regardless of rule type.\n"
        "• FRAUD_ALERT to INVESTIGATION (1 : 0..1): In the schema, INVESTIGATION.alert_id is defined with both a Foreign Key referencing FRAUD_ALERT(alert_id) and a UNIQUE NOT NULL constraint (uq_inv_alert). This guarantees that each investigation docket references exactly one alert, and no alert can be linked to multiple investigations. The relationship is 1 : 0..1 because an alert can exist without an investigation (e.g., pending triage or dismissed alerts like Alert 7005 and 7007, tracked via VW_UNASSIGNED_ALERTS).\n"
        "• INVESTIGATOR to INVESTIGATION (1 : N): One forensic investigator manages multiple assigned investigation cases.\n"
        "• INVESTIGATION to INVESTIGATION_AUDIT (1 : N): Each investigation generates a chronological stream of audit records."
    )

    # =========================================================================
    # SECTION 12: RELATIONAL SCHEMA
    # =========================================================================
    add_heading_1(doc, "12. Relational Schema")
    add_body(
        doc,
        "The formal relational schema of FraudLens is expressed below, where Primary Keys are enclosed in bold brackets [PK] "
        "and Foreign Keys are marked with [FK]:"
    )
    schema_code = (
        "CUSTOMER ([customer_id PK], first_name, last_name, email [UK], phone [UK], kyc_status, risk_score, created_at)\n\n"
        "ACCOUNT ([account_id PK], customer_id [FK -> CUSTOMER.customer_id], account_number [UK], account_type, balance, currency, status, created_at)\n\n"
        "TRANSACTIONS ([transaction_id PK], account_id [FK -> ACCOUNT.account_id], transaction_type, amount, transaction_date, channel, status, counterparty_account, description)\n\n"
        "FRAUD_ALERT ([alert_id PK], transaction_id [FK -> TRANSACTIONS.transaction_id], alert_type, severity, rule_triggered, alert_date, status)\n\n"
        "INVESTIGATOR ([investigator_id PK], first_name, last_name, email [UK], department, experience_years, active_status)\n\n"
        "INVESTIGATION ([investigation_id PK], alert_id [FK -> FRAUD_ALERT.alert_id, UK], investigator_id [FK -> INVESTIGATOR.investigator_id], start_date, end_date, status, outcome, notes)\n\n"
        "INVESTIGATION_AUDIT ([audit_id PK], investigation_id, old_status, new_status, changed_by, change_timestamp, change_action)\n\n"
        "ALERT_AUDIT ([audit_id PK], alert_id, old_status, new_status, changed_by, change_timestamp, remarks)"
    )
    add_code_block(doc, schema_code)

    # =========================================================================
    # SECTION 13: DATABASE DESIGN AND NORMALIZATION
    # =========================================================================
    add_heading_1(doc, "13. Database Design and Normalization (1NF, 2NF, 3NF)")
    add_body(
        doc,
        "Database normalization systematically eliminates data redundancy, prevents insertion, update, and deletion anomalies, "
        "and ensures that all functional dependencies adhere to relational theory."
    )
    add_heading_2(doc, "13.1 First Normal Form (1NF)")
    add_body(
        doc,
        "A relation is in 1NF if and only if every attribute contains only atomic (indivisible) values, and there are no repeating "
        "groups or arrays. FraudLens satisfies 1NF because:\n"
        "• Customer names are split into first_name and last_name rather than stored as a composite string.\n"
        "• Phone numbers and emails are unique scalar strings, not multi-valued lists.\n"
        "• Each table has a defined single-attribute primary key (customer_id, account_id, transaction_id, etc.)."
    )
    add_heading_2(doc, "13.2 Second Normal Form (2NF)")
    add_body(
        doc,
        "A relation is in 2NF if it is in 1NF and every non-prime attribute is fully functionally dependent on the primary key, "
        "eliminating partial dependencies. FraudLens satisfies 2NF because:\n"
        "• All primary keys in the schema are single-column synthetic sequences (e.g. account_id, transaction_id).\n"
        "• In relational theory, partial dependencies can only exist when a primary key is composite. Since all candidate keys "
        "are single attributes, partial dependency is mathematically impossible."
    )
    add_heading_2(doc, "13.3 Third Normal Form (3NF)")
    add_body(
        doc,
        "A relation is in 3NF if it is in 2NF and for every non-trivial functional dependency X -> Y, either X is a superkey or Y is a prime attribute. "
        "A single-column primary key mathematically eliminates partial dependencies (2NF), but 3NF additionally requires that non-key attributes do not determine each other (absence of transitive dependencies). FraudLens rigorously satisfies 3NF across all entities:\n"
        "• CUSTOMER: Determinants are candidate keys (customer_id, email, phone). Non-key attributes {kyc_status, risk_score, created_at} are mutually independent; kyc_status does not determine risk_score (customers with VERIFIED KYC have scores ranging from 8 to 85).\n"
        "• ACCOUNT: Determinants are candidate keys (account_id, account_number). Non-keys {account_type, balance, currency, status, created_at} are independent; account_type does not determine status (SAVINGS and CURRENT accounts exist with ACTIVE, FROZEN, or DORMANT status).\n"
        "• TRANSACTIONS: Customer demographics are not stored; only account_id is referenced. Non-keys {transaction_type, amount, transaction_date, channel, status, counterparty_account, description} are independent; channel does not determine status.\n"
        "• FRAUD_ALERT: Transaction details (amount, channel) reside strictly in TRANSACTIONS, preventing transitive redundancy. Non-keys are independent.\n"
        "• INVESTIGATION: Investigator details depend strictly on investigator_id and are not stored in the case record. Candidate keys are investigation_id and alert_id (via UNIQUE NOT NULL constraint).\n"
        "Thus, every determinant in FraudLens is a candidate superkey, eliminating transitive dependencies."
    )
    add_callout(
        doc,
        "Decoupled Design of Audit Tables",
        "The audit tables (INVESTIGATION_AUDIT and ALERT_AUDIT) are append-only historical ledgers with surrogate primary keys (audit_id). "
        "They intentionally omit restrictive foreign keys to remain decoupled, ensuring audit records persist even if parent records are archived."
    )

    # =========================================================================
    # SECTION 14: TABLE STRUCTURES AND RELATIONSHIPS
    # =========================================================================
    add_heading_1(doc, "14. Table Structures and Relationships")
    add_body(
        doc,
        "FraudLens comprises 8 relational tables. The schema definitions, data types, constraints, and operational purposes "
        "for each table are detailed below."
    )
    for tbl_def in TABLE_DEFINITIONS:
        add_heading_2(doc, f"14.{TABLE_DEFINITIONS.index(tbl_def) + 1} Table: {tbl_def['name']}")
        add_body(doc, f"Purpose: {tbl_def['purpose']}")
        add_bullet(doc, tbl_def["pk"], "Primary Key: ")
        add_bullet(doc, tbl_def["fks"], "Foreign Keys: ")
        add_bullet(doc, tbl_def["uks"], "Unique Keys: ")
        add_bullet(doc, tbl_def["checks"], "Check Constraints: ")

        headers = ["Column Name", "Data Type", "Null?", "Default", "Key / Constraint", "Description"]
        col_w = [1.2, 1.0, 0.5, 0.7, 1.3, 1.8]
        t = doc.add_table(rows=1, cols=6)
        format_table(t, col_w, headers, tbl_def["columns"], is_small=True)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_callout(
        doc,
        "Statutory Retention & Critical Evaluation of ON DELETE CASCADE",
        "The prototype defines ON DELETE CASCADE on foreign keys linking customers, accounts, transactions, and alerts as an academic testing convenience "
        "to enable clean test harness rollbacks. In production banking, physical record deletion is strictly prohibited: Section 12(1)(a) of the Prevention "
        "of Money Laundering Act (PMLA) 2002, Rule 3 of the PML Rules 2005 (amended by Finance Act 2019), Chapter VII of the RBI KYC Master Direction 2016 "
        "(Updated 2023), and FATF Recommendation 11 legally mandate a minimum 5-year retention period for transaction records from the transaction date "
        "and customer identification records from the cessation of the relationship. Production banking schemas mandate ON DELETE RESTRICT and logical soft deletion (status = 'CLOSED')."
    )

    # =========================================================================
    # SECTION 15: BUSINESS RULES AND CONSTRAINTS
    # =========================================================================
    add_heading_1(doc, "15. Business Rules and Constraints")
    add_body(
        doc,
        "Data integrity in FraudLens is enforced declaratively through 71 constraints compiled in the Oracle data dictionary. "
        "These constraints guarantee that invalid data cannot be committed under any circumstances."
    )
    inv_tbl = doc.add_table(rows=1, cols=4)
    format_table(inv_tbl, [1.4, 0.8, 0.8, 3.5], ["Object Type", "Count", "Status", "Verified Objects / Notes"], DB_INVENTORY)

    add_heading_2(doc, "15.1 Core Business Rules Summary")
    add_bullet(doc, "Every financial debit, credit, or transfer must have amount > 0. Negative or zero monetary transactions raise ORA-02290.", "BR-01: Non-Zero Positive Amounts: ")
    add_bullet(doc, "Bank account ledger balances cannot drop below 0.00 INR (balance >= 0). Overdrafts must be formally modeled as credit limits.", "BR-02: Non-Negative Ledger Balance: ")
    add_bullet(doc, "A customer's email and phone number must be unique across the entire banking directory, preventing duplicate profile creation.", "BR-03: Unique Customer Credentials: ")
    add_bullet(doc, "Transactions greater than INR 50,000 are classified as high-value surveillance events and trigger automated alert evaluation.", "BR-04: High-Value Threshold: ")
    add_bullet(doc, "Only investigators with active_status = 'ACTIVE' can be allocated to lead an investigation case docket.", "BR-05: Active Investigator Eligibility: ")
    add_bullet(doc, "An investigation cannot transition to 'CLOSED' without a definitive verdict: CONFIRMED_FRAUD, FALSE_POSITIVE, or INCONCLUSIVE.", "BR-06: Mandatory Case Outcome: ")
    add_bullet(doc, "Deleting a customer or account cascades deletions down to child transactions and alerts (ON DELETE CASCADE), preserving referential consistency.", "BR-07: Referential Cascading: ")

    # =========================================================================
    # SECTION 16: SQL IMPLEMENTATION
    # =========================================================================
    add_heading_1(doc, "16. SQL Implementation")
    add_body(
        doc,
        "The implementation of FraudLens is structured into 12 modular, numbered SQL scripts designed for reproducible execution "
        "against any Oracle Database instance. The master driver script 00_run_all.sql controls the pipeline."
    )
    pipeline_code = (
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
    add_code_block(doc, pipeline_code)

    # =========================================================================
    # SECTION 17: DDL AND DML OPERATIONS
    # =========================================================================
    add_heading_1(doc, "17. DDL and DML Operations")
    add_body(
        doc,
        "Script 02_ddl_dml_demos.sql demonstrates data definition modifications and data manipulation operations "
        "executed safely within transaction control blocks."
    )
    add_heading_2(doc, "17.1 DDL Demonstrations")
    ddl_code = (
        "-- Adding, Modifying, Renaming, and Dropping Table Columns\n"
        "ALTER TABLE CUSTOMER ADD (middle_name VARCHAR2(50));\n"
        "ALTER TABLE CUSTOMER MODIFY (middle_name VARCHAR2(100));\n"
        "ALTER TABLE CUSTOMER RENAME COLUMN middle_name TO secondary_name;\n"
        "ALTER TABLE CUSTOMER DROP COLUMN secondary_name;\n\n"
        "-- Adding and Dropping Check Constraints\n"
        "ALTER TABLE ACCOUNT ADD CONSTRAINT chk_acc_currency_inr CHECK (currency IN ('INR', 'USD', 'EUR'));\n"
        "ALTER TABLE ACCOUNT DROP CONSTRAINT chk_acc_currency_inr;"
    )
    add_code_block(doc, ddl_code)

    add_heading_2(doc, "17.2 DML Operations with Transaction Control")
    dml_code = (
        "-- DML Insert with Explicit Savepoint and Safe Rollback\n"
        "SAVEPOINT sp_before_dml_demo;\n"
        "INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score)\n"
        "VALUES (seq_customer_id.NEXTVAL, 'Test', 'User', 'temp.test@demo.in', '+919999988888', 'PENDING', 20);\n\n"
        "-- Status Update\n"
        "UPDATE CUSTOMER SET kyc_status = 'VERIFIED' WHERE email = 'temp.test@demo.in';\n\n"
        "-- Rollback to preserve seed baseline\n"
        "ROLLBACK TO sp_before_dml_demo;"
    )
    add_code_block(doc, dml_code)

    # =========================================================================
    # SECTION 18: SQL QUERIES, JOINS, SUBQUERIES, AND AGGREGATE FUNCTIONS
    # =========================================================================
    add_heading_1(doc, "18. SQL Queries, Joins, Subqueries, and Aggregate Functions")
    add_body(
        doc,
        "FraudLens includes a rich library of analytical queries demonstrating single-row functions, multi-table joins, "
        "group aggregations, and subqueries."
    )

    add_heading_2(doc, "18.1 Single-Row String, Numeric, and Date Functions")
    q1_code = (
        "SELECT customer_id, \n"
        "       UPPER(first_name || ' ' || last_name) AS full_name_uppercase,\n"
        "       LOWER(email) AS standardized_email,\n"
        "       LENGTH(phone) AS phone_len,\n"
        "       SUBSTR(phone, 1, 3) AS country_code\n"
        "FROM CUSTOMER WHERE customer_id IN (1001, 1002, 1005);"
    )
    add_code_block(doc, q1_code)

    add_heading_2(doc, "18.2 Group Functions and Aggregations (GROUP BY & HAVING)")
    add_body(doc, "Aggregates transacted volumes across digital payment channels, filtering for channels with total volume exceeding INR 100,000:")
    q2_code = (
        "SELECT channel, \n"
        "       COUNT(transaction_id) AS total_tx,\n"
        "       SUM(amount) AS total_volume,\n"
        "       ROUND(AVG(amount), 2) AS avg_ticket\n"
        "FROM TRANSACTIONS\n"
        "GROUP BY channel\n"
        "HAVING SUM(amount) > 100000\n"
        "ORDER BY total_volume DESC;"
    )
    add_code_block(doc, q2_code)
    q2_results = [
        ("NET_BANKING", "8", "1,820,000.00", "227,500.00"),
        ("ATM", "3", "262,000.00", "87,333.33"),
        ("UPI", "4", "128,500.00", "32,125.00"),
    ]
    t_q2 = doc.add_table(rows=1, cols=4)
    format_table(t_q2, [1.8, 1.2, 1.8, 1.7], ["Channel", "Total Txns", "Total Volume (INR)", "Average Ticket (INR)"], q2_results)

    add_heading_2(doc, "18.3 Multi-Table Relational Joins (4-Table Surveillance Join)")
    q3_code = (
        "SELECT c.first_name || ' ' || c.last_name AS customer,\n"
        "       a.account_number, t.amount, t.channel, fa.alert_type, fa.severity\n"
        "FROM CUSTOMER c\n"
        "JOIN ACCOUNT a ON c.customer_id = a.customer_id\n"
        "JOIN TRANSACTIONS t ON a.account_id = t.account_id\n"
        "JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id\n"
        "ORDER BY t.amount DESC;"
    )
    add_code_block(doc, q3_code)

    add_heading_2(doc, "18.4 Subqueries (Single-Row, Multi-Row, Correlated)")
    q_sub_code = (
        "-- Single-Row Subquery: Transactions exceeding overall system average\n"
        "SELECT transaction_id, amount, channel\n"
        "FROM TRANSACTIONS\n"
        "WHERE amount > (SELECT AVG(amount) FROM TRANSACTIONS);\n\n"
        "-- Multi-Row Subquery with IN: Customers with at least one FLAGGED transaction\n"
        "SELECT customer_id, first_name || ' ' || last_name AS customer_name, risk_score\n"
        "FROM CUSTOMER\n"
        "WHERE customer_id IN (\n"
        "    SELECT a.customer_id FROM ACCOUNT a \n"
        "    WHERE a.account_id IN (SELECT t.account_id FROM TRANSACTIONS t WHERE t.status = 'FLAGGED')\n"
        ");\n\n"
        "-- Correlated Subquery with EXISTS: Accounts that have incurred at least one fraud alert\n"
        "SELECT account_number, balance FROM ACCOUNT a\n"
        "WHERE EXISTS (\n"
        "    SELECT 1 FROM TRANSACTIONS t \n"
        "    JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id \n"
        "    WHERE t.account_id = a.account_id\n"
        ");"
    )
    add_code_block(doc, q_sub_code)

    # =========================================================================
    # SECTION 19: DATABASE VIEWS
    # =========================================================================
    add_heading_1(doc, "19. Database Views")
    add_body(
        doc,
        "FraudLens implements 4 analytical database views to simplify complex joins, enhance security by abstracting base tables, "
        "and provide specialized operational dashboards."
    )
    v1_code = (
        "-- 1. VW_HIGH_RISK_TRANSACTIONS: Surfaces high-ticket (>50k INR) or FLAGGED transactions\n"
        "CREATE OR REPLACE VIEW VW_HIGH_RISK_TRANSACTIONS AS\n"
        "SELECT t.transaction_id, t.account_id, a.account_number, c.customer_id,\n"
        "       c.first_name || ' ' || c.last_name AS customer_name, c.risk_score AS customer_risk_score,\n"
        "       t.transaction_type, t.amount, t.channel, t.transaction_date,\n"
        "       t.status AS tx_status, fa.alert_id, fa.alert_type, fa.severity AS alert_severity\n"
        "FROM TRANSACTIONS t\n"
        "JOIN ACCOUNT a ON t.account_id = a.account_id\n"
        "JOIN CUSTOMER c ON a.customer_id = c.customer_id\n"
        "LEFT JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id\n"
        "WHERE t.amount > 50000.00 OR t.status = 'FLAGGED';\n\n"
        "-- 2. VW_INVESTIGATION_SUMMARY: Case lifecycle and turnaround tracking\n"
        "CREATE OR REPLACE VIEW VW_INVESTIGATION_SUMMARY AS\n"
        "SELECT inv.investigation_id, inv.status AS investigation_status, inv.outcome,\n"
        "       fa.alert_id, fa.alert_type, fa.severity AS alert_severity,\n"
        "       t.amount AS transaction_amount,\n"
        "       NVL(i.first_name || ' ' || i.last_name, 'UNASSIGNED') AS lead_investigator,\n"
        "       i.department, inv.start_date, inv.end_date,\n"
        "       CASE WHEN inv.end_date IS NOT NULL THEN (inv.end_date - inv.start_date)\n"
        "            ELSE ROUND(SYSDATE - inv.start_date, 1) END AS duration_days\n"
        "FROM INVESTIGATION inv\n"
        "JOIN FRAUD_ALERT fa ON inv.alert_id = fa.alert_id\n"
        "JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id\n"
        "LEFT JOIN INVESTIGATOR i ON inv.investigator_id = i.investigator_id;\n\n"
        "-- 3. VW_CUSTOMER_FRAUD_EXPOSURE: 360-degree customer portfolio risk posture\n"
        "CREATE OR REPLACE VIEW VW_CUSTOMER_FRAUD_EXPOSURE AS\n"
        "SELECT c.customer_id, c.first_name || ' ' || c.last_name AS customer_name,\n"
        "       c.kyc_status, c.risk_score,\n"
        "       COUNT(DISTINCT a.account_id) AS total_accounts,\n"
        "       NVL(SUM(t.amount), 0) AS total_transacted_volume,\n"
        "       COUNT(DISTINCT t.transaction_id) AS total_tx_count,\n"
        "       COUNT(DISTINCT fa.alert_id) AS alerts_incurred\n"
        "FROM CUSTOMER c\n"
        "LEFT JOIN ACCOUNT a ON c.customer_id = a.customer_id\n"
        "LEFT JOIN TRANSACTIONS t ON a.account_id = t.account_id\n"
        "LEFT JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id\n"
        "GROUP BY c.customer_id, c.first_name, c.last_name, c.kyc_status, c.risk_score;\n\n"
        "-- 4. VW_UNASSIGNED_ALERTS: Triage queue for unassigned surveillance signals\n"
        "CREATE OR REPLACE VIEW VW_UNASSIGNED_ALERTS AS\n"
        "SELECT fa.alert_id, fa.transaction_id, t.amount, t.channel, fa.alert_type, fa.severity\n"
        "FROM FRAUD_ALERT fa\n"
        "JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id\n"
        "WHERE fa.alert_id NOT IN (SELECT alert_id FROM INVESTIGATION);"
    )
    add_code_block(doc, v1_code)

    # =========================================================================
    # SECTION 20: STORED PROCEDURES AND FUNCTIONS
    # =========================================================================
    add_heading_1(doc, "20. Stored Procedures and Functions")
    add_body(
        doc,
        "Procedural logic in FraudLens encapsulates mission-critical operational rules inside compiled PL/SQL subprograms, "
        "eliminating redundant application code and ensuring transactional consistency."
    )

    add_heading_2(doc, "20.1 Stored Procedure: SP_EVALUATE_AND_ALERT_TRANSACTION")
    add_body(doc, "Evaluates transaction amounts against the INR 50,000 threshold and triggers an alert if violated:")
    sp1_code = (
        "CREATE OR REPLACE PROCEDURE SP_EVALUATE_AND_ALERT_TRANSACTION (\n"
        "    p_transaction_id IN NUMBER,\n"
        "    p_new_alert_id   OUT NUMBER\n"
        ") AS\n"
        "    v_amount NUMBER(15,2);\n"
        "    v_existing NUMBER;\n"
        "    v_next_id NUMBER;\n"
        "BEGIN\n"
        "    SELECT amount INTO v_amount FROM TRANSACTIONS WHERE transaction_id = p_transaction_id;\n"
        "    SELECT COUNT(*) INTO v_existing FROM FRAUD_ALERT WHERE transaction_id = p_transaction_id;\n"
        "    IF v_existing > 0 THEN p_new_alert_id := NULL; RETURN; END IF;\n\n"
        "    IF v_amount > 50000.00 THEN\n"
        "        SELECT seq_alert_id.NEXTVAL INTO v_next_id FROM DUAL;\n"
        "        INSERT INTO FRAUD_ALERT (alert_id, transaction_id, alert_type, severity, rule_triggered, status)\n"
        "        VALUES (v_next_id, p_transaction_id, 'HIGH_AMOUNT', 'HIGH',\n"
        "                'Rule 101: Transaction amount ' || TO_CHAR(v_amount, 'FM999,990.00') || ' INR exceeds 50k threshold', 'PENDING');\n"
        "        UPDATE TRANSACTIONS SET status = 'FLAGGED' WHERE transaction_id = p_transaction_id;\n"
        "        p_new_alert_id := v_next_id;\n"
        "    ELSE\n"
        "        p_new_alert_id := NULL;\n"
        "    END IF;\n"
        "END SP_EVALUATE_AND_ALERT_TRANSACTION;"
    )
    add_code_block(doc, sp1_code)

    add_heading_2(doc, "20.2 Stored Procedure: SP_ASSIGN_INVESTIGATOR")
    add_body(doc, "Validates case state and verifies that the investigator is currently ACTIVE before allocation:")
    sp2_code = (
        "CREATE OR REPLACE PROCEDURE SP_ASSIGN_INVESTIGATOR (\n"
        "    p_investigation_id IN NUMBER,\n"
        "    p_investigator_id  IN NUMBER\n"
        ") AS\n"
        "    v_inves_status VARCHAR2(15);\n"
        "    v_inv_status   VARCHAR2(15);\n"
        "BEGIN\n"
        "    SELECT status INTO v_inves_status FROM INVESTIGATION WHERE investigation_id = p_investigation_id;\n"
        "    IF v_inves_status = 'CLOSED' THEN\n"
        "        RAISE_APPLICATION_ERROR(-20002, 'Cannot reassign closed investigation.');\n"
        "    END IF;\n\n"
        "    SELECT active_status INTO v_inv_status FROM INVESTIGATOR WHERE investigator_id = p_investigator_id;\n"
        "    IF v_inv_status != 'ACTIVE' THEN\n"
        "        RAISE_APPLICATION_ERROR(-20004, 'Investigator (ID ' || p_investigator_id || ') is INACTIVE.');\n"
        "    END IF;\n\n"
        "    UPDATE INVESTIGATION SET investigator_id = p_investigator_id WHERE investigation_id = p_investigation_id;\n"
        "END SP_ASSIGN_INVESTIGATOR;"
    )
    add_code_block(doc, sp2_code)

    add_heading_2(doc, "20.3 Stored Functions")
    add_body(doc, "Stored functions compute customer risk tiers, total transaction volumes, and account alert counts:")
    fn_code = (
        "-- 1. FN_CALCULATE_RISK_TIER: Maps risk_score (0-100) to qualitative risk tier\n"
        "CREATE OR REPLACE FUNCTION FN_CALCULATE_RISK_TIER (p_customer_id IN NUMBER) RETURN VARCHAR2 AS\n"
        "    v_score NUMBER(3);\n"
        "BEGIN\n"
        "    SELECT risk_score INTO v_score FROM CUSTOMER WHERE customer_id = p_customer_id;\n"
        "    IF v_score BETWEEN 0 AND 25 THEN RETURN 'LOW_RISK';\n"
        "    ELSIF v_score BETWEEN 26 AND 50 THEN RETURN 'MODERATE_RISK';\n"
        "    ELSIF v_score BETWEEN 51 AND 75 THEN RETURN 'HIGH_RISK';\n"
        "    ELSE RETURN 'CRITICAL_RISK';\n"
        "    END IF;\n"
        "END FN_CALCULATE_RISK_TIER;\n\n"
        "-- 2. FN_GET_TOTAL_TX_AMOUNT: Aggregates volume for an account (returns 0.00 if no transactions)\n"
        "CREATE OR REPLACE FUNCTION FN_GET_TOTAL_TX_AMOUNT (p_account_id IN NUMBER) RETURN NUMBER AS\n"
        "    v_sum NUMBER(15,2);\n"
        "BEGIN\n"
        "    SELECT NVL(SUM(amount), 0.00) INTO v_sum FROM TRANSACTIONS WHERE account_id = p_account_id;\n"
        "    RETURN v_sum;\n"
        "END FN_GET_TOTAL_TX_AMOUNT;"
    )
    add_code_block(doc, fn_code)

    # =========================================================================
    # SECTION 21: CURSORS
    # =========================================================================
    add_heading_1(doc, "21. Database Cursors")
    add_body(
        doc,
        "Script 09_cursors.sql fulfills advanced cursor processing requirements using both explicit cursors and "
        "parameterized cursor FOR loops."
    )
    cur_code = (
        "-- 1. Explicit Cursor with OPEN, FETCH, %NOTFOUND, and CLOSE\n"
        "DECLARE\n"
        "    CURSOR cur_high_risk_alerts IS\n"
        "        SELECT fa.alert_id, fa.alert_type, fa.severity, t.amount, a.account_number\n"
        "        FROM FRAUD_ALERT fa\n"
        "        JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id\n"
        "        JOIN ACCOUNT a ON t.account_id = a.account_id\n"
        "        WHERE fa.severity IN ('CRITICAL', 'HIGH')\n"
        "        ORDER BY t.amount DESC;\n"
        "    v_rec cur_high_risk_alerts%ROWTYPE;\n"
        "BEGIN\n"
        "    OPEN cur_high_risk_alerts;\n"
        "    LOOP\n"
        "        FETCH cur_high_risk_alerts INTO v_rec;\n"
        "        EXIT WHEN cur_high_risk_alerts%NOTFOUND;\n"
        "        DBMS_OUTPUT.PUT_LINE('Alert ' || v_rec.alert_id || ' | Severity: ' || v_rec.severity || ' | Amount: ' || v_rec.amount);\n"
        "    END LOOP;\n"
        "    CLOSE cur_high_risk_alerts;\n"
        "END;\n\n"
        "-- 2. Parameterized Cursor FOR Loop (Active Caseload Processing)\n"
        "DECLARE\n"
        "    CURSOR cur_caseload (p_status VARCHAR2) IS\n"
        "        SELECT investigation_id, status, start_date FROM INVESTIGATION WHERE status = p_status;\n"
        "BEGIN\n"
        "    FOR r IN cur_caseload('UNDER REVIEW') LOOP\n"
        "        DBMS_OUTPUT.PUT_LINE('Active Case ' || r.investigation_id || ' started on ' || r.start_date);\n"
        "    END LOOP;\n"
        "END;"
    )
    add_code_block(doc, cur_code)

    # =========================================================================
    # SECTION 22: TRIGGERS AND AUDIT MANAGEMENT
    # =========================================================================
    add_heading_1(doc, "22. Database Triggers and Audit Management")
    add_body(
        doc,
        "FraudLens implements trigger-based audit logging via row-level triggers that monitor state changes on investigations and alerts. "
        "These triggers populate dedicated audit event tables."
    )
    trg_code = (
        "CREATE OR REPLACE TRIGGER TRG_INVESTIGATION_STATUS_AUDIT\n"
        "AFTER UPDATE OF status ON INVESTIGATION\n"
        "FOR EACH ROW\n"
        "WHEN (OLD.status != NEW.status)\n"
        "DECLARE\n"
        "    v_next_audit_id NUMBER;\n"
        "BEGIN\n"
        "    SELECT seq_inves_audit_id.NEXTVAL INTO v_next_audit_id FROM DUAL;\n"
        "    INSERT INTO INVESTIGATION_AUDIT (\n"
        "        audit_id, investigation_id, old_status, new_status, changed_by, change_timestamp, change_action\n"
        "    ) VALUES (\n"
        "        v_next_audit_id, :NEW.investigation_id, :OLD.status, :NEW.status,\n"
        "        USER, SYSTIMESTAMP, 'STATUS_TRANSITION'\n"
        "    );\n"
        "END;\n"
        "/"
    )
    add_code_block(doc, trg_code)
    add_callout(
        doc,
        "Trigger-Based Audit Logging vs Privileged Administrator Access",
        "The trigger automatically captures USER (authenticated Oracle session user) and SYSTIMESTAMP upon every status modification, "
        "providing application-level non-repudiation for standard user sessions. However, database triggers do not constitute a tamper-proof "
        "or immutable audit log against privileged administrators (DBA / SYSDBA), who possess authority to disable triggers (ALTER TRIGGER ... DISABLE), "
        "truncate tables, or directly alter audit records. True regulatory immutability against administrator tampering requires cryptographic ledger tables "
        "(such as Oracle Blockchain Tables) or write-once-read-many (WORM) storage appliances."
    )

    # =========================================================================
    # SECTION 23: FRAUD DETECTION AND ALERT MANAGEMENT LOGIC
    # =========================================================================
    add_heading_1(doc, "23. Fraud Detection and Alert Management Logic")
    add_body(
        doc,
        "FraudLens defines six heuristic risk classifications in its domain constraints. Procedural Automation Scope: In the current prototype, "
        "the HIGH_AMOUNT rule (> INR 50,000 threshold) is actively evaluated and automated by procedure SP_EVALUATE_AND_ALERT_TRANSACTION. "
        "The remaining five categories are modeled in sample seed data to demonstrate forensic triage and reporting, representing proposed future procedural rules:"
    )
    add_bullet(doc, "Single transactions exceeding INR 50,000 threshold (Rule 101). Actively evaluated by SP_EVALUATE_AND_ALERT_TRANSACTION; flags transaction and generates Alert with HIGH severity.", "1. HIGH_AMOUNT (Active Stored Procedure): ")
    add_bullet(doc, "Rapid successive fund transfers executed within minutes, characteristic of automated account drain.", "2. RAPID_VELOCITY (Seed-Modeled / Proposed Rule): ")
    add_bullet(doc, "Transactions executed over high-risk or unusual channels inconsistent with customer profile.", "3. SUSPICIOUS_CHANNEL (Seed-Modeled / Proposed Rule): ")
    add_bullet(doc, "High-value debits executed during non-standard hours (e.g. 02:00 AM to 04:30 AM).", "4. UNUSUAL_HOURS (Seed-Modeled / Proposed Rule): ")
    add_bullet(doc, "International or cross-border wire transfers to foreign accounts without prior travel declarations.", "5. CROSS_BORDER (Seed-Modeled / Proposed Rule): ")
    add_bullet(doc, "Transactions strategically split just below regulatory reporting thresholds (smurfing, e.g. INR 49,500).", "6. STRUCTURING (Seed-Modeled / Proposed Rule): ")
    add_body(
        doc,
        "Alert Deduplication Guard Analysis: Procedure SP_EVALUATE_AND_ALERT_TRANSACTION executes "
        "SELECT COUNT(*) INTO v_existing_alerts FROM FRAUD_ALERT WHERE transaction_id = p_transaction_id;. "
        "If any alert already exists for the transaction, the procedure immediately exits without generating another alert. "
        "This operates as transaction-level deduplication (suppressing all subsequent alerts for that transaction, regardless of rule type) "
        "to prevent duplicate alerts from repeated batch runs, preserving a clean 1:0..1 procedure-to-alert relationship."
    )

    # =========================================================================
    # SECTION 24: INVESTIGATION MANAGEMENT
    # =========================================================================
    add_heading_1(doc, "24. Investigation Management")
    add_body(
        doc,
        "When an alert is escalated, it enters a structured three-stage forensic workflow. Figure 3 illustrates this case progression."
    )
    flow_img = os.path.join(assets_dir, "workflow_lifecycle.png")
    add_image_figure(doc, flow_img, "Figure 3: FraudLens Investigation Lifecycle and Forensic Workflow State Transition Diagram", width_in=6.2)
    add_body(
        doc,
        "Case Lifecycle Progression:\n"
        "1. OPEN: Case docket created and linked 1:1 with an unassigned fraud alert. Awaiting investigator assignment.\n"
        "2. UNDER REVIEW: Active investigator assigned via SP_ASSIGN_INVESTIGATOR. Evidence gathering, counterparty analysis, and customer interviews conducted.\n"
        "3. CLOSED: Case concluded via SP_UPDATE_INVESTIGATION_STATUS. Requires one of three mandatory outcomes: "
        "CONFIRMED_FRAUD (funds blocked, police dossier filed), FALSE_POSITIVE (alert dismissed, account unblocked), "
        "or INCONCLUSIVE (escalated to senior management)."
    )

    # =========================================================================
    # SECTION 25: TESTING METHODOLOGY AND TEST CASES
    # =========================================================================
    add_heading_1(doc, "25. Testing Methodology and Test Cases")
    add_body(
        doc,
        "Testing was performed natively against Oracle AI Database 26ai Free using an automated test harness (11_test_cases.sql). "
        "The suite executes positive functional workflows to confirm expected operations and negative boundary tests to confirm "
        "that invalid data is blocked by constraints. All tests operate within a transaction savepoint with automatic rollback."
    )
    tbl_tests = doc.add_table(rows=1, cols=6)
    test_rows = [[t["id"], t["category"], t["operation"], t["expected"], t["actual"], t["status"]] for t in TEST_CASES]
    format_table(tbl_tests, [0.5, 1.1, 1.6, 1.3, 1.4, 0.6], ["Test ID", "Category", "Target Operation", "Expected Behavior", "Actual Result", "Status"], test_rows, is_small=True)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # SECTION 26: ACTUAL EXECUTION SCREENSHOTS AND SAMPLE OUTPUTS
    # =========================================================================
    add_heading_1(doc, "26. Actual Execution Screenshots and Sample Outputs")
    add_body(
        doc,
        "All screenshots presented in this section represent genuine, real-time executions captured directly from Oracle SQL*Plus "
        "and Oracle SQL Developer running against Oracle AI Database 26ai Free (container FREEPDB1, schema FRAUDLENS_USER)."
    )

    # Screenshot 1
    ss1_img = os.path.join(assets_dir, "01_oracle_connection_and_pdb.png")
    add_image_figure(doc, ss1_img, "Figure 4: Oracle SQL*Plus Terminal Connection, Container FREEPDB1, and Schema FRAUDLENS_USER", width_in=6.0)

    # Screenshot 2
    ss2_img = os.path.join(assets_dir, "02_table_creation_and_list.png")
    add_image_figure(doc, ss2_img, "Figure 5: Table Creation and Data Dictionary Status Verification (USER_TABLES: All 8 Tables VALID)", width_in=6.0)

    # Screenshot 3
    ss3_img = os.path.join(assets_dir, "03_sample_data_row_counts.png")
    add_image_figure(doc, ss3_img, "Figure 6: Baseline Sample Dataset Record Counts (56 Total Operational Records Across 8 Tables)", width_in=6.0)

    # Screenshot 4
    ss4_img = os.path.join(assets_dir, "04_join_and_groupby_queries.png")
    add_image_figure(doc, ss4_img, "Figure 7: Execution of Multi-Table Relational Joins and Channel Aggregation (GROUP BY & HAVING)", width_in=6.0)

    # Screenshot 5
    ss5_img = os.path.join(assets_dir, "05_constraint_rejection_test.png")
    add_image_figure(doc, ss5_img, "Figure 8: Database Engine Blocking Check Constraint Violation (Negative Amount Rejected with ORA-02290)", width_in=6.0)

    # Screenshot 6
    ss6_img = os.path.join(assets_dir, "06_main_script_execution.png")
    add_image_figure(doc, ss6_img, "Figure 9: Master Test Pipeline Completion Banner — 100% Automated Test Suite Passing Status", width_in=6.0)

    # SQL Developer Screenshots
    add_heading_2(doc, "26.1 SQL Developer Analytical Query Visualizations")
    ss_q1 = os.path.join(assets_dir, "oracle_ss_q1.png")
    add_image_figure(doc, ss_q1, "Figure 10: Oracle SQL Developer Execution Grid — Single-Row Customer Normalization Functions", width_in=6.0)

    ss_q4 = os.path.join(assets_dir, "oracle_ss_q4.png")
    add_image_figure(doc, ss_q4, "Figure 11: Oracle SQL Developer Master 6-Table Relational Dossier Output", width_in=6.0)

    # =========================================================================
    # SECTION 27: RESULTS AND DISCUSSION
    # =========================================================================
    add_heading_1(doc, "27. Results and Discussion")
    add_body(
        doc,
        "The FraudLens implementation passed all 13 documented test cases in the recorded execution run. These tests demonstrate "
        "the expected behavior of the selected operational workflows and constraint checks, without constituting exhaustive correctness verification:\n"
        "• Schema Integrity: All 8 tables, 8 sequences, 4 views, 3 procedures, 3 functions, and 2 triggers compiled without errors.\n"
        "• Constraint Robustness: All 71 integrity constraints operated deterministically. Negative tests 2.1 through 2.6 proved that "
        "negative amounts, duplicate emails, orphan accounts, inactive investigator assignments, and incomplete closures are trapped.\n"
        "• Transactional Control & Recovery: Master test scripts executed with transactional savepoints and clean rollbacks, verifying that "
        "operational data integrity is preserved during negative test failure and batch pipeline execution."
    )

    # =========================================================================
    # SECTION 28: ADVANTAGES AND LIMITATIONS
    # =========================================================================
    add_heading_1(doc, "28. Advantages and Limitations")
    add_heading_2(doc, "28.1 Advantages")
    add_bullet(doc, "Third Normal Form schema eliminates duplicate storage of customer and investigator demographics.", "Normalized Design: ")
    add_bullet(doc, "Integrity constraints (CHECK, UNIQUE, FK CASCADE) prevent invalid data entry at the database engine level.", "Database-Tier Enforcement: ")
    add_bullet(doc, "Automated threshold surveillance eliminates manual triage delays for high-value transactions.", "Procedural Automation: ")
    add_bullet(doc, "Row-level database triggers automatically record state transitions into dedicated audit tables, preserving chronological event history against application-tier alteration (while recognizing that privileged SYSDBA administrators retain database-level alteration authority).", "Trigger-Based Audit Logging: ")

    add_heading_2(doc, "28.2 Limitations")
    add_bullet(doc, "Thresholds (e.g. INR 50,000) are hardcoded and do not adapt dynamically to customer behavioral changes.", "Static Rule Thresholds: ")
    add_bullet(doc, "PL/SQL evaluates transactions after or during commit; it is not a distributed real-time streaming engine like Apache Flink.", "Batch/In-DB Processing: ")
    add_bullet(doc, "The current implementation runs on a single Oracle pluggable database rather than a globally distributed multi-region cluster.", "Single-Node Architecture: ")

    # =========================================================================
    # SECTION 29: FUTURE ENHANCEMENTS
    # =========================================================================
    add_heading_1(doc, "29. Future Enhancements")
    add_bullet(doc, "Integrate machine learning models (e.g. Isolation Forests, XGBoost) via Oracle Machine Learning (OML) for dynamic risk scoring.", "1. Machine Learning Integration: ")
    add_bullet(doc, "Incorporate graph database structures (Oracle Property Graph / Neo4j) to uncover cyclic fund routing and money-mule networks.", "2. Graph Database Modeling: ")
    add_bullet(doc, "Deploy Apache Kafka and Kafka Connect for real-time low-latency transaction ingestion and event streaming.", "3. Distributed Event Streaming: ")
    add_bullet(doc, "Incorporate biometric verification timestamps and device fingerprint hashes into the TRANSACTIONS table.", "4. Biometric & Device Forensics: ")

    # =========================================================================
    # SECTION 30: CONCLUSION
    # =========================================================================
    add_heading_1(doc, "30. Conclusion")
    add_body(
        doc,
        "FraudLens: Financial Transaction and Fraud Investigation Management System demonstrates the practical application of "
        "enterprise database management principles to modern financial security. Through rigorous Third Normal Form schema design, "
        "declarative constraints, procedural PL/SQL surveillance, analytical views, and autonomous audit triggers, FraudLens provides "
        "a resilient, auditable platform for transaction monitoring and forensic case management."
    )
    add_body(
        doc,
        "By executing against Oracle AI Database 26ai Free Release 23.26.3.0.0 and validating the 13 documented operational test cases, "
        "this project illustrates how foundational relational modeling and procedural constraints provide dependable operational integrity for transactional monitoring systems."
    )

    # =========================================================================
    # SECTION 31: REFERENCES
    # =========================================================================
    add_heading_1(doc, "31. References")
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
    for ref in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.15
        r = p_ref.add_run(ref)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = COLOR_TEXT

    # Save Document
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FraudLens_DBMS_Case_Study_Report.docx"))
    doc.save(output_path)
    print(f"[DOCX] Generated report successfully: {output_path}")

if __name__ == "__main__":
    generate_docx()
