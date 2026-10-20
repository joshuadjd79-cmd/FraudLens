# FraudLens: Syllabus & Review Requirements Traceability Matrix

This document maps every requirement from the **B.Tech CSE DBMS Review 1 and Review 2** evaluation rubric to the corresponding SQL / PL-SQL module in the project.

---

## Review 1 Requirements Matrix

| Requirement Area | Detailed Topic / Syntax Item | Implementing File | Code Anchor / Line Reference |
| :--- | :--- | :--- | :--- |
| **Domain Analysis** | Problem definition, business rules, entities | `docs/ERD_RELATIONAL_SCHEMA.md` | Sections 1 & 2 |
| **Relational Model** | Primary keys, foreign keys, constraints | `sql/01_schema.sql` | Lines 30–170 |
| **DDL: CREATE** | Table creation with constraints & sequences | `sql/01_schema.sql` | `CREATE TABLE ...`, `CREATE SEQUENCE` |
| **DDL: ALTER** | ADD column, MODIFY column, RENAME, DROP | `sql/02_ddl_dml_demos.sql` | Section 1 (Lines 22–50) |
| **DDL: DROP** | Table dropping, cascade constraints, purge | `sql/01_schema.sql`, `sql/02_ddl_dml_demos.sql` | Script headers & Line 52 |
| **Constraints: PK/FK** | `PRIMARY KEY`, `FOREIGN KEY ... ON DELETE CASCADE` | `sql/01_schema.sql` | All tables |
| **Constraints: UNIQUE** | Alternate keys (Email, Phone, Account Number) | `sql/01_schema.sql` | Lines 45, 72, 137, 162 |
| **Constraints: NOT NULL** | Mandatory fields | `sql/01_schema.sql` | Throughout all tables |
| **Constraints: CHECK** | Amount $>0$, balance $\ge 0$, enum values | `sql/01_schema.sql` | `chk_cust_kyc`, `chk_tx_amount`, etc. |
| **Constraints: DEFAULT** | Status defaults, currency 'INR', `SYSDATE` | `sql/01_schema.sql` | Lines 48, 73, 98, 126, 164 |
| **DML: INSERT** | Standard insert, defaults, date/timestamp | `sql/02_ddl_dml_demos.sql`, `sql/03_sample_data.sql` | Complete sample dataset |
| **DML: UPDATE** | Conditional update, expressions, status changes | `sql/02_ddl_dml_demos.sql` | Section 2 (Lines 76–90) |
| **DML: DELETE** | Transactional delete with rollback savepoint | `sql/02_ddl_dml_demos.sql` | Section 2 (Lines 92–102) |
| **Single-Row Functions** | String: `UPPER`, `LOWER`, `INITCAP`, `LENGTH`, `SUBSTR` | `sql/04_review1_queries.sql` | Section 1.1 |
| **Single-Row Functions** | Numeric: `ROUND`, `TRUNC`, `MOD` | `sql/04_review1_queries.sql` | Section 1.2 |
| **Single-Row Functions** | Date: `TO_CHAR`, `MONTHS_BETWEEN`, `SYSDATE` | `sql/04_review1_queries.sql` | Section 1.3 |
| **Single-Row Functions** | Null-handling: `NVL`, `COALESCE`, `NVL2` | `sql/04_review1_queries.sql` | Section 1.4 |
| **SQL Operators** | WHERE, comparison (`=`, `!=`, `>`, `<`), AND, OR, NOT | `sql/04_review1_queries.sql` | Section 2.1 |
| **SQL Operators** | Set membership: `IN`, `NOT IN` | `sql/04_review1_queries.sql` | Section 2.2 |
| **SQL Operators** | Range: `BETWEEN ... AND ...` | `sql/04_review1_queries.sql` | Section 2.3 |
| **SQL Operators** | Pattern matching: `LIKE` (`%`, `_`) | `sql/04_review1_queries.sql` | Section 2.4 |
| **SQL Operators** | Null evaluation: `IS NULL`, `IS NOT NULL` | `sql/04_review1_queries.sql` | Section 2.5 |
| **Group Functions** | `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` | `sql/04_review1_queries.sql` | Section 3.1 |
| **Grouping: GROUP BY** | Group transactions by channel and severity | `sql/04_review1_queries.sql` | Section 3.2, 3.3 |
| **Grouping: HAVING** | Filter grouped sets (volume $> ₹100,000$) | `sql/04_review1_queries.sql` | Section 3.4, 3.5 |
| **Relational Joins (R1)** | 2-Table & 3-Table INNER JOINs | `sql/04_review1_queries.sql` | Section 4.1, 4.2, 4.3 |

---

## Review 2 Requirements Matrix

