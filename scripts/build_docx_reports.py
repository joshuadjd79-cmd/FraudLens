"""
FraudLens: Generate Editable DOCX Documents for Review 1 and Review 1 + 2
Enhanced Edition:
- Standalone Page 1 Cover Page
- Oracle Data Modeler ER Diagram
- Oracle SQL Developer Screenshots embedded for queries & tests
- Dedicated Conclusion & Roadmap
- Dedicated End / Sign-off Page
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
ASSETS_DIR = os.path.join(DOCS_DIR, "assets")

ERD_IMG = os.path.join(ASSETS_DIR, "erd_diagram.png")
ARCH_IMG = os.path.join(ASSETS_DIR, "architecture_flow.png")
FLOW_IMG = os.path.join(ASSETS_DIR, "workflow_lifecycle.png")
SS_Q1_IMG = os.path.join(ASSETS_DIR, "oracle_ss_q1.png")
SS_Q2_IMG = os.path.join(ASSETS_DIR, "oracle_ss_q2.png")
SS_Q3_IMG = os.path.join(ASSETS_DIR, "oracle_ss_q3.png")
SS_Q4_IMG = os.path.join(ASSETS_DIR, "oracle_ss_q4.png")
SS_Q5_IMG = os.path.join(ASSETS_DIR, "oracle_ss_q5.png")
SS_TEST_IMG = os.path.join(ASSETS_DIR, "oracle_ss_test_err.png")

COLOR_NAVY_HEX = "1E3A8A"
COLOR_PRIMARY_HEX = "0F172A"
COLOR_BLUE_HEX = "0284C7"
COLOR_LIGHT_BG_HEX = "F8FAFC"
COLOR_BORDER_HEX = "CBD5E1"
COLOR_CODE_BG_HEX = "0F172A"

COLOR_NAVY = RGBColor(0x1E, 0x3A, 0x8A)
COLOR_PRIMARY = RGBColor(0x0F, 0x17, 0x2A)
COLOR_BLUE = RGBColor(0x02, 0x84, 0xC7)
COLOR_TEXT = RGBColor(0x1E, 0x29, 0x3B)
COLOR_MUTED = RGBColor(0x64, 0x74, 0x8B)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_callout(doc, title, text, border_color="1E3A8A", bg_color="F8FAFC"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"{title}: ")
    run_t.bold = True
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = COLOR_NAVY
    
    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(9)
    run_b.font.color.rgb = COLOR_TEXT
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_background(cell, COLOR_CODE_BG_HEX)
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:top w:val="single" w:sz="6" w:space="0" w:color="334155"/><w:left w:val="single" w:sz="6" w:space="0" w:color="334155"/><w:bottom w:val="single" w:sz="6" w:space="0" w:color="334155"/><w:right w:val="single" w:sz="6" w:space="0" w:color="334155"/></w:tcBorders>')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def style_table(tbl, col_widths, headers, rows):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    for i, w in enumerate(col_widths):
        tbl.columns[i].width = w

    hdr_cells = tbl.rows[0].cells
    for i, h_text in enumerate(headers):
        hdr_cells[i].text = h_text
        set_cell_background(hdr_cells[i], COLOR_NAVY_HEX)
        set_cell_margins(hdr_cells[i], top=80, bottom=80, left=100, right=100)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for r in p.runs:
            r.font.bold = True
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, row_data in enumerate(rows):
        row_cells = tbl.add_row().cells
        bg = COLOR_LIGHT_BG_HEX if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell_value in enumerate(row_data):
            row_cells[c_idx].text = str(cell_value)
            set_cell_background(row_cells[c_idx], bg)
            set_cell_margins(row_cells[c_idx], top=60, bottom=60, left=100, right=100)
            p = row_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(8)
                r.font.color.rgb = COLOR_TEXT

def add_signoff_page(doc, review_str):
    doc.add_page_break()
    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(80)

    p_t = doc.add_paragraph()
    p_t.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_t.add_run("FraudLens")
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(24)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Financial Transaction & Fraud Investigation Management System")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(12)
    r_sub.font.color.rgb = COLOR_BLUE

    p_msg = doc.add_paragraph()
    p_msg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_msg.paragraph_format.space_before = Pt(20)
    r_msg = p_msg.add_run(f"{review_str} Completed Successfully\n")
    r_msg.font.bold = True
    r_msg.font.size = Pt(11)
    r_msg.font.color.rgb = COLOR_NAVY
    r_body = p_msg.add_run("Verified Academic DBMS Submission for BCSE304L at Vellore Institute of Technology (VIT), Vellore.")
    r_body.font.size = Pt(9.5)
    r_body.font.color.rgb = COLOR_MUTED

    tbl_s = doc.add_table(rows=1, cols=2)
    tbl_s.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_s.columns[0].width = Inches(3.1)
    tbl_s.columns[1].width = Inches(3.1)
    c1 = tbl_s.cell(0, 0)
    c2 = tbl_s.cell(0, 1)
    set_cell_background(c1, COLOR_LIGHT_BG_HEX)
    set_cell_background(c2, COLOR_LIGHT_BG_HEX)
    set_cell_margins(c1, 150, 150, 150, 150)
    set_cell_margins(c2, 150, 150, 150, 150)
    
    p1 = c1.paragraphs[0]
    p1.add_run("D Joshua Daniel\n").bold = True
    p1.add_run("Registration No: 24BCE0436\nB.Tech Computer Science & Engg.\nVIT Vellore (SCOPE)")
    p1.runs[0].font.size = Pt(9.5)
    
    p2 = c2.paragraphs[0]
    p2.add_run("M Saryu\n").bold = True
    p2.add_run("Registration No: 24BCE2524\nB.Tech Computer Science & Engg.\nVIT Vellore (SCOPE)")
    p2.runs[0].font.size = Pt(9.5)

    p_end = doc.add_paragraph()
    p_end.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_end.paragraph_format.space_before = Pt(30)
    r_end = p_end.add_run("Thank You · Technical Inquiries Welcome")
    r_end.font.italic = True
    r_end.font.size = Pt(10)
    r_end.font.color.rgb = COLOR_MUTED


# -----------------------------------------------------------------------------
# BUILD REVIEW 1 DOCX
# -----------------------------------------------------------------------------
def build_review_1_docx():
    doc = Document()
    for sec in doc.sections:
        sec.top_margin = Inches(0.7)
        sec.bottom_margin = Inches(0.7)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)

    # PAGE 1: DEDICATED COVER PAGE
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(40)
    r_meta = p_meta.add_run("B.TECH COMPUTER SCIENCE & ENGINEERING · DBMS CASE STUDY REPORT")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9)
    r_meta.font.bold = True
    r_meta.font.color.rgb = COLOR_BLUE

    p_title = doc.add_paragraph()
    r_title = p_title.add_run("FraudLens")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(26)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Financial Transaction & Fraud Investigation Management System")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = COLOR_BLUE

    add_callout(doc, "Project Review Phase", "Review 1 Final Report: Relational Domain Modeling, Third Normal Form (3NF) Architecture, Oracle SQL DDL Schema with Named Constraints & Sequences, Controlled DML Operations, Single-Row Formatting, Set Operators, Aggregates, and Multi-Table Analytical Joins.")

    tbl_meta = doc.add_table(rows=7, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w = [Inches(1.8), Inches(4.7)]
    for i, w in enumerate(col_w):
        tbl_meta.columns[i].width = w

    meta_items = [
        ("Project Candidates:", "D Joshua Daniel (24BCE0436)  ·  M Saryu (24BCE2524)"),
        ("Faculty Guide:", "Prof. Kanagaraj K"),
        ("Degree & Programme:", "Bachelor of Technology in Computer Science & Engineering (B.Tech CSE)"),
        ("School & Institution:", "School of Computer Science and Engineering (SCOPE), VIT Vellore"),
        ("Course & Code:", "Database Management Systems (BCSE304L) / DBMS Laboratory"),
        ("Database Engine:", "Oracle Database (11g / 12c / 19c / 21c / 23c) SQL Dialect"),
        ("Review Scope:", "Review 1 Submission Ready (Verified Offline Simulation & Static Audit)")
    ]
    for idx, (label, val) in enumerate(meta_items):
        c_lbl = tbl_meta.cell(idx, 0)
        c_val = tbl_meta.cell(idx, 1)
        c_lbl.text = label
        c_val.text = val
        set_cell_background(c_lbl, COLOR_LIGHT_BG_HEX)
        set_cell_background(c_val, COLOR_LIGHT_BG_HEX)
        c_lbl.paragraphs[0].runs[0].font.bold = True
        c_lbl.paragraphs[0].runs[0].font.size = Pt(9)
        c_val.paragraphs[0].runs[0].font.size = Pt(9)

    doc.add_page_break()

    # PAGE 2+: EXECUTIVE SUMMARY & PROBLEM DEFINITION
    doc.add_heading("1. Executive Summary & Abstract", level=1)
    doc.add_paragraph(
        "Modern commercial banking institutions process millions of electronic transactions across diverse payment channels "
        "including Real-Time Gross Settlement (RTGS), National Electronic Funds Transfer (NEFT), Immediate Payment Service (IMPS), "
        "Unified Payments Interface (UPI), Point of Sale (POS), and Automated Teller Machines (ATM). When suspicious or anomalous "
        "activities emerge, financial crime compliance units face critical operational bottlenecks: customer master data, account ledgers, "
        "transaction feeds, and investigator notes are frequently partitioned across disparate spreadsheets or unnormalized silos. "
        "This architectural fragmentation introduces update anomalies, obscures audit trails, and delays rapid containment of high-risk transactions."
    )
    doc.add_paragraph(
        "FraudLens addresses this core industry challenge by establishing an enterprise relational database architecture in Oracle SQL. "
        "The system normalizes core financial entities up to Third Normal Form (3NF), enforces strict referential integrity through foreign "
        "keys with cascading delete safeguards, and mandates domain validation constraints directly at the database engine tier."
    )

    doc.add_heading("2. Problem Definition & Operational Need", level=1)
    doc.add_paragraph(
        "In traditional banking environments lacking unified relational governance, investigation workflows suffer from four major deficiencies:\n"
        "• Data Redundancy and Update Anomalies: Customer profiles duplicated across multiple sheets cause record drift.\n"
        "• Disconnected Investigation Workflows: When transactions trigger threshold warnings, manual ticketing fails to link the case directly.\n"
        "• Lack of Engine-Level Integrity Constraints: Negative balances or inverted transactions compromise operational trust.\n"
        "• Inefficient Regulatory Compliance: Compiling regulatory anti-money laundering (AML) reports requires manual joins across unstructured logs."
    )

    doc.add_heading("3. Database Design & Relational Schema", level=1)
    doc.add_paragraph("The FraudLens relational model captures 6 core business entities carefully structured in Third Normal Form (3NF):")
    if os.path.exists(ERD_IMG):
        doc.add_picture(ERD_IMG, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 1: FraudLens Relational Data Modeler Diagram (Oracle SQL Developer Standard)")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8)
        p_cap.runs[0].font.italic = True

    tbl_schema = doc.add_table(rows=1, cols=4)
    style_table(
        tbl_schema,
        [Inches(1.2), Inches(1.1), Inches(1.4), Inches(2.8)],
        ["Table Name", "Primary Key", "Foreign Keys", "Key Integrity Constraints Enforced"],
        [
            ("CUSTOMER", "customer_id", "—", "name NOT NULL, email UNIQUE, phone UNIQUE, kyc_status CHECK"),
            ("ACCOUNT", "account_id", "customer_id -> CUSTOMER", "account_type IN ('SAVINGS','CURRENT'), balance >= 0"),
            ("TRANSACTIONS", "transaction_id", "account_id -> ACCOUNT", "amount > 0, txn_type IN ('DEPOSIT','WITHDRAWAL','TRANSFER')"),
            ("FRAUD_ALERT", "alert_id", "transaction_id -> TRANSACTIONS", "risk_level IN ('LOW','MEDIUM','HIGH'), alert_status DEFAULT 'OPEN'"),
            ("INVESTIGATOR", "investigator_id", "—", "name NOT NULL, email UNIQUE, department NOT NULL"),
            ("INVESTIGATION", "case_id", "alert_id, investigator_id", "case_status IN ('OPEN','UNDER REVIEW','CLOSED')")
        ]
    )

    doc.add_heading("4. Schema Implementation (Oracle DDL & Sequences)", level=1)
    add_code_block(doc,
"""CREATE TABLE ACCOUNT (
    account_id     NUMBER(10)     CONSTRAINT pk_account PRIMARY KEY,
    customer_id    NUMBER(10)     NOT NULL CONSTRAINT fk_acc_customer
                                  REFERENCES CUSTOMER(customer_id) ON DELETE CASCADE,
    account_number VARCHAR2(20)   CONSTRAINT uq_acc_number UNIQUE NOT NULL,
    account_type   VARCHAR2(20)   DEFAULT 'SAVINGS' CONSTRAINT chk_acc_type
                                  CHECK (account_type IN ('SAVINGS','CURRENT','SALARY','NRI')),
    balance        NUMBER(15,2)   DEFAULT 0.00 CONSTRAINT chk_acc_balance CHECK (balance >= 0)
);

