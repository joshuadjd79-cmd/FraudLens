"""
FraudLens: Generate Audit and Corrections Report PDF
Builds FraudLens_Report_Audit_and_Corrections.pdf via ReportLab in A4 format.
Provides a comprehensive audit matrix, severity classifications,
technical discrepancy resolutions, and pre-submission checklist.
"""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

C_NAVY = colors.HexColor("#1E3A8A")
C_BLUE = colors.HexColor("#0284C7")
C_SLATE = colors.HexColor("#0F172A")
C_TEXT = colors.HexColor("#1E293B")
C_MUTED = colors.HexColor("#64748B")
C_LIGHT_BG = colors.HexColor("#F8FAFC")
C_BORDER = colors.HexColor("#CBD5E1")
C_RED = colors.HexColor("#DC2626")
C_AMBER = colors.HexColor("#D97706")
C_GREEN = colors.HexColor("#16A34A")
WHITE = colors.HexColor("#FFFFFF")

PAGE_W, PAGE_H = A4
MARGIN = 45.0
PRINT_W = PAGE_W - (2 * MARGIN)

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
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.6)
            self.line(MARGIN, PAGE_H - 36, PAGE_W - MARGIN, PAGE_H - 36)

            self.setFont("Helvetica-Bold", 7.5)
            self.setFillColor(C_NAVY)
            self.drawString(MARGIN, PAGE_H - 30, "FRAUDLENS: TECHNICAL AUDIT & CORRECTION REPORT")

            self.setFont("Helvetica", 7.5)
            self.setFillColor(C_MUTED)
            self.drawRightString(PAGE_W - MARGIN, PAGE_H - 30, "ACADEMIC QA REVIEW")

            self.line(MARGIN, 38, PAGE_W - MARGIN, 38)
            self.setFont("Helvetica", 8)
            self.setFillColor(C_MUTED)
            self.drawString(MARGIN, 26, "Vellore Institute of Technology | D Joshua Daniel (24BCE0436) & M Saryu (24BCE2524)")

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
        fontName='Helvetica-Bold', fontSize=22, leading=28,
        textColor=C_NAVY, alignment=1
    )
    styles['TitleSub'] = ParagraphStyle(
        'TitleSub', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=16,
        textColor=C_BLUE, alignment=1
    )
    styles['MetaBox'] = ParagraphStyle(
        'MetaBox', parent=base['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=C_TEXT
    )
    styles['H1'] = ParagraphStyle(
        'H1', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=13, leading=17,
        textColor=C_NAVY, spaceBefore=12, spaceAfter=5,
        keepWithNext=True
    )
    styles['H2'] = ParagraphStyle(
        'H2', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=C_BLUE, spaceBefore=9, spaceAfter=3,
        keepWithNext=True
    )
    styles['Body'] = ParagraphStyle(
        'Body', parent=base['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=C_TEXT, spaceAfter=4
    )
    styles['Bullet'] = ParagraphStyle(
        'Bullet', parent=base['Normal'],
        fontName='Helvetica', fontSize=8.2, leading=11.5,
        textColor=C_TEXT, leftIndent=10, firstLineIndent=-6, spaceAfter=2.5
    )
    styles['TH'] = ParagraphStyle(
        'TH', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=7.5, leading=9.5,
        textColor=WHITE, alignment=1
    )
    styles['TD'] = ParagraphStyle(
        'TD', parent=base['Normal'],
        fontName='Helvetica', fontSize=7, leading=9,
        textColor=C_TEXT
    )
    styles['TDBold'] = ParagraphStyle(
        'TDBold', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=7, leading=9,
        textColor=C_SLATE
    )
    styles['TDCritical'] = ParagraphStyle(
        'TDCritical', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=7, leading=9,
        textColor=C_RED, alignment=1
    )
    styles['TDMajor'] = ParagraphStyle(
        'TDMajor', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=7, leading=9,
        textColor=C_AMBER, alignment=1
    )
    styles['TDMinor'] = ParagraphStyle(
        'TDMinor', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=7, leading=9,
        textColor=C_BLUE, alignment=1
    )
    styles['TDVerified'] = ParagraphStyle(
        'TDVerified', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=7, leading=9,
        textColor=C_GREEN, alignment=1
    )
    styles['TDMono'] = ParagraphStyle(
        'TDMono', parent=base['Normal'],
        fontName='Courier', fontSize=6.5, leading=8.5,
        textColor=C_TEXT
    )
    return styles

STYLES = setup_styles()

AUDIT_FINDINGS = [
    {
        "loc": "Cover, Sec 8, 9",
        "issue": "OS stated as Windows 11 Professional, but host system is Windows 11 Home Single Language (Build 26200). Hardware listed as 16 GB RAM / Core i7 without distinguishing host vs minimum/recommended.",
        "sev": "Major",
        "fix": "Corrected host OS to Windows 11 Home Single Language. Added explicit distinction between actual host specs (Core i3-1115G4, 8 GB RAM), minimum specs (Dual Core, 4 GB), and recommended enterprise specs (16 GB RAM).",
        "status": "Verified & Corrected"
    },
    {
        "loc": "Cover, Sec 1",
        "issue": "Academic year specified as 2025–2026, but report is dated October 2026. Potential ambiguity between 2025–2026 and 2026–2027 curriculum calendars.",
        "sev": "Major",
        "fix": "Per student instructions, removed Academic Year field entirely from all report cover pages, metadata boxes, and submission verification sheets to prevent calendar ambiguity.",
        "status": "Verified & Removed"
    },
    {
        "loc": "Sec 2, 7, 28",
        "issue": "Exaggerated claims describing FraudLens as 'production-grade', 'tamper-proof', 'unalterable', and achieving '100% security' in an enterprise banking environment.",
        "sev": "Critical",
        "fix": "Replaced hyperbolic marketing terms with rigorous academic terminology. Reclassified system as a comprehensive academic prototype demonstrating enterprise DBMS principles. Clarified trigger auditing vs DBA superuser limitations.",
        "status": "Verified & Corrected"
    },
    {
        "loc": "Sec 11, 14, 20",
        "issue": "Cardinality discrepancy: ER diagram states TRANSACTIONS to FRAUD_ALERT is 1:N, but SP_EVALUATE_AND_ALERT_TRANSACTION enforces a check preventing multiple alerts for the same transaction.",
        "sev": "Critical",
        "fix": "Reconciled duality: explained that the relational schema DDL structurally allows 1:N (foreign key is non-unique to accommodate multiple distinct rule engines), but the current procedure implementation includes a 1:1 guard against duplicate alerts.",
        "status": "Verified & Corrected"
    },
    {
        "loc": "Sec 22",
        "issue": "Audit triggers claimed to provide 'tamper-proof' and 'unalterable' logging, ignoring that privileged database users (SYSDBA / DBA) can alter or truncate tables.",
        "sev": "Major",
        "fix": "Clarified that triggers guarantee application-level non-repudiation against standard user sessions, but enterprise compliance requires Oracle Blockchain Tables or hardware WORM storage for DBA-level immutability.",
        "status": "Verified & Corrected"
    },
    {
        "loc": "Sec 14, 15",
        "issue": "Use of ON DELETE CASCADE on ACCOUNT and TRANSACTIONS not critically evaluated against real-world banking compliance (RBI/FATF retention rules).",
        "sev": "Major",
        "fix": "Added academic evaluation explaining that cascading deletes demonstrate relational referential integrity in a prototype, but real banking systems prohibit physical record deletion and enforce soft deletes with ON DELETE RESTRICT.",
        "status": "Verified & Corrected"
    },
    {
        "loc": "Sec 13",
        "issue": "Normalization section claimed schema is in 3NF solely because primary keys are single columns, which is logically incomplete.",
        "sev": "Critical",
        "fix": "Rewrote normalization proofs with complete mathematical rigor, analyzing non-prime functional dependencies for each table and demonstrating the absence of both partial and transitive dependencies.",
        "status": "Verified & Corrected"
    },
    {
        "loc": "Sec 15",
        "issue": "Statement of 71 constraints repeated without explaining how Oracle arrives at 53 CHECK constraints when only 17 explicit business rule CHECK constraints exist.",
        "sev": "Major",
        "fix": "Detailed exact composition from Oracle USER_CONSTRAINTS: 17 explicit domain CHECK constraints + 36 column NOT NULL integrity checks = 53 type 'C' constraints, plus 8 PK, 5 FK, and 5 UK, totalling exactly 71.",
        "status": "Verified & Corrected"
    },
    {
        "loc": "Sec 23",
        "issue": "Report discussed 6 fraud rules as if all were active procedural features, whereas only the HIGH_AMOUNT (> 50k) rule is automated via stored procedure.",
        "sev": "Critical",
        "fix": "Clarified that only the HIGH_AMOUNT rule is procedurally automated; the other 5 rules (velocity, channel, off-hours, cross-border, structuring) exist in the check constraint enum and sample data, representing future enhancements.",
        "status": "Verified & Corrected"
    },
    {
        "loc": "Sec 25, 27",
        "issue": "Report claimed '100% success rate' in terms that could imply complete bug-free correctness rather than all included tests passing.",
        "sev": "Major",
        "fix": "Revised phrasing to exact scientific language: 'All 13 included test cases passed in the recorded execution run without compile or runtime errors', distinguishing test suite passing from production readiness.",
        "status": "Verified & Corrected"
    },
    {
        "loc": "Sec 2, 4, 23",
        "issue": "Distinction between an automated alert and legal proof of fraud needed stronger, repeated emphasis across analytical sections.",
        "sev": "Major",
        "fix": "Reinforced the core principle throughout Sections 2, 4, 7, 23, and 24: an automated alert is an investigative anomaly indicator, not evidence of criminal guilt.",
        "status": "Verified & Corrected"
    },
    {
        "loc": "Sec 26",
        "issue": "Visual evidence needed verification to ensure that all 8 embedded figures contain genuine, un-fabricated execution screenshots from the active Oracle 26ai environment.",
        "sev": "Critical",
        "fix": "Verified all screenshots against genuine output files in evidence/oracle/ (01 to 06) and docs/assets/ (Q1 to Q5). Captions accurately reflect console and SQL Developer executions.",
        "status": "Verified & Corrected"
    },
    {
        "loc": "Sec 31",
        "issue": "References needed standardized academic formatting and explicit citations for regulatory guidelines (RBI KYC Master Direction, FATF guidance).",
        "sev": "Minor",
        "fix": "Standardized references according to APA/IEEE format, including full textbook editions (Silberschatz 7th ed., Elmasri 7th ed.) and authentic regulatory documentation references.",
        "status": "Verified & Corrected"
    },
    {
        "loc": "TOC & Pagination",
        "issue": "Table of Contents page numbers in initial draft required precise alignment with actual generated page positions.",
        "sev": "Minor",
        "fix": "Reconciled and synchronized all 31 section page mappings in the Table of Contents to match exact physical page layout in the 20-page document.",
        "status": "Verified & Corrected"
    }
]

def generate_audit_pdf():
    output_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "FraudLens_Report_Audit_and_Corrections.pdf"))
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=MARGIN
    )

    story = []

    # Title & Metadata
    story.append(Spacer(1, 10))
    story.append(Paragraph("FRAUDLENS: TECHNICAL REPORT AUDIT & CORRECTIONS", STYLES['TitleMain']))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Comprehensive Academic Quality Assurance Review & Discrepancy Reconciliation", STYLES['TitleSub']))
    story.append(Spacer(1, 12))

    meta_content = [
        [Paragraph("<b>Target Document:</b>", STYLES['TDBold']), Paragraph("FraudLens_DBMS_Case_Study_Report_Final.pdf", STYLES['TD']),
         Paragraph("<b>Date of Audit:</b>", STYLES['TDBold']), Paragraph("26-OCT-2026", STYLES['TD'])],
        [Paragraph("<b>Institution:</b>", STYLES['TDBold']), Paragraph("Vellore Institute of Technology", STYLES['TD']),
         Paragraph("<b>Subject:</b>", STYLES['TDBold']), Paragraph("Database Management Systems (DBMS)", STYLES['TD'])],
        [Paragraph("<b>Students:</b>", STYLES['TDBold']), Paragraph("D Joshua Daniel (24BCE0436) & M Saryu (24BCE2524)", STYLES['TD']),
         Paragraph("<b>Faculty Guide:</b>", STYLES['TDBold']), Paragraph("Prof. Kanagaraj K", STYLES['TD'])],
        [Paragraph("<b>Oracle Environment:</b>", STYLES['TDBold']), Paragraph("Oracle AI Database 26ai Free (FREEPDB1 / FRAUDLENS_USER)", STYLES['TD']),
         Paragraph("<b>Host Machine:</b>", STYLES['TDBold']), Paragraph("Win 11 Home Single Language | Core i3-1115G4 | 8GB RAM", STYLES['TD'])],
    ]
    t_meta = Table(meta_content, colWidths=[90, 160, 95, 160])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_LIGHT_BG),
        ('BOX', (0,0), (-1,-1), 1.0, C_NAVY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 12))

    # Executive Summary of Audit
    story.append(Paragraph("1. Executive Summary of Audit", STYLES['H1']))
    story.append(Paragraph(
        "A rigorous, line-by-line technical audit of the FraudLens DBMS Case Study Report was conducted across all 31 sections. "
        "The review evaluated factual fidelity against the live Oracle AI Database 26ai Free instance, checked relational modeling "
        "principles against Codd and Date relational algebra, verified procedural PL/SQL exception flows, cross-referenced physical constraints "
        "in Oracle's data dictionary, and audited host hardware specifications.",
        STYLES['Body']
    ))
    story.append(Paragraph(
        "<b>Summary of Findings:</b> 14 key findings were identified across three severity tiers: <b>4 Critical</b> (exaggerated production claims, "
        "unreconciled transaction-to-alert cardinality, oversimplified normalization proofs, and unclarified fraud rule automation scope), "
        "<b>8 Major</b> (audit immutability nuance, ON DELETE CASCADE compliance evaluation, constraint breakdown, host hardware/OS corrections, "
        "and academic year clarification), and <b>2 Minor</b> (reference standardizations and TOC pagination alignment). "
        "All verified items have been corrected directly in the final report <code>FraudLens_DBMS_Case_Study_Report_Final.pdf</code>.",
        STYLES['Body']
    ))
    story.append(Spacer(1, 8))

    # Section 2: Audit Table
    story.append(Paragraph("2. Comprehensive Audit & Correction Matrix", STYLES['H1']))
    story.append(Paragraph(
        "The matrix below details every issue identified, its severity rating, the specific technical correction applied, "
        "and its current verification status.",
        STYLES['Body']
    ))

    table_data = [
        [Paragraph("<b>Location</b>", STYLES['TH']),
         Paragraph("<b>Issue Identified</b>", STYLES['TH']),
         Paragraph("<b>Severity</b>", STYLES['TH']),
         Paragraph("<b>Applied Correction & Technical Rationale</b>", STYLES['TH']),
         Paragraph("<b>Status</b>", STYLES['TH'])]
    ]

    for item in AUDIT_FINDINGS:
        if item["sev"] == "Critical":
            p_sev = Paragraph(item["sev"], STYLES['TDCritical'])
        elif item["sev"] == "Major":
            p_sev = Paragraph(item["sev"], STYLES['TDMajor'])
        else:
            p_sev = Paragraph(item["sev"], STYLES['TDMinor'])

        if item["status"] == "Verified & Corrected":
            p_stat = Paragraph(item["status"], STYLES['TDVerified'])
        else:
            p_stat = Paragraph(item["status"], STYLES['TDMajor'])

        table_data.append([
            Paragraph(item["loc"], STYLES['TDBold']),
            Paragraph(item["issue"], STYLES['TD']),
            p_sev,
            Paragraph(item["fix"], STYLES['TD']),
            p_stat
        ])

    t_audit = Table(table_data, colWidths=[65, 125, 45, 185, 85])
    t_audit.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_NAVY),
        ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, C_LIGHT_BG])
    ]))
    story.append(t_audit)
    story.append(PageBreak())

    # Section 3: Deep Technical Resolutions
    story.append(Paragraph("3. Deep Technical Analysis & Discrepancy Resolutions", STYLES['H1']))

    story.append(Paragraph("3.1 Transaction-to-Alert Cardinality & Transaction-Level Deduplication", STYLES['H2']))
    story.append(Paragraph(
        "<b>The Issue:</b> The ER diagram defines <code>TRANSACTIONS (1) <---o{ (N) FRAUD_ALERT</code> "
        "because <code>transaction_id</code> in <code>FRAUD_ALERT</code> is a non-unique foreign key. However, the stored procedure "
        "<code>SP_EVALUATE_AND_ALERT_TRANSACTION</code> executes <code>SELECT COUNT(*) INTO v_existing FROM FRAUD_ALERT WHERE transaction_id = p_transaction_id;</code> "
        "and immediately exits if an alert already exists, effectively behaving as 1:0..1.<br/>"
        "<b>The Resolution:</b> The schema DDL provides 1:N structural capacity for future independent surveillance engines. "
        "Procedurally, the current check implements <b>transaction-level deduplication</b> (suppressing all subsequent alerts for that transaction, "
        "regardless of rule type) to prevent duplicate alerts from repeated batch runs, preserving a clean 1:0..1 procedure-to-alert relationship.",
        STYLES['Body']
    ))

    story.append(Paragraph("3.2 Trigger-Based Audit Logging vs. DBA Superuser Privileges", STYLES['H2']))
    story.append(Paragraph(
        "<b>The Issue:</b> Describing audit tables as 'tamper-proof' or 'unalterable' is academically inaccurate. Row-level triggers "
        "intercept standard DML operations executed by application users or compliance officers, but they do not prevent a DBA "
        "or SYSDBA from disabling triggers (<code>ALTER TRIGGER ... DISABLE</code>) or directly updating the audit table.<br/>"
        "<b>The Resolution:</b> The report now accurately states that the triggers provide <i>autonomous application-level audit logging "
        "and non-repudiation for standard user sessions</i>. It notes that true enterprise-grade immutability against database administrators "
        "requires specialized cryptographic technologies such as Oracle Blockchain Tables, write-once-read-many (WORM) storage, or hardware security modules (HSMs).",
        STYLES['Body']
    ))

    story.append(Paragraph("3.3 Statutory 5-Year Retention & Critical Evaluation of ON DELETE CASCADE", STYLES['H2']))
    story.append(Paragraph(
        "<b>The Issue:</b> Foreign keys specify <code>ON DELETE CASCADE</code>, which physically purges transaction records if an account or customer is deleted, "
        "conflicting with banking compliance mandates.<br/>"
        "<b>The Resolution:</b> Under Section 12(1)(a) of the Prevention of Money Laundering Act (PMLA) 2002, Rule 3 of PML Rules 2005 (amended by Finance Act 2019), "
        "Chapter VII (Section 45) of the RBI KYC Master Direction 2016 (Updated 2023), and FATF Recommendation 11, banks are legally mandated to preserve transaction "
        "records for at least <b>5 years</b> from the date of transaction and customer identification records for at least <b>5 years</b> after account closure. "
        "The report explains that cascading delete is an educational testing convenience; production banking schemas strictly enforce <code>ON DELETE RESTRICT</code> "
        "and logical soft deletion (<code>status = 'CLOSED'</code>).",
        STYLES['Body']
    ))

    story.append(Paragraph("3.4 Reconciliation of 71 Integrity Constraints", STYLES['H2']))
    story.append(Paragraph(
        "<b>The Issue:</b> Script <code>01_schema.sql</code> contains 17 explicit business rule <code>CHECK</code> constraints, but "
        "Oracle's <code>USER_CONSTRAINTS</code> view reports 53 check constraints (totaling 71 constraints).<br/>"
        "<b>The Resolution:</b> In Oracle Database, every column declared as <code>NOT NULL</code> is internally compiled as a system-generated "
        "check constraint of type <code>C</code> with the condition <code>\"COLUMN_NAME\" IS NOT NULL</code>. The 71 constraints are thus verified as: "
        "<b>17</b> explicit domain business rule CHECK constraints + <b>36</b> NOT NULL integrity check constraints = <b>53</b> type 'C' constraints, "
        "plus <b>8</b> Primary Keys ('P'), <b>5</b> Foreign Keys ('R'), and <b>5</b> Unique Keys ('U').",
        STYLES['Body']
    ))

    story.append(Paragraph("3.5 Procedurally Implemented vs Sample-Simulated Fraud Detection Rules", STYLES['H2']))
    story.append(Paragraph(
        "<b>The Issue:</b> The report describes 6 fraud alert categories, which could lead evaluators to expect automated PL/SQL procedures for all six.<br/>"
        "<b>The Resolution:</b> Only <code>HIGH_AMOUNT</code> (> 50,000 INR) is procedurally automated in <code>SP_EVALUATE_AND_ALERT_TRANSACTION</code>. "
        "The remaining five categories are modeled in the <code>chk_alert_type</code> domain constraint and illustrated through domain-realistic seed data in "
        "<code>03_sample_data.sql</code> to enable multi-table join and dossier reporting, representing proposed future procedural enhancements.",
        STYLES['Body']
    ))

    story.append(Paragraph("3.6 Transaction Engine Demarcation & Alert-to-Investigation Cardinality (1 : 0..1)", STYLES['H2']))
    story.append(Paragraph(
        "<b>Transaction Engine Demarcation:</b> FraudLens functions as a financial surveillance and fraud tracking system. It records immutable transaction event streams, "
        "channel metadata, and surveillance flags in <code>TRANSACTIONS</code>, with account balance snapshots in <code>ACCOUNT.balance</code>. It does not perform "
        "automated general ledger debit/credit balance mutations upon insertion.<br/>"
        "<b>Alert-to-Investigation Cardinality:</b> In the relational schema, <code>INVESTIGATION.alert_id</code> is a Foreign Key with a <code>UNIQUE NOT NULL</code> constraint. "
        "The cardinality is strictly <b>1 : 0..1</b> because newly triggered alerts remain in <code>PENDING</code> status (or are dismissed at triage) without an investigation dossier.",
        STYLES['Body']
    ))

    # Section 4: Pre-submission checklist
    story.append(Spacer(1, 4))
    story.append(Paragraph("4. Final Pre-Submission Checklist for Students", STYLES['H1']))
    story.append(Paragraph(
        "Before final academic evaluation, the following items must be verified by the student authors:",
        STYLES['Body']
    ))
    checklist_items = [
        "1. Academic Year: Successfully removed from all report cover pages and metadata blocks per user request.",
        "2. Faculty Evaluator Confirmed: Assigned and confirmed as Prof. Kanagaraj K, SCOPE, Vellore Institute of Technology.",
        "3. Review Student Registration Numbers: Confirmed D Joshua Daniel (24BCE0436) and M Saryu (24BCE2524) at Vellore Institute of Technology.",
        "4. Oral Defense Alignment: During evaluation, be prepared to explain the 1:N schema vs 1:1 procedure guard duality, the distinction between high-amount procedural automation and seed-simulated rules, and why triggers do not restrict DBA superusers.",
        "5. File Verification: Ensure both FraudLens_DBMS_Case_Study_Report_Final.pdf and FraudLens_Report_Audit_and_Corrections.pdf are retained together in the project submission archive."
    ]
    for c_item in checklist_items:
        story.append(Paragraph(f"• {c_item}", STYLES['Bullet']))

    story.append(Spacer(1, 8))
    story.append(Paragraph("5. Summary of Deliverables Produced", STYLES['H1']))
    story.append(Paragraph(
        "• <b>Revised Final PDF:</b> <code>FraudLens_DBMS_Case_Study_Report_Final.pdf</code> (20 pages, fully corrected academic report)<br/>"
        "• <b>Audit & QA PDF:</b> <code>FraudLens_Report_Audit_and_Corrections.pdf</code> (Comprehensive audit document with matrix)<br/>"
        "• <b>Supporting Assets:</b> <code>FraudLens_Report_Assets/</code> (26 verified high-resolution figures and genuine console screenshots)<br/>"
        "• <b>Verification Text:</b> <code>FraudLens_Report_Verification.txt</code> (Automated submission checklist)",
        STYLES['Body']
    ))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[AUDIT PDF] Successfully generated: {output_pdf}")

if __name__ == "__main__":
    generate_audit_pdf()
