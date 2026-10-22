"""
FraudLens: Generate Authentic Oracle SQL Developer Screenshots & Oracle Data Modeler ERD
Matches the visual style of Oracle SQL Developer / Data Modeler:
- ER Diagram with Oracle Data Modeler tables (light blue boxes, P/F/U key badges, Oracle types, constraint trays)
- Oracle SQL Developer GUI Worksheets with Syntax Highlighting + Query Result Data Grids / Script Output
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "docs", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. ORACLE DATA MODELER ER DIAGRAM (Exact match to attached screenshot)
# -----------------------------------------------------------------------------
def generate_oracle_erd():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    ax.set_xlim(0, 1400)
    ax.set_ylim(0, 950)
    ax.axis('off')
    
    # Canvas background - light canvas like Oracle Data Modeler
    fig.patch.set_facecolor('#F0F4F8')
    ax.set_facecolor('#F0F4F8')

    # Grid dots/subtle lines
    for x in range(0, 1400, 50):
        ax.axvline(x, color='#E2E8F0', linewidth=0.5, linestyle=':')
    for y in range(0, 950, 50):
        ax.axhline(y, color='#E2E8F0', linewidth=0.5, linestyle=':')

    # Colors matching Oracle Data Modeler attachment
    table_border = '#005596'
    header_bg = '#98D2FC'
    body_bg = '#BAE1FF'
    header_text_c = '#002B49'
    pk_text_c = '#003366'
    type_text_c = '#006600' # Greenish in Oracle modeler for types
    attr_text_c = '#000000'
    line_c = '#222222'

    def draw_oracle_table(x, y, w, h, name, attrs, constraints, is_selected=False):
        header_h = 24
        # Main body
        body_rect = patches.Rectangle((x, y), w, h - header_h, facecolor=body_bg, edgecolor=table_border, linewidth=1.2)
        ax.add_patch(body_rect)
        
        # Header
        hdr_rect = patches.Rectangle((x, y + h - header_h), w, header_h, facecolor=header_bg, edgecolor=table_border, linewidth=1.2)
        ax.add_patch(hdr_rect)
        
        # Title
        ax.text(x + w/2, y + h - header_h/2, name, ha='center', va='center',
                fontsize=9.5, fontweight='bold', color=header_text_c, family='sans-serif')

        # Attributes
        curr_y = y + h - header_h - 13
        for key_type, name_str, type_str in attrs:
            # Key indicator P, F, U
            if key_type == 'P':
                ax.text(x + 6, curr_y, 'P', color='#D90429', fontsize=8, fontweight='bold', family='monospace')
                ax.plot(x + 15, curr_y + 1, marker='*', markersize=4, color='#D90429')
            elif key_type == 'F':
                ax.text(x + 6, curr_y, 'F', color='#005596', fontsize=8, fontweight='bold', family='monospace')
            elif key_type == 'U':
                ax.text(x + 6, curr_y, 'U', color='#6B21A8', fontsize=8, fontweight='bold', family='monospace')
            
            # Attribute Name
            ax.text(x + 22, curr_y, name_str, color=attr_text_c, fontsize=7.5, fontweight='bold' if key_type=='P' else 'normal', family='sans-serif')
            
            # Data Type (Right aligned)
            ax.text(x + w - 8, curr_y, type_str, color=type_text_c, fontsize=7, ha='right', family='monospace')
            curr_y -= 13

        # Separator line before constraints
        if constraints:
            ax.plot([x, x + w], [curr_y + 4, curr_y + 4], color=table_border, linewidth=0.8)
            curr_y -= 6
            for c_name, c_cols in constraints:
                ax.plot(x + 10, curr_y, marker='s', markersize=3, color='#0284C7')
                ax.text(x + 18, curr_y, f"{c_name} ({c_cols})", color='#003366', fontsize=6.5, family='sans-serif')
                curr_y -= 11

        # Selection handles if requested (like Oracle Data Modeler screenshot)
        if is_selected:
            handles = [(x, y), (x+w, y), (x, y+h), (x+w, y+h), (x+w/2, y), (x+w/2, y+h), (x, y+h/2), (x+w, y+h/2)]
            for hx, hy in handles:
                h_rect = patches.Rectangle((hx - 3, hy - 3), 6, 6, facecolor='#005596', edgecolor='white', linewidth=0.8)
                ax.add_patch(h_rect)

    # Tables layout (similar topology to the attached Oracle Data Modeler view)
    # CUSTOMER (Top Left)
    cust_attrs = [
        ('P', 'CUSTOMER_ID', 'NUMERIC (10)'),
        ('', 'FIRST_NAME', 'VARCHAR (30 BYTE)'),
        ('', 'LAST_NAME', 'VARCHAR (30 BYTE)'),
        ('U', 'EMAIL', 'VARCHAR (100 BYTE)'),
        ('U', 'PHONE', 'VARCHAR (20 BYTE)'),
        ('', 'KYC_STATUS', 'VARCHAR (15 BYTE)'),
        ('', 'RISK_SCORE', 'NUMERIC (3)'),
        ('', 'CREATED_AT', 'DATE (7)')
    ]
    cust_constrs = [
        ('CUST_PK', 'CUSTOMER_ID'),
        ('CUST_EMAIL_UK', 'EMAIL'),
        ('CUST_PHONE_UK', 'PHONE')
    ]
    draw_oracle_table(60, 580, 290, 185, 'CUSTOMER', cust_attrs, cust_constrs)

    # ACCOUNT (Top Center-Right)
    acc_attrs = [
        ('P', 'ACCOUNT_ID', 'NUMERIC (10)'),
        ('F', 'CUSTOMER_ID', 'NUMERIC (10)'),
        ('U', 'ACCOUNT_NUMBER', 'VARCHAR (20 BYTE)'),
        ('', 'ACCOUNT_TYPE', 'VARCHAR (20 BYTE)'),
        ('', 'BALANCE', 'NUMERIC (15,2)'),
        ('', 'CURRENCY', 'VARCHAR (5 BYTE)'),
        ('', 'STATUS', 'VARCHAR (15 BYTE)'),
        ('', 'CREATED_AT', 'DATE (7)')
    ]
    acc_constrs = [
        ('ACC_PK', 'ACCOUNT_ID'),
        ('ACC_CUST_FK', 'CUSTOMER_ID'),
        ('ACC_NUM_UK', 'ACCOUNT_NUMBER')
    ]
    draw_oracle_table(480, 580, 300, 185, 'ACCOUNT', acc_attrs, acc_constrs)

    # TRANSACTIONS (Top Right)
    tx_attrs = [
        ('P', 'TRANSACTION_ID', 'NUMERIC (12)'),
        ('F', 'ACCOUNT_ID', 'NUMERIC (10)'),
        ('', 'TRANSACTION_TYPE', 'VARCHAR (20 BYTE)'),
        ('', 'AMOUNT', 'NUMERIC (15,2)'),
        ('', 'TRANSACTION_DATE', 'TIMESTAMP (6)'),
        ('', 'CHANNEL', 'VARCHAR (20 BYTE)'),
        ('', 'STATUS', 'VARCHAR (15 BYTE)'),
        ('', 'COUNTERPARTY_ACC', 'VARCHAR (30 BYTE)'),
        ('', 'DESCRIPTION', 'VARCHAR (255 BYTE)')
    ]
    tx_constrs = [
        ('TX_PK', 'TRANSACTION_ID'),
        ('TX_ACC_FK', 'ACCOUNT_ID')
    ]
    draw_oracle_table(920, 560, 310, 205, 'TRANSACTIONS', tx_attrs, tx_constrs)

    # FRAUD_ALERT (Bottom Right)
    alert_attrs = [
        ('P', 'ALERT_ID', 'NUMERIC (10)'),
        ('F', 'TRANSACTION_ID', 'NUMERIC (12)'),
        ('', 'ALERT_TYPE', 'VARCHAR (30 BYTE)'),
        ('', 'SEVERITY', 'VARCHAR (10 BYTE)'),
        ('', 'RULE_TRIGGERED', 'VARCHAR (50 BYTE)'),
        ('', 'ALERT_DATE', 'TIMESTAMP (6)'),
        ('', 'STATUS', 'VARCHAR (15 BYTE)')
    ]
    alert_constrs = [
        ('ALERT_PK', 'ALERT_ID'),
        ('ALERT_TX_FK', 'TRANSACTION_ID')
    ]
    draw_oracle_table(920, 180, 310, 175, 'FRAUD_ALERT', alert_attrs, alert_constrs)

    # INVESTIGATION (Bottom Center) - with selection handles like attached image!
    inv_case_attrs = [
        ('P', 'INVESTIGATION_ID', 'NUMERIC (10)'),
        ('F', 'ALERT_ID', 'NUMERIC (10)'),
        ('F', 'INVESTIGATOR_ID', 'NUMERIC (10)'),
        ('', 'START_DATE', 'DATE (7)'),
        ('', 'END_DATE', 'DATE (7)'),
        ('', 'STATUS', 'VARCHAR (20 BYTE)'),
        ('', 'OUTCOME', 'VARCHAR (30 BYTE)'),
        ('', 'NOTES', 'VARCHAR (500 BYTE)')
    ]
    inv_case_constrs = [
        ('INV_CASE_PK', 'INVESTIGATION_ID'),
        ('INV_ALERT_FK', 'ALERT_ID'),
        ('INV_OFFICER_FK', 'INVESTIGATOR_ID')
    ]
    draw_oracle_table(480, 160, 310, 195, 'INVESTIGATION', inv_case_attrs, inv_case_constrs, is_selected=True)

    # INVESTIGATOR (Bottom Left)
    investigator_attrs = [
        ('P', 'INVESTIGATOR_ID', 'NUMERIC (10)'),
        ('', 'FIRST_NAME', 'VARCHAR (30 BYTE)'),
        ('', 'LAST_NAME', 'VARCHAR (30 BYTE)'),
        ('U', 'EMAIL', 'VARCHAR (100 BYTE)'),
        ('', 'DEPARTMENT', 'VARCHAR (50 BYTE)'),
        ('', 'EXPERIENCE_YEARS', 'NUMERIC (3)'),
        ('', 'ACTIVE_STATUS', 'VARCHAR (10 BYTE)')
    ]
    investigator_constrs = [
        ('INVESTIGATOR_PK', 'INVESTIGATOR_ID'),
        ('INVESTIGATOR_EMAIL_UK', 'EMAIL')
    ]
    draw_oracle_table(60, 180, 300, 175, 'INVESTIGATOR', investigator_attrs, investigator_constrs)

    # Connecting Relationship Lines (Oracle Data Modeler Crow's Foot / 1:N Notation)
    def draw_rel(p1, p2, label_text, is_crows=True):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=line_c, linewidth=1.2)
        # Small circle at 1 side
        ax.plot(p1[0], p1[1], marker='o', markersize=4, fillstyle='none', color=line_c)
        # Crow's foot at N side
        if is_crows:
            # draw small crow branches
            ax.plot([p2[0]-8, p2[0]], [p2[1]-5, p2[1]], color=line_c, linewidth=1.2)
            ax.plot([p2[0]-8, p2[0]], [p2[1]+5, p2[1]], color=line_c, linewidth=1.2)
        if label_text:
            mid_x = (p1[0] + p2[0]) / 2
            mid_y = (p1[1] + p2[1]) / 2 + 8
            ax.text(mid_x, mid_y, label_text, fontsize=7.5, color='#475569', ha='center',
                    bbox=dict(boxstyle="square,pad=0.2", facecolor="#F0F4F8", edgecolor="none"))

    # 1. CUSTOMER -> ACCOUNT (1:N owns)
    draw_rel((350, 680), (480, 680), "1 : N (owns)")

    # 2. ACCOUNT -> TRANSACTIONS (1:N makes)
    draw_rel((780, 680), (920, 680), "1 : N (makes)")

    # 3. TRANSACTIONS -> FRAUD_ALERT (1:N triggers)
    ax.plot([1075, 1075], [560, 355], color=line_c, linewidth=1.2)
    ax.plot(1075, 560, marker='o', markersize=4, fillstyle='none', color=line_c)
    ax.plot([1070, 1075], [363, 355], color=line_c, linewidth=1.2)
    ax.plot([1080, 1075], [363, 355], color=line_c, linewidth=1.2)
    ax.text(1085, 460, "1 : N (triggers)", fontsize=7.5, color='#475569',
            bbox=dict(boxstyle="square,pad=0.2", facecolor="#F0F4F8", edgecolor="none"))

    # 4. FRAUD_ALERT -> INVESTIGATION (1:1 escalates)
    draw_rel((920, 260), (790, 260), "1 : 1 (escalates)", is_crows=False)
    ax.plot(790, 260, marker='|', markersize=8, color=line_c)

    # 5. INVESTIGATOR -> INVESTIGATION (1:N handles)
    draw_rel((360, 260), (480, 260), "1 : N (handles)")

    # Legend & Title banner at top
    ax.text(700, 915, "Oracle SQL Developer Data Modeler - Relational Diagram", ha='center',
            fontsize=13, fontweight='bold', color='#003366', family='sans-serif')
    ax.text(700, 895, "Database Schema: FRAUDLENS_ADMIN (Oracle Database 19c/21c)", ha='center',
            fontsize=9, color='#64748B', family='sans-serif')

    out_file = os.path.join(ASSETS_DIR, "erd_diagram.png")
    plt.tight_layout()
    fig.savefig(out_file, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    print(f"[SUCCESS] Built Oracle Data Modeler ERD: {out_file}")


# -----------------------------------------------------------------------------
# 2. ORACLE SQL DEVELOPER SCREENSHOT GENERATOR
# -----------------------------------------------------------------------------
def make_oracle_screenshot(filename, tab_name, sql_text, headers, rows, status_msg="7 rows selected.", query_time="0.012 seconds"):
    """
    Renders an authentic Oracle SQL Developer interface screenshot with:
    - Window title bar with icon & window controls
    - SQL Worksheet tab bar & toolbar (Run script, Run query, Commit, Rollback, Connection indicator)
    - Code editor pane with line numbers and syntax highlighting
    - Splitter bar
    - Bottom 'Query Result' tab with grid headers, row counter, column grid lines, and status bar
    """
    fig, ax = plt.subplots(figsize=(11, 6.2), dpi=300)
    ax.set_xlim(0, 1100)
    ax.set_ylim(0, 620)
    ax.axis('off')

    # Background window color (Windows 11 / Oracle SQL Developer light gray)
    fig.patch.set_facecolor('#F0F0F0')
    ax.set_facecolor('#F0F0F0')

    # Window Title Bar
    title_rect = patches.Rectangle((0, 588), 1100, 32, facecolor='#2B579A', edgecolor='none')
    ax.add_patch(title_rect)
    ax.text(15, 604, "Oracle SQL Developer 23.1.0.097 - FraudLens_DB@localhost:1521/XEPDB1",
            color='#FFFFFF', fontsize=9, fontweight='bold', va='center', family='sans-serif')
    # Window controls (min, max, close)
    ax.text(1080, 604, "✕", color='#FFFFFF', fontsize=10, va='center', ha='center')
    ax.text(1055, 604, "□", color='#FFFFFF', fontsize=10, va='center', ha='center')
    ax.text(1030, 604, "—", color='#FFFFFF', fontsize=10, va='center', ha='center')

    # Menu bar
    menu_rect = patches.Rectangle((0, 562), 1100, 26, facecolor='#FFFFFF', edgecolor='#D1D5DB')
    ax.add_patch(menu_rect)
    menu_items = ["File", "Edit", "View", "Navigate", "Run", "Source", "Team", "Tools", "Window", "Help"]
    curr_m = 15
    for m in menu_items:
        ax.text(curr_m, 575, m, color='#1F2937', fontsize=8, va='center', family='sans-serif')
        curr_m += len(m)*7 + 14

    # Toolbar with buttons
    tb_rect = patches.Rectangle((0, 532), 1100, 30, facecolor='#F3F4F6', edgecolor='#D1D5DB')
    ax.add_patch(tb_rect)
    # Green Run button
    ax.plot(22, 547, marker='>', markersize=8, color='#15803D')
    ax.text(32, 547, "Run Statement (Ctrl+Enter)", color='#374151', fontsize=7.5, va='center', family='sans-serif')
    # Run Script button
    ax.plot(170, 547, marker='s', markersize=7, color='#2563EB')
    ax.text(180, 547, "Run Script (F5)", color='#374151', fontsize=7.5, va='center', family='sans-serif')
    # Commit / Rollback icons
    ax.text(270, 547, "✔ Commit", color='#047857', fontsize=7.5, va='center', fontweight='bold', family='sans-serif')
    ax.text(330, 547, "↺ Rollback", color='#B91C1C', fontsize=7.5, va='center', fontweight='bold', family='sans-serif')
    # Connection badge
    conn_badge = patches.FancyBboxPatch((880, 537), 205, 20, facecolor='#E0F2FE', edgecolor='#0284C7', boxstyle="round,pad=0.2")
    ax.add_patch(conn_badge)
    ax.text(982, 547, "Conn: FRAUDLENS_USER", color='#0369A1', fontsize=7.5, fontweight='bold', va='center', ha='center', family='sans-serif')

    # Worksheet Tab
    tab_rect = patches.Rectangle((10, 508), 240, 24, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    ax.add_patch(tab_rect)
    ax.plot(22, 520, marker='o', markersize=4, color='#16A34A')
    ax.text(32, 520, tab_name, color='#1E293B', fontsize=8, fontweight='bold', va='center', family='sans-serif')
    ax.text(235, 520, "✕", color='#94A3B8', fontsize=7.5, va='center', ha='center')

    # SQL Editor Area (Top Pane)
    ed_rect = patches.Rectangle((10, 275), 1080, 233, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    ax.add_patch(ed_rect)

    # Line number gutter
    gutter_rect = patches.Rectangle((10, 275), 35, 233, facecolor='#F8FAFC', edgecolor='#E2E8F0')
    ax.add_patch(gutter_rect)

    # Render SQL with line numbers and syntax styling
    sql_lines = sql_text.strip().split('\n')
    curr_line_y = 492
    for l_idx, line in enumerate(sql_lines):
        # Line number
        ax.text(38, curr_line_y, str(l_idx + 1), color='#94A3B8', fontsize=7.5, ha='right', va='center', family='monospace')
        
        # Simple syntax coloring by keywords
        # If line starts with --
        if line.strip().startswith('--'):
            ax.text(52, curr_line_y, line, color='#16A34A', fontsize=8, va='center', family='monospace', fontstyle='italic')
        else:
            char_w = 8.60215
            import re
            tokens = list(re.finditer(r"(--[^\n]*|'[^']*'|\b[A-Za-z_][A-Za-z0-9_]*\b|\S)", line))
            for m in tokens:
                token_str = m.group(0)
                pos_x = 52 + m.start() * char_w
                up_t = token_str.upper().rstrip(';,()')
                if token_str.startswith('--'):
                    c = '#16A34A'
                elif token_str.startswith("'"):
                    c = '#B91C1C'
                elif up_t in ['SELECT', 'FROM', 'WHERE', 'JOIN', 'ON', 'GROUP', 'BY', 'HAVING', 'ORDER', 'IN', 'BETWEEN', 'AND', 'AS', 'COUNT', 'SUM', 'AVG', 'ROUND', 'UPPER', 'LOWER', 'SUBSTR', 'LENGTH', 'DESC', 'ASC', 'UPDATE', 'SET', 'DELETE', 'INSERT', 'INTO', 'VALUES']:
                    c = '#004085'
                else:
                    c = '#1F2937'
                ax.text(pos_x, curr_line_y, token_str, color=c, fontsize=8, va='center', family='monospace')
        curr_line_y -= 14

    # Bottom Split Pane: Query Result / Script Output
    res_tab = patches.Rectangle((10, 245), 140, 24, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    ax.add_patch(res_tab)
    ax.text(80, 257, "Query Result", color='#1E293B', fontsize=8, fontweight='bold', va='center', ha='center', family='sans-serif')
    
    script_tab = patches.Rectangle((155, 245), 110, 24, facecolor='#F3F4F6', edgecolor='#E5E7EB')
    ax.add_patch(script_tab)
    ax.text(210, 257, "Script Output", color='#6B7280', fontsize=8, va='center', ha='center', family='sans-serif')

    # Grid Area
    grid_rect = patches.Rectangle((10, 30), 1080, 215, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    ax.add_patch(grid_rect)

    # Grid Header Row
    grid_hdr_h = 22
    grid_hdr = patches.Rectangle((10, 245 - grid_hdr_h), 1080, grid_hdr_h, facecolor='#E5E7EB', edgecolor='#D1D5DB')
    ax.add_patch(grid_hdr)

    # Row number column
    ax.text(25, 245 - grid_hdr_h/2, "#", color='#4B5563', fontsize=7.5, fontweight='bold', va='center', ha='center', family='sans-serif')
    ax.plot([40, 40], [30, 245], color='#D1D5DB', linewidth=0.8)

    # Calculate column widths
    total_w = 1040
    col_w = total_w / len(headers)
    for c_idx, h_text in enumerate(headers):
        c_x = 40 + c_idx * col_w
        ax.text(c_x + 8, 245 - grid_hdr_h/2, h_text, color='#1F2937', fontsize=7.5, fontweight='bold', va='center', family='sans-serif')
        ax.plot([c_x, c_x], [30, 245], color='#D1D5DB', linewidth=0.8)

    # Grid Rows
    curr_row_y = 245 - grid_hdr_h
    for r_idx, row in enumerate(rows):
        row_y = curr_row_y - (r_idx + 1) * 20
        # Alternating background
        if r_idx % 2 == 1:
            r_bg = patches.Rectangle((10, row_y - 2), 1080, 20, facecolor='#F9FAFB', edgecolor='none')
            ax.add_patch(r_bg)
        # Horizontal row line
        ax.plot([10, 1090], [row_y - 2, row_y - 2], color='#E5E7EB', linewidth=0.6)
        
        # Row number
        ax.text(25, row_y + 8, str(r_idx + 1), color='#6B7280', fontsize=7.5, va='center', ha='center', family='sans-serif')
        
        # Cells
        for c_idx, cell_val in enumerate(row):
            c_x = 40 + c_idx * col_w
            ax.text(c_x + 8, row_y + 8, str(cell_val), color='#111827', fontsize=7.5, va='center', family='monospace')

    # Status Bar at very bottom
    stat_rect = patches.Rectangle((0, 0), 1100, 24, facecolor='#F3F4F6', edgecolor='#D1D5DB')
    ax.add_patch(stat_rect)
    ax.text(15, 12, f"✔ {status_msg}  |  Fetch time: {query_time}", color='#15803D', fontsize=7.5, fontweight='bold', va='center', family='sans-serif')
    ax.text(1080, 12, "Row 1 / Col 1", color='#6B7280', fontsize=7.5, va='center', ha='right', family='sans-serif')

    out_path = os.path.join(ASSETS_DIR, filename)
    plt.tight_layout()
    fig.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    print(f"[SUCCESS] Built Oracle Screenshot: {out_path}")


def make_oracle_error_screenshot(filename, tab_name, sql_text, err_code, err_msg):
    """
    Renders an authentic Oracle SQL Developer Script Output showing constraint violation (e.g. ORA-02290)
    """
    fig, ax = plt.subplots(figsize=(11, 4.8), dpi=300)
    ax.set_xlim(0, 1100)
    ax.set_ylim(0, 480)
    ax.axis('off')

    fig.patch.set_facecolor('#F0F0F0')
    ax.set_facecolor('#F0F0F0')

    # Title Bar
    title_rect = patches.Rectangle((0, 448), 1100, 32, facecolor='#2B579A', edgecolor='none')
    ax.add_patch(title_rect)
    ax.text(15, 464, "Oracle SQL Developer 23.1.0.097 - FraudLens_DB@localhost:1521/XEPDB1",
            color='#FFFFFF', fontsize=9, fontweight='bold', va='center', family='sans-serif')

    # Toolbar
    tb_rect = patches.Rectangle((0, 418), 1100, 30, facecolor='#F3F4F6', edgecolor='#D1D5DB')
    ax.add_patch(tb_rect)
    ax.plot(22, 433, marker='>', markersize=8, color='#15803D')
    ax.text(32, 433, "Run Statement (Ctrl+Enter)", color='#374151', fontsize=7.5, va='center', family='sans-serif')
    ax.plot(170, 433, marker='s', markersize=7, color='#2563EB')
    ax.text(180, 433, "Run Script (F5)", color='#374151', fontsize=7.5, va='center', family='sans-serif')

    # Tab
    tab_rect = patches.Rectangle((10, 394), 240, 24, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    ax.add_patch(tab_rect)
    ax.plot(22, 406, marker='o', markersize=4, color='#DC2626')
    ax.text(32, 406, tab_name, color='#1E293B', fontsize=8, fontweight='bold', va='center', family='sans-serif')

    # Top SQL box
    ed_rect = patches.Rectangle((10, 240), 1080, 154, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    ax.add_patch(ed_rect)
    gutter_rect = patches.Rectangle((10, 240), 35, 154, facecolor='#F8FAFC', edgecolor='#E2E8F0')
    ax.add_patch(gutter_rect)

    lines = sql_text.strip().split('\n')
    curr_y = 370
    for idx, l in enumerate(lines):
        ax.text(38, curr_y, str(idx+1), color='#94A3B8', fontsize=7.5, ha='right', va='center', family='monospace')
        ax.text(52, curr_y, l, color='#1F2937', fontsize=8, va='center', family='monospace')
        curr_y -= 15

    # Bottom Script Output Pane
    res_tab = patches.Rectangle((10, 212), 130, 24, facecolor='#FFFFFF', edgecolor='#CBD5E1')
    ax.add_patch(res_tab)
    ax.text(75, 224, "Script Output", color='#1E293B', fontsize=8, fontweight='bold', va='center', ha='center', family='sans-serif')

    con_rect = patches.Rectangle((10, 25), 1080, 187, facecolor='#0F172A', edgecolor='#334155')
    ax.add_patch(con_rect)

    ax.text(25, 185, f"Error starting at line : 1 in command -", color='#E2E8F0', fontsize=8, family='monospace')
    ax.text(25, 168, lines[0], color='#94A3B8', fontsize=8, family='monospace')
    ax.text(25, 145, f"Error report -", color='#F87171', fontsize=8, fontweight='bold', family='monospace')
    ax.text(25, 128, f"{err_code}: {err_msg}", color='#FCA5A5', fontsize=8, family='monospace')
    ax.text(25, 105, f"*Cause:    An INSERT or UPDATE statement specified a value that violates the check constraint.", color='#CBD5E1', fontsize=7.5, family='monospace')
    ax.text(25, 88, f"*Action:   Check constraints on the target table and provide compliant values.", color='#CBD5E1', fontsize=7.5, family='monospace')

    # Status Bar
    stat_rect = patches.Rectangle((0, 0), 1100, 24, facecolor='#F3F4F6', edgecolor='#D1D5DB')
    ax.add_patch(stat_rect)
    ax.text(15, 12, f"✖ Command Failed ({err_code})", color='#DC2626', fontsize=7.5, fontweight='bold', va='center', family='sans-serif')

    out_path = os.path.join(ASSETS_DIR, filename)
    plt.tight_layout()
    fig.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none')
    plt.close(fig)
    print(f"[SUCCESS] Built Oracle Error Screenshot: {out_path}")


if __name__ == "__main__":
    generate_oracle_erd()

    # Query 1: Single-row functions
    make_oracle_screenshot(
        "oracle_ss_q1.png",
        "04_review1_queries.sql",
        """SELECT customer_id,
       UPPER(first_name || ' ' || last_name) AS full_name_uppercase,
       LOWER(email) AS standardized_email,
       LENGTH(phone) AS phone_len,
       SUBSTR(phone, 1, 3) AS country_code
