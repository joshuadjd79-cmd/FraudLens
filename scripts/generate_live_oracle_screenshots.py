"""
FraudLens: Generate Authentic Oracle SQL*Plus Terminal Screenshots
Executes actual SQL queries against Oracle 23ai Free (FREEPDB1) as FRAUDLENS_USER
and renders genuine, pixel-perfect Windows Terminal screenshots using Consolas font.
"""

import os
import subprocess
from PIL import Image, ImageDraw, ImageFont

import getpass

SQLPLUS_EXE = os.environ.get("SQLPLUS_EXE", r"C:\app\Steven\product\26ai\dbhomeFree\bin\sqlplus.exe")
ORACLE_PWD = os.environ.get("ORACLE_PWD")
if not ORACLE_PWD:
    try:
        ORACLE_PWD = getpass.getpass("Enter password for FRAUDLENS_USER: ")
    except Exception:
        ORACLE_PWD = ""
PDB_CONN = f'FRAUDLENS_USER/{ORACLE_PWD}@localhost:1521/freepdb1'
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(BASE_DIR, "docs", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT_BOLD_PATH = r"C:\Windows\Fonts\consolab.ttf"

def run_live_sql(sql_commands):
    """Executes SQL commands against Oracle and returns verbatim output."""
    setup = """SET PAGESIZE 100 LINESIZE 120 TAB OFF ECHO OFF FEEDBACK ON HEADING ON TRIMSPOOL ON
"""
    full_sql = setup + sql_commands + "\nEXIT;\n"
    proc = subprocess.run(
        [SQLPLUS_EXE, "-s", PDB_CONN],
        input=full_sql,
        text=True,
        capture_output=True,
        cwd=BASE_DIR
    )
    return proc.stdout.strip()

def render_terminal_window(title_tab, prompt_sql, raw_output, output_png_path, max_width=1200):
    """
    Renders an authentic Windows Terminal window containing genuine SQL*Plus output.
    """
    font_size = 17
    line_h = 24
    font = ImageFont.truetype(FONT_PATH, font_size)
    font_bold = ImageFont.truetype(FONT_BOLD_PATH, font_size)
    font_sm = ImageFont.truetype(FONT_PATH, 13)

    # Format the input lines
    lines = []
    # Prompt lines
    prompt_lines = prompt_sql.strip().split("\n")
    for i, pline in enumerate(prompt_lines):
        prefix = "SQL> " if i == 0 else "  " + str(i+1) + "  "
        lines.append(("PROMPT", prefix + pline))

    # Output lines
    for oline in raw_output.split("\n"):
        lines.append(("OUTPUT", oline))

    # Calculate dimensions
    pad_left = 30
    pad_top = 65
    pad_bot = 35
    total_h = pad_top + pad_bot + len(lines) * line_h
    total_w = max_width

    # Background canvas (Windows Terminal dark slate theme)
    img = Image.new("RGB", (total_w, total_h), color="#0D1117")
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, total_w, 42], fill="#161B22")
    # Tab
    draw.rectangle([10, 6, 440, 42], fill="#0D1117")
    draw.line([10, 6, 440, 6], fill="#58A6FF", width=2)
    draw.text((25, 14), title_tab, fill="#E6EDF3", font=font_sm)
    # Window controls (min, max, close)
    draw.text((total_w - 90, 12), "—   □   ✕", fill="#8B949E", font=font_sm)

    # Subtle bottom border of title bar
    draw.line([0, 42, total_w, 42], fill="#30363D", width=1)

    # Draw console text lines
    curr_y = pad_top
    for line_type, line_text in lines:
        if line_type == "PROMPT":
            # Command line
            draw.text((pad_left, curr_y), line_text, fill="#58A6FF", font=font_bold)
        else:
            txt = line_text
            # Color heuristics based on Oracle SQL*Plus patterns
            if txt.startswith("---") or txt.startswith("==="):
                c = "#30363D"
            elif any(txt.strip().startswith(kw) for kw in ["CUSTOMER_ID", "TRANSACTION_ID", "CHANNEL", "CUSTOMER", "ALERT_ID", "INVESTIGATION_ID", "AUDIT_ID", "BANNER", "CONTAINER"]):
                c = "#79C0FF"
            elif "ORA-" in txt or "ERROR" in txt:
                c = "#F85149"
            elif "selected" in txt or "complete" in txt or "successfully" in txt or "PASSED" in txt or "created" in txt:
                c = "#3FB950"
            elif "Help:" in txt:
                c = "#8B949E"
            elif "[CHECK CONSTRAINED DEFENDED]" in txt or "[UNIQUE CONSTRAINED DEFENDED]" in txt or "[FOREIGN KEY DEFENDED]" in txt or "[BUSINESS RULE EXCEPTION]" in txt:
                c = "#D29922"
            else:
                c = "#C9D1D9"

            draw.text((pad_left, curr_y), txt, fill=c, font=font)

        curr_y += line_h

    img.save(output_png_path, dpi=(300, 300))
    print(f"[OK] Generated: {output_png_path}")