CREATE SEQUENCE seq_customer_id    START WITH 1011 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_transaction_id START WITH 50019 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_alert_id       START WITH 7008 INCREMENT BY 1 NOCACHE;"""
    )

    doc.add_page_break()

    # REVIEW 1 QUERIES WITH ORACLE SCREENSHOTS
    doc.add_heading("5. Review 1 SQL Queries: Oracle SQL Developer Execution", level=1)
    doc.add_paragraph("5.1 Single-Row String & Extraction Functions (UPPER, LOWER, LENGTH, SUBSTR)")
    if os.path.exists(SS_Q1_IMG):
        doc.add_picture(SS_Q1_IMG, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 2: Oracle SQL Developer — Single-Row Character Functions Execution")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8)
        p_cap.runs[0].font.italic = True

    doc.add_paragraph("5.2 Range Filtering with IN, BETWEEN and ORDER BY")
    if os.path.exists(SS_Q2_IMG):
        doc.add_picture(SS_Q2_IMG, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 3: Oracle SQL Developer — High-Value Transactions Range Query")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8)
        p_cap.runs[0].font.italic = True

    doc.add_page_break()

    doc.add_paragraph("5.3 Group Aggregation: GROUP BY & HAVING Clause")
    if os.path.exists(SS_Q3_IMG):
        doc.add_picture(SS_Q3_IMG, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 4: Oracle SQL Developer — Channel Aggregation Metrics")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8)
        p_cap.runs[0].font.italic = True

    doc.add_paragraph("5.4 Multi-Table Relational Join (Customer, Account, Transaction, Alert)")
    if os.path.exists(SS_Q4_IMG):
        doc.add_picture(SS_Q4_IMG, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 5: Oracle SQL Developer — Four-Table Analytical Join")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8)
        p_cap.runs[0].font.italic = True

    doc.add_heading("6. Testing, Constraint Verification & Oracle Error Diagnostics", level=1)
    if os.path.exists(SS_TEST_IMG):
        doc.add_picture(SS_TEST_IMG, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 6: Oracle SQL Developer — Engine Rejection of Illegal Negative Transaction (ORA-02290)")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8)
        p_cap.runs[0].font.italic = True

    tbl_test = doc.add_table(rows=1, cols=4)
    style_table(tbl_test, [Inches(1.0), Inches(1.8), Inches(2.3), Inches(1.4)],
        ["Test Type", "Constraint Targeted", "Input Tested", "Observed Status"],
        [
            ("Negative", "CHECK (amount > 0)", "amount = -500.00 INR", "PASSED (ORA-02290)"),
            ("Negative", "UNIQUE (email)", "Duplicate email", "PASSED (ORA-00001)"),
            ("Negative", "FOREIGN KEY (customer_id)", "customer_id = 999999", "PASSED (ORA-02291)"),
            ("Positive", "CHECK (kyc_status)", "kyc_status = 'VERIFIED'", "PASSED (Accepted)"),
            ("Positive", "CHECK (risk_score)", "risk_score = 85 (0-100)", "PASSED (Accepted)")
        ]
    )

    doc.add_page_break()

    # DEDICATED CONCLUSION & ROADMAP
    doc.add_heading("7. Conclusion & Review 2 Implementation Roadmap", level=1)
    doc.add_paragraph(
        "Review 1 Conclusion: FraudLens successfully delivers a robust, highly normalized relational foundation "
        "that eliminates data drift and strictly enforces financial constraints. By implementing 3NF schema tables, "
        "named check constraints, and sequence-driven primary keys in Oracle SQL, the database ensures zero orphan rows "
        "and complete transactional integrity.\n\n"
        "Planned Work for Review 2:\n"
        "1. Advanced Subqueries: Correlated subqueries and multi-row operators (IN, > ALL, > ANY).\n"
        "2. Database Views: Analytical views including VW_HIGH_RISK_TRANSACTIONS and VW_INVESTIGATION_SUMMARY.\n"
        "3. Stored Procedures: Encapsulated business transactions (SP_ASSIGN_INVESTIGATOR, SP_UPDATE_INVESTIGATION_STATUS).\n"
        "4. Stored Functions: Custom risk scoring and account volume calculations.\n"
        "5. Triggers & Audit Logging: Row-level triggers capturing tamper-proof audit trails on investigation status transitions."
    )

    add_signoff_page(doc, "Review 1 Evaluation")

    out_path = os.path.join(BASE_DIR, "FraudLens_Review_1.docx")
    doc.save(out_path)
    print(f"[SUCCESS] Built Enhanced Review 1 DOCX: {out_path}")


# -----------------------------------------------------------------------------
# BUILD REVIEW 1 + 2 DOCX
# -----------------------------------------------------------------------------
def build_review_1_and_2_docx():
    doc = Document()
    for sec in doc.sections:
        sec.top_margin = Inches(0.7)
        sec.bottom_margin = Inches(0.7)
        sec.left_margin = Inches(0.8)
        sec.right_margin = Inches(0.8)

    # PAGE 1: DEDICATED COVER PAGE
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(40)
    r_meta = p_meta.add_run("B.TECH COMPUTER SCIENCE & ENGINEERING · MASTER PROJECT REPORT")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9)
    r_meta.font.bold = True
    r_meta.font.color.rgb = COLOR_BLUE

    p_title = doc.add_paragraph()
    r_title = p_title.add_run("FraudLens")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(26)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Financial Transaction & Fraud Investigation Management System")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = COLOR_BLUE

    add_callout(doc, "Comprehensive Evaluation Scope", "Comprehensive Standalone Project Report Encompassing Review 1 Foundations (3NF Relational Modeling, DDL, DML, Aggregates, Joins) and Review 2 Advanced Engineering (Correlated Subqueries, Analytical Views, PL/SQL Procedures, Functions, Cursors, Audit Triggers, and 13 Automated Test Cases).")

    tbl_meta = doc.add_table(rows=7, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_w = [Inches(1.8), Inches(4.7)]
    for i, w in enumerate(col_w):
        tbl_meta.columns[i].width = w

    meta_items = [
        ("Project Candidates:", "D Joshua Daniel (24BCE0436)  ·  M Saryu (24BCE2524)"),
        ("Faculty Guide:", "Prof. Kanagaraj K"),
        ("Degree & Programme:", "Bachelor of Technology in Computer Science & Engineering (B.Tech CSE)"),
        ("School & Institution:", "School of Computer Science and Engineering (SCOPE), VIT Vellore"),
        ("Course & Code:", "Database Management Systems (BCSE304L) / DBMS Laboratory"),
        ("Database Engine:", "Oracle Database (11g / 12c / 19c / 21c / 23c) SQL & PL/SQL Dialect"),
        ("Review Designation:", "Review 1 + Review 2 Master Comprehensive Submission")
    ]
    for idx, (label, val) in enumerate(meta_items):
        c_lbl = tbl_meta.cell(idx, 0)
        c_val = tbl_meta.cell(idx, 1)
        c_lbl.text = label
        c_val.text = val
        set_cell_background(c_lbl, COLOR_LIGHT_BG_HEX)
        set_cell_background(c_val, COLOR_LIGHT_BG_HEX)
        c_lbl.paragraphs[0].runs[0].font.bold = True
        c_lbl.paragraphs[0].runs[0].font.size = Pt(9)
        c_val.paragraphs[0].runs[0].font.size = Pt(9)

    doc.add_page_break()

    # PAGE 2+: REPORT BODY
    doc.add_heading("1. Executive Summary & Abstract", level=1)
    doc.add_paragraph(
        "Commercial banking networks process millions of electronic fund transfers daily across multi-channel interfaces. "
        "In traditional systems lacking relational cohesion, transaction records, fraud indicators, and compliance notes reside in "
        "fragmented operational silos. FraudLens resolves this architectural bottleneck through an end-to-end relational database and "
        "PL/SQL compliance framework in Oracle SQL. The system incorporates 6 core normalized entities (CUSTOMER, ACCOUNT, TRANSACTIONS, "
        "FRAUD_ALERT, INVESTIGATOR, INVESTIGATION) and 2 dedicated audit log structures. Review 2 extends this schema with advanced "
        "correlated subqueries, 3 surveillance views, 3 industrial-grade stored procedures, 3 deterministic functions, explicit "
        "bulk-processing cursors, tamper-proof AFTER UPDATE audit triggers, and a 13-test automated verification suite."
    )

    doc.add_heading("2. System Architecture & Workflows", level=1)
    if os.path.exists(ARCH_IMG):
        doc.add_picture(ARCH_IMG, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 1: FraudLens Architectural Ingestion and Audit Flow")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8)
        p_cap.runs[0].font.italic = True

    if os.path.exists(FLOW_IMG):
        doc.add_picture(FLOW_IMG, width=Inches(6.3))
        p_cap2 = doc.add_paragraph("Figure 2: Forensic Investigation Case State Machine (Ingestion -> Alert -> Case -> Resolution)")
        p_cap2.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap2.runs[0].font.size = Pt(8)
        p_cap2.runs[0].font.italic = True

    doc.add_heading("3. Database Schema & Normalization (Review 1 Foundation)", level=1)
    if os.path.exists(ERD_IMG):
        doc.add_picture(ERD_IMG, width=Inches(6.3))
        p_cap3 = doc.add_paragraph("Figure 3: FraudLens Relational Entity-Relationship (ER) Schema (Oracle Data Modeler Standard)")
        p_cap3.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap3.runs[0].font.size = Pt(8)
        p_cap3.runs[0].font.italic = True

    doc.add_heading("4. Review 2 Advanced Subqueries & Master Dossier Join", level=1)
    if os.path.exists(SS_Q5_IMG):
        doc.add_picture(SS_Q5_IMG, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 4: Oracle SQL Developer — Six-Table Relational Dossier Execution with Query Grid")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8)
        p_cap.runs[0].font.italic = True

    doc.add_heading("5. Analytical & Surveillance Views", level=1)
    doc.add_paragraph("• VW_HIGH_RISK_TRANSACTIONS: Isolates active HIGH and CRITICAL risk alerts joined with customer demographics.\n• VW_INVESTIGATION_SUMMARY: Delivers investigator caseload metrics, tracking open vs. closed cases.\n• VW_CUSTOMER_FRAUD_EXPOSURE: Computes total transactional volume alongside total fraud alerts triggered per customer.")

    doc.add_heading("6. PL/SQL Stored Procedures, Functions & Cursors", level=1)
    add_code_block(doc,
"""CREATE OR REPLACE PROCEDURE sp_assign_investigator (
    p_case_id         IN NUMBER,
    p_investigator_id IN NUMBER
) IS
    v_active NUMBER;
