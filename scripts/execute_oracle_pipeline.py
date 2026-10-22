"""
FraudLens: Native Oracle Pipeline Execution and Verification Harness
Connects to Oracle 26ai Free (FREEPDB1) as FRAUDLENS_USER.
Executes 00_run_all.sql and collects genuine verification evidence.
"""

import os
import subprocess
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SQL_DIR = os.path.join(BASE_DIR, "sql")
EVIDENCE_DIR = os.path.join(BASE_DIR, "evidence", "oracle")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

import getpass

ORACLE_PWD = os.environ.get("ORACLE_PWD")
if not ORACLE_PWD:
    # Fallback to interactive prompt if executed manually
    try:
        ORACLE_PWD = getpass.getpass("Enter password for FRAUDLENS_USER: ")
    except Exception:
        ORACLE_PWD = ""

PDB_CONN = f'FRAUDLENS_USER/"{ORACLE_PWD}"@//localhost:1521/freepdb1'

SQLPLUS_EXE = os.environ.get("SQLPLUS_EXE", r"C:\app\Steven\product\26ai\dbhomeFree\bin\sqlplus.exe")

def run_sqlplus(conn_str, sql_commands, cwd=SQL_DIR):
    """Executes SQL commands via SQL*Plus and returns stdout, stderr, and exitcode."""
    cmd = [SQLPLUS_EXE, "-s", conn_str]
    proc = subprocess.run(
        cmd,
        input=sql_commands,
        text=True,
        capture_output=True,
        cwd=cwd
    )
    return proc.stdout, proc.stderr, proc.returncode