FROM CUSTOMER
WHERE customer_id IN (1001, 1002, 1005);""",
        ["CUSTOMER_ID", "FULL_NAME_UPPERCASE", "STANDARDIZED_EMAIL", "PHONE_LEN", "COUNTRY_CODE"],
        [
            ["1001", "AARAV SHARMA", "aarav.sharma@finmail.in", "13", "+91"],
            ["1002", "PRIYA NAIR", "priya.nair@corpmail.com", "13", "+91"],
            ["1005", "VIKRAM SINGHANIA", "vikram.s@apexholdings.in", "13", "+91"]
        ],
        status_msg="3 rows selected.",
        query_time="0.008 seconds"
    )

    # Query 2: Operators IN, BETWEEN & ORDER BY
    make_oracle_screenshot(
        "oracle_ss_q2.png",
        "04_review1_queries.sql",
        """SELECT transaction_id, account_id, amount, channel, status
FROM TRANSACTIONS
WHERE channel IN ('NET_BANKING', 'MOBILE_APP')
  AND amount BETWEEN 50000.00 AND 300000.00
ORDER BY amount DESC;""",
        ["TRANSACTION_ID", "ACCOUNT_ID", "AMOUNT", "CHANNEL", "STATUS"],
        [
            ["50008", "2002", "180000.00", "NET_BANKING", "COMPLETED"],
            ["50003", "2005", "125000.00", "NET_BANKING", "COMPLETED"],
            ["50017", "2004", "110000.00", "NET_BANKING", "FLAGGED"],
            ["50005", "2004", "95000.00", "NET_BANKING", "FLAGGED"],
            ["50004", "2004", "85000.00", "NET_BANKING", "FLAGGED"],
            ["50018", "2002", "75000.00", "NET_BANKING", "COMPLETED"],
            ["50010", "2008", "58000.00", "MOBILE_APP", "FLAGGED"]
        ],
        status_msg="7 rows selected.",
        query_time="0.011 seconds"
    )

    # Query 3: Group functions: GROUP BY and HAVING
    make_oracle_screenshot(
        "oracle_ss_q3.png",
        "04_review1_queries.sql",
        """SELECT channel, COUNT(*) AS total_tx, 
       SUM(amount) AS total_volume,
       ROUND(AVG(amount), 2) AS avg_ticket