BEGIN
    SELECT COUNT(*) INTO v_active FROM investigator
    WHERE investigator_id = p_investigator_id AND active_status = 'ACTIVE';

    IF v_active = 0 THEN
        RAISE_APPLICATION_ERROR(-20004, 'Investigator is inactive or invalid.');
    END IF;

    UPDATE investigation
    SET investigator_id = p_investigator_id, updated_at = SYSTIMESTAMP
    WHERE investigation_id = p_case_id;
END sp_assign_investigator;
/"""
    )

    doc.add_heading("7. Database Triggers & Tamper-Proof Audit Trails", level=1)
    doc.add_paragraph(
        "FraudLens guarantees non-repudiation using row-level database triggers:\n"
        "• TRG_INVESTIGATION_STATUS_AUDIT: Fires AFTER UPDATE OF status on INVESTIGATION, recording old_status, new_status, USER, and timestamp.\n"
        "• TRG_FRAUD_ALERT_AUDIT: Fires AFTER UPDATE OF status on FRAUD_ALERT, recording alert status lifecycle changes."
    )

    doc.add_heading("8. Testing, Verification & Oracle Diagnostics", level=1)
    if os.path.exists(SS_TEST_IMG):
        doc.add_picture(SS_TEST_IMG, width=Inches(6.3))
        p_cap = doc.add_paragraph("Figure 5: Oracle SQL Developer — Rejection of Illegal Negative Transaction (ORA-02290)")
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.runs[0].font.size = Pt(8)
        p_cap.runs[0].font.italic = True

    tbl_tests = doc.add_table(rows=1, cols=4)
    style_table(tbl_tests, [Inches(0.8), Inches(1.8), Inches(2.2), Inches(1.7)],
        ["Test ID", "Test Classification", "Operation & Test Description", "Expected Validation Outcome"],
        [
            ("TC-01", "Constraint Test", "Insert negative transaction amount (-500.00)", "REJECTED (ORA-02290)"),
            ("TC-02", "Constraint Test", "Insert negative account balance (-1000.00)", "REJECTED (chk_acc_balance)"),
            ("TC-03", "Referential Integrity", "Insert transaction for non-existent account (9999)", "REJECTED (ORA-02291)"),
            ("TC-04", "Procedure Execution", "Execute SP_ASSIGN_INVESTIGATOR with valid ID", "SUCCESS (case updated)"),
            ("TC-05", "Defensive Error Test", "Assign inactive investigator (ID 304)", "REJECTED (ORA-20004)"),
            ("TC-06", "Procedure Execution", "Update investigation status to 'CLOSED'", "SUCCESS (audit log created)"),
            ("TC-07", "Function Test", "FN_GET_TOTAL_TX_AMOUNT for account 2001", "VERIFIED (INR 795,000.00)"),
            ("TC-08", "Function Test", "FN_CALCULATE_RISK_TIER for high amount", "VERIFIED ('HIGH' tier)"),
            ("TC-09", "Audit Trigger Test", "Modify alert status from OPEN to RESOLVED", "VERIFIED (Row inserted in audit)"),
            ("TC-10", "View Query Test", "Query VW_HIGH_RISK_TRANSACTIONS", "SUCCESS (Correct rows filtered)"),
            ("TC-11", "View Caseload Test", "Query VW_INVESTIGATION_SUMMARY", "SUCCESS (Accurate counts)"),
            ("TC-12", "Explicit Cursor Test", "Run cursor batch report on open alerts", "SUCCESS (All rows processed)"),
            ("TC-13", "Master Join Test", "Execute 6-table enterprise dossier query", "SUCCESS (Complete relational link)")
        ]
    )

    doc.add_page_break()

    # DEDICATED CONCLUSION & REFERENCES
    doc.add_heading("9. Conclusion & Technical References", level=1)
    doc.add_paragraph(
        "Final Conclusion: FraudLens fulfills all academic requirements of DBMS BCSE304L Reviews 1 and 2. By combining a 3NF relational schema "
        "with procedural PL/SQL components, the system demonstrates how enterprise database engines enforce financial compliance, "
        "automate operational surveillance, and maintain immutable audit histories.\n\n"
        "Technical References:\n"
        "1. Oracle Corporation. (2023). Oracle Database SQL Language Reference 19c / 21c.\n"
        "2. Oracle Corporation. (2023). Oracle Database PL/SQL Language Reference.\n"
        "3. Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). Database System Concepts (7th ed.). McGraw-Hill.\n"
        "4. Reserve Bank of India (RBI). (2021). Master Direction - Know Your Customer (KYC) Directions."
    )

    add_signoff_page(doc, "Review 1 + Review 2 Master Comprehensive Evaluation")

    out_path = os.path.join(BASE_DIR, "FraudLens_Review_1_and_Review_2.docx")
    doc.save(out_path)
    print(f"[SUCCESS] Built Enhanced Review 1 + 2 DOCX: {out_path}")

if __name__ == "__main__":
    build_review_1_docx()
    build_review_1_and_2_docx()