| Requirement Area | Detailed Topic / Syntax Item | Implementing File | Code Anchor / Line Reference |
| :--- | :--- | :--- | :--- |
| **A. Subqueries** | Single-row subquery with scalar comparison (`> AVG`) | `sql/05_review2_subqueries_joins.sql` | Section 1.1 |
| **A. Subqueries** | Single-row subquery finding peak account balance | `sql/05_review2_subqueries_joins.sql` | Section 1.2 |
| **A. Subqueries** | Multi-row subquery with `IN` (Flagged tx customers) | `sql/05_review2_subqueries_joins.sql` | Section 1.3 |
| **A. Subqueries** | Multi-row subquery with `> ALL` operator | `sql/05_review2_subqueries_joins.sql` | Section 1.4 |
| **A. Subqueries** | Multi-row subquery with `> ANY` operator | `sql/05_review2_subqueries_joins.sql` | Section 1.5 |
| **A. Subqueries** | Correlated subquery (Transacted amount $>$ balance) | `sql/05_review2_subqueries_joins.sql` | Section 1.6 |
| **A. Subqueries** | Correlated subquery with `EXISTS` | `sql/05_review2_subqueries_joins.sql` | Section 1.7 |
| **A. Subqueries** | Correlated subquery with `NOT EXISTS` | `sql/05_review2_subqueries_joins.sql` | Section 1.8 |
| **B. Advanced Joins** | `LEFT OUTER JOIN` (Investigators & Caseload) | `sql/05_review2_subqueries_joins.sql` | Section 2.1 |
| **B. Advanced Joins** | `LEFT OUTER JOIN` (Alerts & Investigations) | `sql/05_review2_subqueries_joins.sql` | Section 2.2 |
| **B. Reporting Dossier** | Comprehensive 6-Table Relational Join | `sql/05_review2_subqueries_joins.sql` | Section 2.3 |
| **C. Views** | High-Risk Transaction Surveillance View | `sql/06_views.sql` | `VW_HIGH_RISK_TRANSACTIONS` |
| **C. Views** | Forensic Investigation Summary & Duration View | `sql/06_views.sql` | `VW_INVESTIGATION_SUMMARY` |
| **C. Views** | Customer 360 Fraud Exposure Aggregate View | `sql/06_views.sql` | `VW_CUSTOMER_FRAUD_EXPOSURE` |
| **C. Views** | Triage Queue for Unassigned Alerts View | `sql/06_views.sql` | `VW_UNASSIGNED_ALERTS` |
| **D. Stored Procedures**| Assign Investigator (`SP_ASSIGN_INVESTIGATOR`) | `sql/07_procedures.sql` | Procedure 1 |
| **D. Stored Procedures**| Progress Investigation Status (`SP_UPDATE_INVESTIGATION_STATUS`) | `sql/07_procedures.sql` | Procedure 2 |
| **D. Stored Procedures**| Rule Evaluation & Auto-Alert (`SP_EVALUATE_AND_ALERT_TRANSACTION`) | `sql/07_procedures.sql` | Procedure 3 |
| **D. Error Handling** | Oracle PL/SQL `EXCEPTION`, `RAISE_APPLICATION_ERROR` | `sql/07_procedures.sql`, `sql/08_functions.sql` | All procedures & functions |
| **E. Stored Functions** | Account Total Transacted (`FN_GET_TOTAL_TX_AMOUNT`) | `sql/08_functions.sql` | Function 1 |
| **E. Stored Functions** | Account Alert Count (`FN_GET_ACCOUNT_ALERT_COUNT`) | `sql/08_functions.sql` | Function 2 |
| **E. Stored Functions** | Customer Risk Tier (`FN_CALCULATE_RISK_TIER`) | `sql/08_functions.sql` | Function 3 |
| **F. Cursors** | Explicit Cursor (`OPEN`, `FETCH`, `%NOTFOUND`, `CLOSE`) | `sql/09_cursors.sql` | Demo 1 |
| **F. Cursors** | Parameterized Cursor FOR Loop | `sql/09_cursors.sql` | Demo 2 |
| **G. Triggers** | Row-level `AFTER UPDATE OF status` on Investigation | `sql/10_triggers_audit.sql` | `TRG_INVESTIGATION_STATUS_AUDIT` |
| **G. Triggers** | Row-level `AFTER UPDATE OF status` on Alert | `sql/10_triggers_audit.sql` | `TRG_FRAUD_ALERT_AUDIT` |
| **G. Audit Trail** | Dedicated audit tables tracking changes & timestamps | `sql/01_schema.sql`, `sql/10_triggers_audit.sql` | `INVESTIGATION_AUDIT`, `ALERT_AUDIT` |
| **H. Test Harness** | 13 Positive & Negative automated test cases | `sql/11_test_cases.sql` | Test Suite 1 & 2 |
| **H. Master Pipeline** | Sequenced batch runner with feedback | `sql/00_run_all.sql` | Master script |