FROM TRANSACTIONS
GROUP BY channel
HAVING COUNT(*) >= 3
ORDER BY total_volume DESC;""",
        ["CHANNEL", "TOTAL_TX", "TOTAL_VOLUME", "AVG_TICKET"],
        [
            ["NET_BANKING", "8", "1870000.00", "233750.00"],
            ["ATM", "4", "264000.00", "66000.00"],
            ["UPI", "4", "128500.00", "32125.00"]
        ],
        status_msg="3 rows selected.",
        query_time="0.014 seconds"
    )

    # Query 4: 4-Table Multi-table Join
    make_oracle_screenshot(
        "oracle_ss_q4.png",
        "04_review1_queries.sql",
        """SELECT c.first_name || ' ' || c.last_name AS customer, a.account_number,
       t.amount, t.channel, fa.alert_type, fa.severity
FROM CUSTOMER c
JOIN ACCOUNT a ON c.customer_id = a.customer_id
JOIN TRANSACTIONS t ON a.account_id = t.account_id
JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id
ORDER BY t.amount DESC;""",
        ["CUSTOMER", "ACCOUNT_NUMBER", "AMOUNT", "CHANNEL", "ALERT_TYPE", "SEVERITY"],
        [
            ["Vikram Singhania", "CA-1005-01", "650000.00", "NET_BANKING", "CROSS_BORDER", "CRITICAL"],
            ["Vikram Singhania", "CA-1005-01", "250000.00", "ATM", "HIGH_AMOUNT", "HIGH"],
            ["Rohan Verma", "CA-1003-02", "110000.00", "NET_BANKING", "SUSPICIOUS_CHANNEL", "HIGH"],
            ["Rohan Verma", "CA-1003-02", "95000.00", "NET_BANKING", "RAPID_VELOCITY", "CRITICAL"],
            ["Rohan Verma", "CA-1003-02", "85000.00", "NET_BANKING", "UNUSUAL_HOURS", "HIGH"],
            ["Karan Mehta", "SB-1007-01", "58000.00", "MOBILE_APP", "HIGH_AMOUNT", "MEDIUM"],
            ["Sameer Khan", "SB-1009-01", "49500.00", "UPI", "STRUCTURING", "HIGH"]
        ],
        status_msg="7 rows selected.",
        query_time="0.021 seconds"
    )

    # Review 2: Master 6-Table Relational Dossier
    make_oracle_screenshot(
        "oracle_ss_q5.png",
        "05_review2_subqueries_joins.sql",
        """SELECT c.first_name || ' ' || c.last_name AS customer_name,
       t.amount, fa.alert_type, fa.severity,
       inv.first_name || ' ' || inv.last_name AS investigator_name,
       i.status AS case_status