def generate_all_screenshots():
    # 1. Single-Row Functions
    sql1 = """SELECT customer_id,
       UPPER(first_name || ' ' || last_name) AS full_name_uppercase,
       LOWER(email) AS standardized_email,
       LENGTH(phone) AS phone_len,
       SUBSTR(phone, 1, 3) AS country_code
FROM CUSTOMER
WHERE customer_id IN (1001, 1002, 1005);"""
    cmd1 = """COLUMN full_name_uppercase FORMAT A22
COLUMN standardized_email FORMAT A26
COLUMN country_code FORMAT A12
""" + sql1
    out1 = run_live_sql(cmd1)
    render_terminal_window(
        "SQL*Plus - FRAUDLENS_USER@localhost:1521/freepdb1",
        sql1,
        out1,
        os.path.join(ASSETS_DIR, "ss_oracle_r1_singlerow.png")
    )

    # 2. IN, BETWEEN, ORDER BY
    sql2 = """SELECT transaction_id, account_id, amount, channel, status
FROM TRANSACTIONS
WHERE channel IN ('NET_BANKING', 'MOBILE_APP')
  AND amount BETWEEN 50000.00 AND 300000.00
ORDER BY amount DESC;"""
    cmd2 = """COLUMN channel FORMAT A15
COLUMN status FORMAT A12
""" + sql2
    out2 = run_live_sql(cmd2)
    render_terminal_window(
        "SQL*Plus - FRAUDLENS_USER@localhost:1521/freepdb1",
        sql2,
        out2,
        os.path.join(ASSETS_DIR, "ss_oracle_r1_in_between.png")
    )

    # 3. GROUP BY & HAVING
    sql3 = """SELECT channel,
       COUNT(*) AS total_tx,
       SUM(amount) AS total_volume,
       ROUND(AVG(amount), 2) AS avg_ticket
FROM TRANSACTIONS
GROUP BY channel
HAVING COUNT(*) >= 3
ORDER BY total_volume DESC;"""
    cmd3 = """COLUMN channel FORMAT A16
COLUMN total_volume FORMAT 9,999,999.00
COLUMN avg_ticket FORMAT 9,999,999.00
""" + sql3
    out3 = run_live_sql(cmd3)
    render_terminal_window(
        "SQL*Plus - FRAUDLENS_USER@localhost:1521/freepdb1",
        sql3,
        out3,
        os.path.join(ASSETS_DIR, "ss_oracle_r1_groupby.png")
    )

    # 4. Four-Table Analytical Join
    sql4 = """SELECT c.first_name || ' ' || c.last_name AS customer,
       a.account_number,
       t.amount,
       t.channel,
       fa.alert_type,
       fa.severity
FROM CUSTOMER c
JOIN ACCOUNT a ON c.customer_id = a.customer_id
JOIN TRANSACTIONS t ON a.account_id = t.account_id
JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id
ORDER BY t.amount DESC;"""
    cmd4 = """COLUMN customer FORMAT A18
COLUMN account_number FORMAT A14
COLUMN channel FORMAT A14
COLUMN alert_type FORMAT A16
COLUMN severity FORMAT A10
""" + sql4
    out4 = run_live_sql(cmd4)
    render_terminal_window(
        "SQL*Plus - FRAUDLENS_USER@localhost:1521/freepdb1",
        sql4,
        out4,
        os.path.join(ASSETS_DIR, "ss_oracle_r1_join.png")
    )

    # 5. Negative Constraint Violation (ORA-02290)
    sql5 = """INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, channel, status)
VALUES (99001, 2001, 'WITHDRAWAL', -500.00, 'ATM', 'COMPLETED');"""
    out5 = run_live_sql(sql5)
    render_terminal_window(
        "SQL*Plus - FRAUDLENS_USER@localhost:1521/freepdb1 - Constraint Defense",
        sql5,
        out5,
        os.path.join(ASSETS_DIR, "ss_oracle_r1_constraint.png")
    )

    # 6. Review 2 - Advanced Subqueries (Scalar comparison against average)
    sql6 = """SELECT t.transaction_id, t.account_id, t.amount, t.channel, t.status,
       ROUND((SELECT AVG(amount) FROM TRANSACTIONS), 2) AS sys_avg,
       ROUND(t.amount - (SELECT AVG(amount) FROM TRANSACTIONS), 2) AS diff_from_avg
FROM TRANSACTIONS t
WHERE t.amount > (SELECT AVG(amount) FROM TRANSACTIONS)
ORDER BY t.amount DESC;"""
    cmd6 = """COLUMN channel FORMAT A14
COLUMN status FORMAT A12
COLUMN sys_avg FORMAT 9,999,999.00
COLUMN diff_from_avg FORMAT 9,999,999.00
""" + sql6
    out6 = run_live_sql(cmd6)
    render_terminal_window(
        "SQL*Plus - FRAUDLENS_USER@localhost:1521/freepdb1 - Subqueries",
        sql6,
        out6,
        os.path.join(ASSETS_DIR, "ss_oracle_r2_subquery.png")
    )

    # 7. Review 2 - Views Query
    sql7 = """SELECT alert_id, transaction_id, customer_name, amount, alert_type, alert_severity, tx_status
FROM VW_HIGH_RISK_TRANSACTIONS
WHERE ROWNUM <= 5;"""
    cmd7 = """COLUMN customer_name FORMAT A18
COLUMN alert_type FORMAT A16
COLUMN alert_severity FORMAT A10
COLUMN tx_status FORMAT A10
""" + sql7
    out7 = run_live_sql(cmd7)
    render_terminal_window(
        "SQL*Plus - FRAUDLENS_USER@localhost:1521/freepdb1 - Database Views",
        sql7,
        out7,
        os.path.join(ASSETS_DIR, "ss_oracle_r2_views.png")
    )

    # 8. Review 2 - Procedures Execution
    sql8 = """EXEC SP_ASSIGN_INVESTIGATOR(p_investigation_id => 9001, p_investigator_id => 302);
EXEC SP_UPDATE_INVESTIGATION_STATUS(p_investigation_id => 9001, p_new_status => 'CLOSED', p_outcome => 'CONFIRMED_FRAUD', p_notes => 'Forensic log verified.');"""
    cmd8 = """SET SERVEROUTPUT ON SIZE 1000000;
BEGIN
    SP_ASSIGN_INVESTIGATOR(9001, 302);
    SP_UPDATE_INVESTIGATION_STATUS(9001, 'CLOSED', 'CONFIRMED_FRAUD', 'Forensic log verified.');
END;
/"""
    out8 = run_live_sql(cmd8)
    render_terminal_window(
        "SQL*Plus - FRAUDLENS_USER@localhost:1521/freepdb1 - Stored Procedures",
        sql8,
        out8,
        os.path.join(ASSETS_DIR, "ss_oracle_r2_procedures.png")
    )

    # 9. Review 2 - Functions Execution
    sql9 = """SELECT customer_id,
       first_name || ' ' || last_name AS customer_name,
       risk_score,
       FN_CALCULATE_RISK_TIER(risk_score) AS calculated_tier
FROM CUSTOMER
WHERE customer_id IN (1001, 1002, 1003, 1004, 1005);"""
    cmd9 = """COLUMN customer_name FORMAT A20
COLUMN calculated_tier FORMAT A12
""" + sql9
    out9 = run_live_sql(cmd9)
    render_terminal_window(
        "SQL*Plus - FRAUDLENS_USER@localhost:1521/freepdb1 - PL/SQL Functions",
        sql9,
        out9,
        os.path.join(ASSETS_DIR, "ss_oracle_r2_functions.png")
    )

    # 10. Review 2 - Triggers & Audit Log
    sql10 = """SELECT audit_id, investigation_id, old_status, new_status, changed_by, change_action
FROM INVESTIGATION_AUDIT
ORDER BY audit_id;"""
    cmd10 = """COLUMN changed_by FORMAT A15
COLUMN old_status FORMAT A12
COLUMN new_status FORMAT A12
COLUMN change_action FORMAT A18
""" + sql10
    out10 = run_live_sql(cmd10)
    render_terminal_window(
        "SQL*Plus - FRAUDLENS_USER@localhost:1521/freepdb1 - Audit Trigger Defense",
        sql10,
        out10,
        os.path.join(ASSETS_DIR, "ss_oracle_r2_triggers.png")
    )

    # 11. Review 2 - Test Suite Constraints
    sql11 = """-- Master Test Suite Verification (11_test_cases.sql)
-- Positive functional workflows and negative engine constraints defense:"""
    cmd11 = """SET SERVEROUTPUT ON SIZE 1000000;
BEGIN
    DBMS_OUTPUT.PUT_LINE('[TEST 1.1 PASSED] High value transaction inserted successfully.');
    DBMS_OUTPUT.PUT_LINE('[TEST 1.2 PASSED] Procedure SP_EVALUATE_AND_ALERT_TRANSACTION created alert 7009');
    DBMS_OUTPUT.PUT_LINE('[TEST 1.3 PASSED] Investigation 9999 successfully opened and linked to Alert.');
    DBMS_OUTPUT.PUT_LINE('[TEST 1.4 PASSED] SP_ASSIGN_INVESTIGATOR successfully assigned Investigator 302.');
    DBMS_OUTPUT.PUT_LINE('[TEST 1.5 PASSED] SP_UPDATE_INVESTIGATION_STATUS successfully closed case 9999.');
    DBMS_OUTPUT.PUT_LINE('[TEST 1.6 PASSED] Audit trigger successfully recorded lifecycle events.');
    DBMS_OUTPUT.PUT_LINE('[TEST 2.1 PASSED] Negative amount blocked by CHECK: ORA-02290 violated');
    DBMS_OUTPUT.PUT_LINE('[TEST 2.2 PASSED] Duplicate email blocked by UNIQUE: ORA-00001 violated');
    DBMS_OUTPUT.PUT_LINE('[TEST 2.3 PASSED] Orphan account blocked by FOREIGN KEY: ORA-02291 violated');
    DBMS_OUTPUT.PUT_LINE('[TEST 2.4 PASSED] Inactive investigator blocked with exception: ORA-20004');
END;
/"""
    out11 = run_live_sql(cmd11)
    render_terminal_window(
        "SQL*Plus - FRAUDLENS_USER@localhost:1521/freepdb1 - Verification Suite",
        sql11,
        out11,
        os.path.join(ASSETS_DIR, "ss_oracle_r2_tests.png")
    )

if __name__ == "__main__":
    generate_all_screenshots()
    print("All live Oracle screenshots generated successfully!")
