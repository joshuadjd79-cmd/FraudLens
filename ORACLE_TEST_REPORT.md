# FraudLens: Oracle Database Execution & Test Verification Report

**Evaluation Level:** Review 1 & Review 2 Live Oracle Verification  
**Database Platform:** Oracle AI Database 26ai Free Release `23.26.3.0.0`  
**Container / PDB:** `FREEPDB1`  
**Schema / User:** `FRAUDLENS_USER`  
**Date of Execution:** 21-OCT-2026  

---

## 1. Executive Summary

All 12 modular SQL scripts of the **FraudLens — Financial Transaction and Fraud Investigation Management System** were executed against a native, locally hosted Oracle AI Database 26ai Free instance inside the dedicated pluggable database `FREEPDB1`.

Execution was performed using native Oracle SQL*Plus. All 8 database tables, 8 sequences, 4 analytical views, 3 stored procedures, 3 stored functions, 2 database triggers, and 71 integrity constraints compiled without errors. The 13-case test harness passed 100% of both positive lifecycle workflows and negative boundary constraints.

---

## 2. Verified Database Object Inventory

| Object Type | Count | Status | Notes |
| :--- | :---: | :---: | :--- |
| **Tables** | **8** | `VALID` | `CUSTOMER`, `ACCOUNT`, `TRANSACTIONS`, `FRAUD_ALERT`, `INVESTIGATOR`, `INVESTIGATION`, `INVESTIGATION_AUDIT`, `ALERT_AUDIT` |
| **Baseline Records** | **56** | `VERIFIED` | 10 Customers, 12 Accounts, 18 Transactions, 7 Fraud Alerts, 4 Investigators, 5 Investigations |
| **Sequences** | **8** | `VALID` | Starting above seed ranges: `SEQ_CUSTOMER_ID` (1011), `SEQ_ACCOUNT_ID` (2013), `SEQ_TRANSACTION_ID` (50019), `SEQ_ALERT_ID` (7009), `SEQ_INVESTIGATOR_ID` (305), `SEQ_INVESTIGATION_ID` (9006), `SEQ_INVES_AUDIT_ID` (4), `SEQ_ALERT_AUDIT_ID` (3) |
| **Views** | **4** | `VALID` | `VW_HIGH_RISK_TRANSACTIONS`, `VW_INVESTIGATION_SUMMARY`, `VW_CUSTOMER_FRAUD_EXPOSURE`, `VW_UNASSIGNED_ALERTS` |
| **Stored Procedures** | **3** | `VALID` | `SP_ASSIGN_INVESTIGATOR`, `SP_EVALUATE_AND_ALERT_TRANSACTION`, `SP_UPDATE_INVESTIGATION_STATUS` |
| **Stored Functions** | **3** | `VALID` | `FN_CALCULATE_RISK_TIER`, `FN_GET_ACCOUNT_ALERT_COUNT`, `FN_GET_TOTAL_TX_AMOUNT` |
| **Database Triggers** | **2** | `ENABLED` | `TRG_INVESTIGATION_STATUS_AUDIT`, `TRG_FRAUD_ALERT_AUDIT` |
| **Integrity Constraints** | **71** | `ENABLED` | 53 CHECK constraints, 8 Primary Keys, 5 Foreign Keys (`R`), 5 Unique Keys (`U`) |

---

## 3. Automated Test Suite Results (13 / 13 PASSED)

The test harness in `sql/11_test_cases.sql` was executed within a transactional savepoint with automatic rollback and post-cleanup:

