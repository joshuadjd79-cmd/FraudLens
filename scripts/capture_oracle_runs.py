"""
FraudLens: Execute live Oracle queries and capture verbatim SQL*Plus outputs.
"""

import os
import subprocess

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
OUTPUT_DIR = os.path.join(BASE_DIR, "evidence", "oracle_runs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_sql(cmd_script, filename):
    setup = """SET PAGESIZE 50 LINESIZE 120 TAB OFF ECHO ON FEEDBACK ON HEADING ON TRIMSPOOL ON
"""
    full_sql = setup + cmd_script + "\nEXIT;\n"
    proc = subprocess.run(
        [SQLPLUS_EXE, "-s", PDB_CONN],
        input=full_sql,
        text=True,
        capture_output=True,
        cwd=BASE_DIR
    )
    out_path = os.path.join(OUTPUT_DIR, filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(proc.stdout)
        if proc.stderr:
            f.write("\nSTDERR:\n" + proc.stderr)
    print(f"Captured: {filename} (Return code: {proc.returncode})")
    return proc.stdout

# 1. Connection & Banner
run_sql("""
SELECT banner FROM v$version;
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS container,
       SYS_CONTEXT('USERENV', 'SESSION_USER') AS current_user,
       SYS_CONTEXT('USERENV', 'DB_NAME') AS db_name
FROM DUAL;
""", "01_connection.txt")

# 2. Review 1 - Query 1 Single Row
run_sql("""
SELECT customer_id,
       UPPER(first_name || ' ' || last_name) AS full_name_uppercase,
       LOWER(email) AS standardized_email,
       LENGTH(phone) AS phone_len,
       SUBSTR(phone, 1, 3) AS country_code
FROM CUSTOMER
WHERE customer_id IN (1001, 1002, 1005);
""", "02_r1_singlerow.txt")

# 3. Review 1 - Query 2 IN, BETWEEN, ORDER BY
run_sql("""
SELECT transaction_id, account_id, amount, channel, status
FROM TRANSACTIONS
WHERE channel IN ('NET_BANKING', 'MOBILE_APP')
  AND amount BETWEEN 50000.00 AND 300000.00
ORDER BY amount DESC;
""", "03_r1_in_between.txt")

# 4. Review 1 - Query 3 GROUP BY & HAVING
run_sql("""
SELECT channel, COUNT(*) AS total_tx, SUM(amount) AS total_volume,
       ROUND(AVG(amount), 2) AS avg_ticket
FROM TRANSACTIONS
GROUP BY channel
HAVING COUNT(*) >= 3
ORDER BY total_volume DESC;
""", "04_r1_groupby.txt")

# 5. Review 1 - Query 4 Four-table join
run_sql("""
SELECT c.first_name || ' ' || c.last_name AS customer,
       a.account_number,
       t.amount,
       t.channel,
       fa.alert_type,
       fa.severity
FROM CUSTOMER c
JOIN ACCOUNT a ON c.customer_id = a.customer_id
JOIN TRANSACTIONS t ON a.account_id = t.account_id
JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id
ORDER BY t.amount DESC;
""", "05_r1_join.txt")

# 6. Review 1 - Constraint violation (ORA-02290)
run_sql("""
INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, channel, status)
VALUES (99001, 2001, 'WITHDRAWAL', -500.00, 'ATM', 'COMPLETED');
""", "06_r1_constraint_err.txt")

# 7. Review 2 - Subqueries
run_sql("""
SELECT t.transaction_id, t.account_id, t.amount, t.channel, t.status,
       ROUND((SELECT AVG(amount) FROM TRANSACTIONS), 2) AS sys_avg,
       ROUND(t.amount - (SELECT AVG(amount) FROM TRANSACTIONS), 2) AS diff_from_avg
FROM TRANSACTIONS t
WHERE t.amount > (SELECT AVG(amount) FROM TRANSACTIONS)
ORDER BY t.amount DESC;
""", "07_r2_subquery.txt")

# 8. Review 2 - Views
run_sql("""
COLUMN customer_name FORMAT A18
COLUMN alert_type FORMAT A16
COLUMN alert_severity FORMAT A10
COLUMN tx_status FORMAT A10
SELECT alert_id, transaction_id, customer_name, amount, alert_type, alert_severity, tx_status
FROM VW_HIGH_RISK_TRANSACTIONS
WHERE ROWNUM <= 5;
""", "08_r2_views.txt")

# 9. Review 2 - Stored Procedures
run_sql("""
SET SERVEROUTPUT ON SIZE 1000000;
DECLARE
    v_alert_id NUMBER;
BEGIN
    SP_ASSIGN_INVESTIGATOR(p_investigation_id => 9001, p_investigator_id => 302);
    SP_UPDATE_INVESTIGATION_STATUS(p_investigation_id => 9001, p_new_status => 'CLOSED', p_outcome => 'CONFIRMED_FRAUD', p_notes => 'Card skimming verified.');
END;
/
""", "09_r2_procedures.txt")

# 10. Review 2 - Functions
run_sql("""
COLUMN customer_name FORMAT A20
COLUMN calculated_tier FORMAT A12
SELECT customer_id, first_name || ' ' || last_name AS customer_name, risk_score,
       FN_CALCULATE_RISK_TIER(risk_score) AS calculated_tier
FROM CUSTOMER
WHERE customer_id IN (1001, 1002, 1003, 1004, 1005);
""", "10_r2_functions.txt")

# 11. Review 2 - Triggers & Audit
run_sql("""
COLUMN changed_by FORMAT A15
COLUMN old_status FORMAT A12
COLUMN new_status FORMAT A12
COLUMN change_action FORMAT A18
SELECT audit_id, investigation_id, old_status, new_status, changed_by, change_action
FROM INVESTIGATION_AUDIT
ORDER BY audit_id;
""", "11_r2_triggers.txt")

# 12. Review 2 - Negative Test Suite Constraints
run_sql("""
SET SERVEROUTPUT ON SIZE 1000000;
-- Test 2.1: Check constraint
BEGIN
    INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, channel, status)
    VALUES (99001, 2001, 'WITHDRAWAL', -500.00, 'ATM', 'COMPLETED');
EXCEPTION WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('[CHECK CONSTRAINED DEFENDED] ' || SQLERRM);
END;
/

-- Test 2.2: Unique constraint
BEGIN
    INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score)
    VALUES (9901, 'Duplicate', 'User', 'aarav.sharma@finmail.in', '+919876543299', 'VERIFIED', 10);
EXCEPTION WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('[UNIQUE CONSTRAINED DEFENDED] ' || SQLERRM);
END;
/

-- Test 2.3: Foreign Key constraint
BEGIN
    INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, status)
    VALUES (9901, 999999, 'SB-9999-99', 'SAVINGS', 5000.00, 'ACTIVE');
EXCEPTION WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('[FOREIGN KEY DEFENDED] ' || SQLERRM);
END;
/

-- Test 2.4: Inactive Investigator Exception
BEGIN
    SP_ASSIGN_INVESTIGATOR(9002, 304);
EXCEPTION WHEN OTHERS THEN
    DBMS_OUTPUT.PUT_LINE('[BUSINESS RULE EXCEPTION] ' || SQLERRM);
END;
/
""", "12_r2_test_suite.txt")

print("All live Oracle queries executed and outputs captured!")