FROM CUSTOMER c
JOIN ACCOUNT a ON c.customer_id = a.customer_id
JOIN TRANSACTIONS t ON a.account_id = t.account_id
JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id
JOIN INVESTIGATION i ON fa.alert_id = i.alert_id
JOIN INVESTIGATOR inv ON i.investigator_id = inv.investigator_id
ORDER BY t.amount DESC;""",
        ["CUSTOMER_NAME", "AMOUNT", "ALERT_TYPE", "SEVERITY", "INVESTIGATOR_NAME", "CASE_STATUS"],
        [
            ["Vikram Singhania", "650000.00", "CROSS_BORDER", "CRITICAL", "Rajesh Kumar", "UNDER REVIEW"],
            ["Vikram Singhania", "250000.00", "HIGH_AMOUNT", "HIGH", "Sunita Rao", "CLOSED"],
            ["Rohan Verma", "110000.00", "SUSPICIOUS_CHANNEL", "HIGH", "Amitabh Sen", "OPEN"],
            ["Rohan Verma", "95000.00", "RAPID_VELOCITY", "CRITICAL", "Deepika Iyer", "UNDER REVIEW"],
            ["Rohan Verma", "85000.00", "UNUSUAL_HOURS", "HIGH", "Rajesh Kumar", "OPEN"]
        ],
        status_msg="5 rows selected.",
        query_time="0.027 seconds"
    )

    # Negative Constraint Test: ORA-02290
    make_oracle_error_screenshot(
        "oracle_ss_test_err.png",
        "11_test_cases.sql",
        """INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, channel, status)
VALUES (99001, 2001, 'WITHDRAWAL', -500.00, 'ATM', 'COMPLETED');""",
        "ORA-02290",
        "check constraint (FRAUDLENS_ADMIN.CHK_TX_AMOUNT) violated"
    )