| Test ID | Test Category | Target Operation / Statement | Expected Oracle Behavior | Actual Verified Result | Status |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **1.1** | Functional Workflow | Insert high-value transaction (₹75,000.00) | Row created in `TRANSACTIONS` with `PENDING` status | `1 row created. Transaction 59999 inserted.` | **PASSED** |
| **1.2** | Stored Procedure | Execute `SP_EVALUATE_AND_ALERT_TRANSACTION` | Breaches ₹50k threshold; generates Alert 7009 | `[SUCCESS] Generated Fraud Alert 7009 for Transaction 59999.` | **PASSED** |
| **1.3** | Functional Workflow | Open `INVESTIGATION` docket for Alert 7009 | Case 9999 created in `OPEN` state | `1 row created. Investigation 9999 opened.` | **PASSED** |
| **1.4** | Stored Procedure | Execute `SP_ASSIGN_INVESTIGATOR(9999, 302)` | Allocates active investigator Kavita Mishra | `[SUCCESS] Assigned Investigator Kavita Mishra (ID: 302) to Case 9999.` | **PASSED** |
| **1.5** | Stored Procedure | `SP_UPDATE_INVESTIGATION_STATUS(9999, 'CLOSED', 'CONFIRMED_FRAUD')` | Transitions case to `CLOSED` and stamps `end_date` | `[SUCCESS] Case 9999 status progressed from OPEN to CLOSED.` | **PASSED** |
| **1.6** | Trigger & Audit | Audit trail query on `INVESTIGATION_AUDIT` | Row-level trigger records status change events | `Audit trigger successfully recorded 1 lifecycle events for Case 9999.` | **PASSED** |
| **1.7** | Stored Functions | Execute `FN_GET_TOTAL_TX_AMOUNT` & `FN_CALCULATE_RISK_TIER` | Returns accurate financial sum and risk tier | `Account 2001 Volume: 92450 INR, Customer 1001 Tier: LOW_RISK` | **PASSED** |
| **2.1** | Constraint Rejection | Insert negative transaction amount (`-500.00 INR`) | Engine blocks insert with `ORA-02290` | `Blocked by CHECK constraint: ORA-02290: check constraint (FRAUDLENS_USER.CHK_TX_AMOUNT) violated` | **PASSED** |
| **2.2** | Unique Key Rejection | Insert duplicate email (`aarav.sharma@finmail.in`) | Engine blocks insert with `ORA-00001` | `Blocked by UNIQUE constraint: ORA-00001: unique constraint (FRAUDLENS_USER.UQ_CUSTOMER_EMAIL) violated` | **PASSED** |
| **2.3** | Referential Integrity | Insert account with non-existent `customer_id = 999999` | Engine blocks orphan record with `ORA-02291` | `Blocked by FOREIGN KEY constraint: ORA-02291: integrity constraint (FRAUDLENS_USER.FK_ACC_CUSTOMER) violated` | **PASSED** |
| **2.4** | Procedure Exception | Assign inactive investigator (`Farhan Qureshi`, ID 304) | Procedure throws user-defined exception `ORA-20004` | `Blocked with exception: ORA-20004: Error: Investigator Farhan Qureshi (ID 304) is INACTIVE.` | **PASSED** |
| **2.5** | Procedure Exception | Close case without outcome parameter (`outcome = NULL`) | Procedure throws user-defined exception `ORA-20012` | `Blocked with exception: ORA-20012: Closing a case requires a definitive outcome.` | **PASSED** |
| **2.6** | Function Exception | Call `FN_GET_TOTAL_TX_AMOUNT(999999)` with invalid account | Function raises `ORA-20030` | `Blocked with exception: ORA-20030: Account ID 999999 does not exist.` | **PASSED** |

---

## 4. Issues Diagnosed & Fixes Applied

During live Oracle SQL*Plus testing, two technical issues were identified and resolved:

1. **SQL\*Plus Ampersand (`&`) Variable Substitution Prompts:**
   * *Symptom:* SQL*Plus paused during batch execution on PROMPT headers containing `&` (e.g., `Review 1 & Review 2`, `Negative & Constraint Validation`, `GROUP BY & HAVING`), outputting `Enter value for constraint:` or `SP2-0546: User requested Interrupt or EOF detected`.
   * *Root Cause:* Default SQL*Plus behavior treats `&` as a variable substitution prefix (`SET DEFINE ON`).
   * *Resolution:* Added `SET DEFINE OFF;` at the top of `sql/00_run_all.sql` and the execution scripts. All ampersands are now parsed as literal characters.

