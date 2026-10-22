"""
FraudLens: Master PDF & DOCX Documentation Generator
Generates:
1. FraudLens_Review_1.pdf
2. FraudLens_Review_1_and_Review_2.pdf
3. FraudLens_Review_1.docx
4. FraudLens_Review_1_and_Review_2.docx
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
ASSETS_DIR = os.path.join(DOCS_DIR, "assets")

# Ensure assets exist
ERD_IMG = os.path.join(ASSETS_DIR, "erd_diagram.png")
ARCH_IMG = os.path.join(ASSETS_DIR, "architecture_flow.png")
FLOW_IMG = os.path.join(ASSETS_DIR, "workflow_lifecycle.png")

# Palette Constants
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

# Numbered Canvas for Two-Pass Page Numbering (Page X of Y)
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
        if self._pageNumber == 1:
            # Suppress header and footer on cover page
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(COLOR_MUTED)

        # Running Header
        self.drawString(45, 805, "FraudLens: Financial Transaction & Fraud Investigation Management System")
        self.drawRightString(550, 805, "B.Tech CSE · VIT Vellore")
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(45, 798, 550, 798)

        # Running Footer
        self.line(45, 45, 550, 45)
        self.drawString(45, 34, "DBMS Case Study · Confidential & Academic Report")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(550, 34, page_str)
        self.restoreState()

def create_custom_styles():
    styles = getSampleStyleSheet()
    
    # Custom headings
    styles.add(ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=COLOR_PRIMARY,
        alignment=0,
        spaceAfter=10
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=COLOR_BLUE,
        alignment=0,
        spaceAfter=25
    ))
    styles.add(ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=15,
        textColor=COLOR_TEXT,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=COLOR_NAVY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'SubSectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=COLOR_PRIMARY,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    ))
    styles.add(ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=COLOR_TEXT,
        spaceAfter=6
    ))
    styles.add(ParagraphStyle(
        'BodyDarkBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13.5,
        textColor=COLOR_TEXT
    ))
    styles.add(ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=COLOR_TEXT
    ))
    styles.add(ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=COLOR_TEXT,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.5,
        textColor=COLOR_TEXT,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        'TableCellMono',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=COLOR_TEXT,
        alignment=0
    ))
    styles.add(ParagraphStyle(
        'CodeBlock',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=10,
        textColor=COLOR_CODE_TEXT
    ))
    styles.add(ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        textColor=COLOR_MUTED,
        alignment=1,
        spaceAfter=8
    ))
    return styles

def build_callout(text, styles, border_color=COLOR_BLUE, bg_color=colors.HexColor("#F0F9FF")):
    p = Paragraph(f"<b>Key Insight:</b> {text}", styles['CalloutText'])
    t = Table([[p]], colWidths=[505])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('BOX', (0,0), (-1,-1), 1, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    return t

def build_code_box(code_text, styles):
    clean_lines = [line for line in code_text.strip().splitlines()]
    paragraphs = [Paragraph(line.replace(" ", "&nbsp;"), styles['CodeBlock']) for line in clean_lines]
    t = Table([[paragraphs]], colWidths=[505])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), COLOR_CODE_BG),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#334155")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

print("[OK] Base PDF generation framework initialized.")