def step1_verify_version_pdb():
    print(">>> [Step 1] Verifying Oracle Version and Container Details...")
    sql = """
SET PAGESIZE 50 LINESIZE 150 FEEDBACK OFF DEFINE OFF
SELECT banner FROM v$version;
SELECT name, open_mode, restricted FROM v$pdbs;
SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS current_container,
       SYS_CONTEXT('USERENV', 'SESSION_USER') AS session_user,
       SYS_CONTEXT('USERENV', 'DB_NAME') AS db_name
FROM DUAL;
EXIT;
"""
    stdout, stderr, code = run_sqlplus(PDB_CONN, sql)
    out_path = os.path.join(EVIDENCE_DIR, "01_oracle_version_pdb.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("=== ORACLE INSTANCE & CONTAINER VERIFICATION ===\n")
        f.write(stdout)
        if stderr:
            f.write("\nSTDERR:\n" + stderr)
    print(f"    Saved: {out_path} (Exit: {code})")

def step2_execute_pipeline():
    print(">>> [Step 2] Executing Master Pipeline: 00_run_all.sql...")
    sql = """
SET DEFINE OFF
SET ECHO ON
SET FEEDBACK ON
SET SERVEROUTPUT ON SIZE 1000000
SET LINESIZE 250
SET PAGESIZE 100
@00_run_all.sql
EXIT;
"""
    stdout, stderr, code = run_sqlplus(PDB_CONN, sql, cwd=SQL_DIR)
    out_path = os.path.join(EVIDENCE_DIR, "02_pipeline_execution.log")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(stdout)
        if stderr:
            f.write("\n=== STDERR ===\n" + stderr)
    print(f"    Saved: {out_path} (Exit: {code})")
    return stdout, code

def step3_verify_counts_and_objects():
    print(">>> [Step 3] Verifying Database Objects, Table Counts, and Records...")
    sql = """
SET PAGESIZE 100 LINESIZE 200 FEEDBACK ON DEFINE OFF
PROMPT ============================================================================
PROMPT 1. ALL TABLES IN FRAUDLENS_USER SCHEMA
PROMPT ============================================================================
SELECT table_name, status, num_rows, tablespace_name 
FROM user_tables 
ORDER BY table_name;

PROMPT ============================================================================
PROMPT 2. RECORD COUNTS ACROSS ALL CORE & AUDIT TABLES
PROMPT ============================================================================
SELECT 'CUSTOMER'            AS table_name, COUNT(*) AS record_count FROM CUSTOMER
UNION ALL
SELECT 'ACCOUNT'             AS table_name, COUNT(*) AS record_count FROM ACCOUNT
UNION ALL
SELECT 'TRANSACTIONS'        AS table_name, COUNT(*) AS record_count FROM TRANSACTIONS
UNION ALL
SELECT 'FRAUD_ALERT'         AS table_name, COUNT(*) AS record_count FROM FRAUD_ALERT
UNION ALL
SELECT 'INVESTIGATOR'        AS table_name, COUNT(*) AS record_count FROM INVESTIGATOR
UNION ALL
SELECT 'INVESTIGATION'       AS table_name, COUNT(*) AS record_count FROM INVESTIGATION
UNION ALL
SELECT 'INVESTIGATION_AUDIT' AS table_name, COUNT(*) AS record_count FROM INVESTIGATION_AUDIT
UNION ALL
SELECT 'ALERT_AUDIT'         AS table_name, COUNT(*) AS record_count FROM ALERT_AUDIT;

PROMPT ============================================================================
PROMPT 3. SEQUENCES STATUS & CURRENT VALUES
PROMPT ============================================================================
SELECT sequence_name, min_value, max_value, increment_by, last_number 
FROM user_sequences 
ORDER BY sequence_name;

PROMPT ============================================================================
PROMPT 4. VIEWS STATUS
PROMPT ============================================================================
SELECT view_name, read_only 
FROM user_views 
ORDER BY view_name;

PROMPT ============================================================================
PROMPT 5. STORED PROCEDURES & FUNCTIONS STATUS
PROMPT ============================================================================
SELECT object_name, object_type, status, created, last_ddl_time 
FROM user_objects 
WHERE object_type IN ('PROCEDURE', 'FUNCTION') 
ORDER BY object_type, object_name;

PROMPT ============================================================================
PROMPT 6. TRIGGERS STATUS
PROMPT ============================================================================
SELECT trigger_name, trigger_type, triggering_event, table_name, status 
FROM user_triggers 
ORDER BY trigger_name;

PROMPT ============================================================================
PROMPT 7. CONSTRAINTS AUDIT
PROMPT ============================================================================
SELECT constraint_type, COUNT(*) AS constraint_count, status
FROM user_constraints
GROUP BY constraint_type, status
ORDER BY constraint_type;

EXIT;
"""
    stdout, stderr, code = run_sqlplus(PDB_CONN, sql)
    out_path = os.path.join(EVIDENCE_DIR, "03_table_record_counts.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(stdout)
        if stderr:
            f.write("\nSTDERR:\n" + stderr)
    print(f"    Saved: {out_path} (Exit: {code})")

def step4_verify_queries():
    print(">>> [Step 4] Executing Key Queries and Capturing Real Outputs...")
    sql = """
SET PAGESIZE 100 LINESIZE 250 FEEDBACK ON DEFINE OFF
PROMPT ============================================================================
PROMPT QUERY 1: Single-Row Functions (Customer Details Normalization)
PROMPT ============================================================================
SELECT customer_id,
       UPPER(first_name || ' ' || last_name) AS full_name_uppercase,
       LOWER(email) AS standardized_email,
       LENGTH(phone) AS phone_len,
       SUBSTR(phone, 1, 3) AS country_code
FROM CUSTOMER
WHERE customer_id IN (1001, 1002, 1005);

PROMPT ============================================================================
PROMPT QUERY 2: Channel Aggregation (GROUP BY & HAVING)
PROMPT ============================================================================
SELECT channel, COUNT(*) AS total_tx, SUM(amount) AS total_volume,
       ROUND(AVG(amount), 2) AS avg_ticket
FROM TRANSACTIONS
GROUP BY channel
HAVING COUNT(*) >= 3
ORDER BY total_volume DESC;

PROMPT ============================================================================
PROMPT QUERY 3: 4-Table Join (Customer -> Account -> Tx -> Alert)
PROMPT ============================================================================
SELECT c.first_name || ' ' || c.last_name AS customer, a.account_number,
       t.amount, t.channel, fa.alert_type, fa.severity
FROM CUSTOMER c
JOIN ACCOUNT a ON c.customer_id = a.customer_id
JOIN TRANSACTIONS t ON a.account_id = t.account_id
JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id
ORDER BY t.amount DESC;

PROMPT ============================================================================
PROMPT QUERY 4: Master 6-Table Relational Dossier Join
PROMPT ============================================================================
SELECT inv.investigation_id AS case_ref, inv.status AS case_status, inv.outcome,
       fa.alert_type, fa.severity, t.transaction_id AS tx_id, t.amount, t.channel,
       a.account_number, c.first_name || ' ' || c.last_name AS customer_name,
       NVL(i.first_name || ' ' || i.last_name, 'UNASSIGNED') AS lead_investigator
FROM INVESTIGATION inv
JOIN FRAUD_ALERT fa       ON inv.alert_id = fa.alert_id
JOIN TRANSACTIONS t       ON fa.transaction_id = t.transaction_id
JOIN ACCOUNT a            ON t.account_id = a.account_id
JOIN CUSTOMER c           ON a.customer_id = c.customer_id
LEFT JOIN INVESTIGATOR i  ON inv.investigator_id = i.investigator_id
ORDER BY inv.investigation_id;

PROMPT ============================================================================
PROMPT QUERY 5: View Surveillance Data (VW_HIGH_RISK_TRANSACTIONS)
PROMPT ============================================================================
SELECT alert_id, transaction_id, customer_name, amount, alert_type, alert_severity, tx_status
FROM VW_HIGH_RISK_TRANSACTIONS;

PROMPT ============================================================================
PROMPT QUERY 6: Constraint Defense Test (Attempt Illegal Negative Transaction)
PROMPT ============================================================================
-- Expecting ORA-02290
INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, channel, status)
VALUES (99001, 2001, 'WITHDRAWAL', -500.00, 'ATM', 'COMPLETED');

EXIT;
"""
    stdout, stderr, code = run_sqlplus(PDB_CONN, sql)
    out_path = os.path.join(EVIDENCE_DIR, "04_query_results.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(stdout)
        if stderr:
            f.write("\nSTDERR:\n" + stderr)
    print(f"    Saved: {out_path} (Exit: {code})")

def step5_verify_test_cases():
    print(">>> [Step 5] Executing 11_test_cases.sql Test Suite...")
    sql = """
SET DEFINE OFF
SET ECHO ON
SET FEEDBACK ON
SET SERVEROUTPUT ON SIZE 1000000
SET LINESIZE 250
SET PAGESIZE 100
@11_test_cases.sql
EXIT;
"""
    stdout, stderr, code = run_sqlplus(PDB_CONN, sql, cwd=SQL_DIR)
    out_path = os.path.join(EVIDENCE_DIR, "05_test_cases_log.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(stdout)
        if stderr:
            f.write("\n=== STDERR ===\n" + stderr)
    print(f"    Saved: {out_path} (Exit: {code})")

if __name__ == "__main__":
    step1_verify_version_pdb()
    step2_execute_pipeline()
    step3_verify_counts_and_objects()
    step4_verify_queries()
    step5_verify_test_cases()
    print(">>> Finished All Oracle Execution and Evidence Collection Successfully!")