2. **Column Aliasing in `VW_HIGH_RISK_TRANSACTIONS`:**
   * *Symptom:* `SELECT ... status FROM VW_HIGH_RISK_TRANSACTIONS` raised `ORA-00904: "STATUS": invalid identifier`.
   * *Root Cause:* The view defines `t.status AS tx_status` and `fa.severity AS alert_severity` to avoid column collisions between the joined `TRANSACTIONS` and `FRAUD_ALERT` tables.
   * *Resolution:* Updated the surveillance query in test scripts to query the correct column aliases (`tx_status`, `alert_severity`).

---

## 5. Evidence Artifacts Generated

The following genuine evidence files are archived in [`evidence/oracle/`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/):

* **Text Evidence Logs:**
  * [`evidence/oracle/01_oracle_version_pdb.txt`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/01_oracle_version_pdb.txt): Verified Oracle banner, container name (`FREEPDB1`), and session user.
  * [`evidence/oracle/02_pipeline_execution.log`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/02_pipeline_execution.log): Complete output stream from running `00_run_all.sql`.
  * [`evidence/oracle/03_table_record_counts.txt`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/03_table_record_counts.txt): Exact record counts, sequences, views, procedures, functions, triggers, and constraints.
  * [`evidence/oracle/04_query_results.txt`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/04_query_results.txt): Real query results for single-row functions, aggregations, 4-table joins, and 6-table Relational Dossier.
  * [`evidence/oracle/05_test_cases_log.txt`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/05_test_cases_log.txt): Granular output from all 13 test cases.

* **Console Screenshot Images:**
  * [`evidence/oracle/01_oracle_connection_and_pdb.png`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/01_oracle_connection_and_pdb.png): Terminal connection and PDB status.
  * [`evidence/oracle/02_table_creation_and_list.png`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/02_table_creation_and_list.png): `user_tables` listing showing all 8 tables valid.
  * [`evidence/oracle/03_sample_data_row_counts.png`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/03_sample_data_row_counts.png): Row count summary verifying 56 baseline records.
  * [`evidence/oracle/04_join_and_groupby_queries.png`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/04_join_and_groupby_queries.png): Verified multi-table join and `GROUP BY / HAVING` outputs.
  * [`evidence/oracle/05_constraint_rejection_test.png`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/05_constraint_rejection_test.png): Engine rejection of invalid negative transaction amount (`ORA-02290`).
  * [`evidence/oracle/06_main_script_execution.png`](file:///c:/Users/Steven/OneDrive/Desktop/dbms/evidence/oracle/06_main_script_execution.png): Complete test suite completion banner.

---

## 6. Review 1 Report Statements Update Advisory

Per your instructions, your existing `FraudLens_Review_1.pdf` was not modified automatically. When you are ready to update the report text for submission, here are the exact adjustments to make:

1. **Verification Disclosure Statement (Section 9 & 10):**
   * *Previous text:* *"Native Oracle execution scripts (00_run_all.sql) are ready for execution in Oracle SQL Developer or Live SQL. Testing verified offline via relational simulation."*
   * *Updated text:* *"All 12 SQL and PL/SQL scripts were executed directly against a native Oracle Database instance (Oracle AI Database 26ai Free, Release 23.26.3.0.0, container FREEPDB1) as dedicated user FRAUDLENS_USER. All 8 tables, 56 baseline records, 71 constraints, views, stored procedures, functions, triggers, and all 13 test cases (7 positive, 6 negative) were validated with zero compile or runtime errors."*

2. **Query Results Grid Figures:**
   * The actual numbers and names in your report (e.g. Net Banking total volume: ₹1,820,000, 8 txns; ATM volume: ₹262,000, 3 txns; UPI volume: ₹128,500, 4 txns; Vikram Singhania CA-1005-01 ₹650,000) have been 100% matched by live Oracle execution results.
