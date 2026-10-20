# FraudLens: Database Execution & Verification Guide

This guide describes how to run and verify the **FraudLens** SQL and PL/SQL code across standard Oracle Database environments.

---

## 1. Supported Environments

* **Oracle SQL Developer** (Versions 19c, 21c, 23c)
* **Oracle SQL\*Plus CLI**
* **Oracle Live SQL** (`livesql.oracle.com`)
* **Oracle Autonomous Database (Cloud)**
* **Local In-Memory Mirror Validation Engine** (Python 3.8+)

---

## 2. Recommended Execution Sequence

All scripts are numbered strictly according to referential dependency:

```text
sql/
├── 00_run_all.sql                   <-- Master Driver (executes 01 through 11 in order)
├── 01_schema.sql                    <-- Core DDL: Sequences, Tables, Constraints
├── 02_ddl_dml_demos.sql             <-- Review 1 DDL ALTER & DML Demonstrations
├── 03_sample_data.sql               <-- Consistent domain sample dataset
├── 04_review1_queries.sql           <-- Functions, Operators, Group By, Joins
├── 05_review2_subqueries_joins.sql  <-- Subqueries, Multi-table Dossier Join
├── 06_views.sql                     <-- Surveillance & Operational Views
├── 07_procedures.sql                <-- PL/SQL Stored Procedures
├── 08_functions.sql                 <-- PL/SQL Stored Functions
├── 09_cursors.sql                   <-- PL/SQL Explicit Cursor & Cursor FOR Loop
├── 10_triggers_audit.sql            <-- PL/SQL Audit Triggers & Event Logs
└── 11_test_cases.sql                <-- Positive & Negative Test Suite
```

---

## 3. Running via Oracle SQL Developer (GUI)

1. Open **Oracle SQL Developer** and establish a connection to your Oracle schema (e.g., `HR`, `SYSTEM`, or project user `FRAUDLENS_USER`).
2. Open the file **`sql/00_run_all.sql`** (`File -> Open`).
3. Press **F5** (or click the **Run Script** icon with the tiny page and green triangle).
4. View the **Script Output** console. You will see sequential execution logs, row insertion counts, procedure compilation statuses, and automated test passes.
5. Alternatively, open and execute each script individually from `01_schema.sql` to `11_test_cases.sql` using **F5**.

---

## 4. Running via SQL*Plus (Command Line)

1. Open your terminal or Windows PowerShell.
2. Navigate to the `sql/` directory:
   ```powershell
   cd c:\Users\Steven\OneDrive\Desktop\dbms\sql
   ```
3. Connect using SQL\*Plus:
   ```bash
   sqlplus username/password@localhost:1521/XEPDB1
   ```
4. Execute the master script:
   ```sql
   SQL> @00_run_all.sql
   ```
5. To log all output directly to a file:
   ```sql
   SQL> SPOOL execution_results.log
   SQL> @00_run_all.sql
   SQL> SPOOL OFF
   ```

---

## 5. Running on Oracle Live SQL (Web Browser)

1. Navigate to **[https://livesql.oracle.com](https://livesql.oracle.com)** and sign in with your Oracle SSO credentials.
2. Click **SQL Worksheet**.
3. Since Live SQL does not support `@` file includes, paste each script into the worksheet in sequential order:
   * Paste and Run `01_schema.sql`
   * Paste and Run `03_sample_data.sql`
   * Paste and Run `04_review1_queries.sql`
   * Paste and Run `05_review2_subqueries_joins.sql`
   * Paste and Run `06_views.sql`
   * Paste and Run `07_procedures.sql`
   * Paste and Run `08_functions.sql`
   * Paste and Run `09_cursors.sql`
   * Paste and Run `10_triggers_audit.sql`
   * Paste and Run `11_test_cases.sql`

---

## 6. Running Local Python Validation Runner

If an Oracle instance is not currently configured on your local workstation, run the included Python mirror validation engine to verify relational constraints, foreign keys, and query logic immediately:

```powershell
cd c:\Users\Steven\OneDrive\Desktop\dbms
python scripts\validate_sql.py
```

### Verified Output Summary:
* **All 12 SQL scripts verified**: Correct syntax, balance, and referential sequence.
* **Customer table**: 10 profiles populated.
* **Account table**: 12 accounts populated.
* **Transactions table**: 18 transactions populated (10 transactions exceeding ₹50,000 threshold).
* **Fraud Alert table**: 7 anomaly alerts populated.
* **Investigator table**: 4 compliance officers populated.
* **Investigation table**: 5 forensic cases populated.
* **6-Table Dossier Join**: 5 full cases joined across customers, accounts, transactions, alerts, and investigators.
* **Audit Triggers & Test Harness**: 13 positive and negative test cases passing with clean rollback.
