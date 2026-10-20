# FraudLens: Financial Transaction & Fraud Investigation Management System

[![Oracle Database](https://img.shields.io/badge/Oracle-11g%20%7C%2012c%20%7C%2019c%20%7C%2021c%20%7C%2023c-red.svg)](https://www.oracle.com/database/)
[![SQL & PL/SQL](https://img.shields.io/badge/Language-SQL%20%26%20PL%2FSQL-orange.svg)](#)
[![Academic Project](https://img.shields.io/badge/B.Tech-CSE%20DBMS%20Case%20Study-blue.svg)](#)
[![Validation Status](https://img.shields.io/badge/Validation-100%25%20Verified-brightgreen.svg)](#)

A comprehensive, production-grade Database Management System (DBMS) case study built for **B.Tech CSE Review 1 and Review 2** evaluations. **FraudLens** models financial transactions, automated fraud surveillance rules, triage alerts, and formal forensic investigations within an auditable banking architecture.

---

## 1. Problem Statement & Domain Overview

Modern digital banking platforms process millions of monetary transactions daily across UPI, Net-Banking, Mobile Apps, and ATMs. Fast transaction processing must coexist with rigorous Anti-Money Laundering (AML) controls and fraud detection mechanisms.

### Core Challenges:
1. **High-Velocity Anomaly Detection**: Identifying suspicious activities (such as rapid successive transfers or off-hour withdrawals) without introducing operational friction for legitimate customers.
2. **Alert vs. Proof Distinction**: An automated fraud alert is merely an investigative signal—not definitive proof of fraud. Systems require human-in-the-loop forensic validation.
3. **Caseload & Lifecycle Management**: Tracking investigation cases as they progress through `OPEN`, `UNDER REVIEW`, and `CLOSED` states.
4. **Forensic Auditability**: Maintaining tamper-proof audit trails for status modifications to ensure compliance with financial authorities.

---

## 2. Core Entities & Business Rules

FraudLens is designed around **six core relational entities** plus dedicated audit event streams:

| Entity | Primary Key | Description & Role |
| :--- | :--- | :--- |
| **`CUSTOMER`** | `customer_id` | Retail and corporate banking clients with KYC status and baseline risk scores. |
| **`ACCOUNT`** | `account_id` | Bank accounts (Savings, Current, Salary, NRI) linked to customers (1:N). |
| **`TRANSACTIONS`** | `transaction_id` | Monetary debits, credits, transfers, and payments tied to accounts. |
| **`FRAUD_ALERT`** | `alert_id` | System signals triggered when transaction attributes breach anomaly rules. |
| **`INVESTIGATOR`** | `investigator_id` | Compliance officers and cyber forensic specialists. |
| **`INVESTIGATION`** | `investigation_id` | Formal case dossier linking an alert to an investigator (1:1 with Alert). |
| **`INVESTIGATION_AUDIT`** | `audit_id` | Automated event stream tracking case status changes and timestamps. |
| **`ALERT_AUDIT`** | `audit_id` | Automated event stream tracking alert triage state transitions. |

### Enforced Business Rules:
- **Ownership**: Each account belongs to exactly one customer (`customer_id` FK).
- **Ledger Integrity**: Each transaction belongs to exactly one account (`account_id` FK).
- **Alert Generation**: Every fraud alert references a recorded transaction.
- **Illustrative Rule Threshold**: Transaction amounts greater than **₹50,000 INR** represent high-value surveillance thresholds.
- **Investigator Assignment**: Investigations link an alert to an investigator. Only `ACTIVE` investigators can be assigned.
- **Lifecycle Progression**: Investigations progress through `OPEN` $\rightarrow$ `UNDER REVIEW` $\rightarrow$ `CLOSED`.
- **Closure Validation**: A case cannot be marked `CLOSED` without a definitive outcome (`CONFIRMED_FRAUD`, `FALSE_POSITIVE`, `INCONCLUSIVE`).

---

## 3. Project File Organization

The project follows a modular, numbered architecture designed for clean execution order:

```text
dbms/
├── sql/
│   ├── 00_run_all.sql                   # Master driver script executing 01 through 11
│   ├── 01_schema.sql                    # Core tables, constraints, sequences, and comments
│   ├── 02_ddl_dml_demos.sql             # Review 1 DDL (ALTER, DROP) and DML operations
│   ├── 03_sample_data.sql               # Domain-realistic sample dataset (INR amounts)
│   ├── 04_review1_queries.sql           # Single-row functions, operators, group by, joins
│   ├── 05_review2_subqueries_joins.sql  # Subqueries (single, multi, correlated) & joins
│   ├── 06_views.sql                     # Surveillance, summary, exposure, and triage views
│   ├── 07_procedures.sql                # Stored procedures with PL/SQL exception handling
│   ├── 08_functions.sql                 # Stored functions for amounts, alert counts, tiers
│   ├── 09_cursors.sql                   # Explicit cursors and parameterized cursor FOR loops
│   ├── 10_triggers_audit.sql            # Row-level audit triggers and log verification
│   └── 11_test_cases.sql                # 13 automated positive and negative test cases
├── docs/
│   ├── ERD_RELATIONAL_SCHEMA.md         # Mermaid ER diagram, schema, and normalization
│   ├── REQUIREMENTS_MAPPING.md          # Traceability matrix for Review 1 & 2 requirements
│   └── EXECUTION_GUIDE.md               # Guide for SQL Developer, SQL*Plus, LiveSQL
├── scripts/
│   └── validate_sql.py                  # Python mirror engine validating logic and constraints
├── .gitignore                           # Git ignore rules
└── README.md                            # Complete project documentation
```

---

## 4. Feature Coverage Matrix

### Review 1 Requirements
* **DDL**: Complete `CREATE TABLE`, `ALTER TABLE` (ADD, MODIFY, RENAME, DROP columns and constraints), and safe `DROP TABLE PURGE`.
* **Constraints**: `PRIMARY KEY`, `FOREIGN KEY ... ON DELETE CASCADE`, `UNIQUE`, `NOT NULL`, `CHECK`, and `DEFAULT`.
* **DML**: `INSERT` (with defaults and timestamps), `UPDATE` (expressions and status), and `DELETE` (with savepoint rollback).
* **Single-Row Functions**: `UPPER`, `LOWER`, `INITCAP`, `LENGTH`, `SUBSTR`, `ROUND`, `TRUNC`, `MOD`, `TO_CHAR`, `MONTHS_BETWEEN`, `NVL`, `COALESCE`, `NVL2`.
* **Filtering & Operators**: `WHERE`, comparison (`=`, `!=`, `>`, `<`), `AND`, `OR`, `NOT`, `IN`, `NOT IN`, `BETWEEN`, `LIKE`, `IS NULL`, `IS NOT NULL`.
* **Group Functions**: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`, `GROUP BY`, and `HAVING`.
* **Relational Joins**: Multi-table inner joins across customers, accounts, and transactions.

### Review 2 Requirements
* **Subqueries**:
  * *Single-Row*: Filtering transactions exceeding system average (`> AVG(amount)`).
  * *Multi-Row*: Filtering customers with flagged transactions (`IN`), transactions exceeding all deposits (`> ALL`), and transactions exceeding any transfer (`> ANY`).
  * *Correlated*: Accounts with transaction volume exceeding balance, and `EXISTS` / `NOT EXISTS` checks.
* **Advanced Joins**: `LEFT OUTER JOIN` showing unassigned investigators and alerts, plus a comprehensive 6-table **Master Investigation Dossier**.
* **Database Views**:
  * `VW_HIGH_RISK_TRANSACTIONS`: Real-time transaction surveillance.
  * `VW_INVESTIGATION_SUMMARY`: Forensic case lifecycle and turnaround tracking.
  * `VW_CUSTOMER_FRAUD_EXPOSURE`: 360-degree customer risk posture.
  * `VW_UNASSIGNED_ALERTS`: Triage queue for pending signals.
* **Stored Procedures**:
  * `SP_ASSIGN_INVESTIGATOR`: Validates investigator active status and assigns lead.
  * `SP_UPDATE_INVESTIGATION_STATUS`: Manages state progression and requires outcomes on closure.
  * `SP_EVALUATE_AND_ALERT_TRANSACTION`: Evaluates >₹50,000 threshold and triggers alerts.
* **Stored Functions**:
  * `FN_GET_TOTAL_TX_AMOUNT`: Aggregates account transaction volume.
  * `FN_GET_ACCOUNT_ALERT_COUNT`: Calculates alert frequency per account.
  * `FN_CALCULATE_RISK_TIER`: Converts numeric risk scores (0–100) to risk tier bands.
* **Cursors**:
  * Explicit Cursor (`OPEN`, `FETCH`, `%NOTFOUND`, `CLOSE`) compiling high-risk alert exposure.
  * Parameterized Cursor FOR loop batch-processing active investigation queues.
* **Triggers & Auditing**:
  * `TRG_INVESTIGATION_STATUS_AUDIT`: Captures previous/new status, user, and timestamp into `INVESTIGATION_AUDIT`.
  * `TRG_FRAUD_ALERT_AUDIT`: Captures alert transitions into `ALERT_AUDIT`.
* **Testing & Integrity**:
  * 13 automated positive and negative test cases validating check constraints, unique keys, foreign keys, and procedure exceptions.

---

## 5. Quickstart & Execution

### Option A: Oracle SQL Developer / SQL*Plus (Recommended)
1. Open SQL Developer or SQL\*Plus connected to your Oracle schema.
2. Run the master script:
   ```sql
   @sql/00_run_all.sql
   ```
3. All 11 modules will compile and execute with complete output logging.

### Option B: Local Python Validation Engine (Offline Simulation)
Run the automated 3-tier linter and relational simulation runner in your terminal:
```bash
python scripts/validate_sql.py
```
> [!NOTE]
> `validate_sql.py` performs deep static PL/SQL linting and simulates relational execution in Python SQLite. For official native database evaluation, run `00_run_all.sql` in Oracle SQL Developer or SQL*Plus.

---

## 6. Live Feature Demonstration Sequence

All IDs below are verified against `03_sample_data.sql`:

### A. Automatic Alert Generation via Stored Procedure
Evaluates transaction **`50008`** (Amount: ₹180,000 INR, currently unflagged without an alert):
```sql
VAR v_alert_id NUMBER;
EXEC SP_EVALUATE_AND_ALERT_TRANSACTION(50008, :v_alert_id);
PRINT v_alert_id;
-- Output: [SUCCESS] Generated Fraud Alert 7008 for Transaction 50008.
```

### B. Investigator Assignment with Active Status Validation
Assigns active investigator **`302`** (Kavita Mishra) to open case **`9004`**:
```sql
EXEC SP_ASSIGN_INVESTIGATOR(9004, 302);
-- Output: [SUCCESS] Assigned Investigator Kavita Mishra (ID: 302) to Case 9004.

-- Negative Test: Assigning inactive investigator 304 (Farhan Qureshi)
EXEC SP_ASSIGN_INVESTIGATOR(9001, 304);
-- Output: ORA-20004: Error: Investigator Farhan Qureshi (ID 304) is INACTIVE.
```

### C. State Progression & Audit Trigger Capture
Progresses case **`9004`** from `OPEN` to `UNDER REVIEW`:
```sql
EXEC SP_UPDATE_INVESTIGATION_STATUS(9004, 'UNDER REVIEW', 'PENDING', 'Forensic IP log requested from correspondent bank.');
-- Output: [SUCCESS] Case 9004 status progressed from OPEN to UNDER REVIEW.

-- Verify trigger capture in INVESTIGATION_AUDIT:
SELECT audit_id, investigation_id, old_status, new_status, changed_by, change_action 
FROM INVESTIGATION_AUDIT WHERE investigation_id = 9004;
```

### D. Master 6-Table Relational Dossier
```sql
SELECT inv.investigation_id, inv.status, fa.severity, t.amount, a.account_number,
       c.first_name || ' ' || c.last_name AS customer,
       i.first_name || ' ' || i.last_name AS lead_investigator
FROM INVESTIGATION inv
JOIN FRAUD_ALERT fa       ON inv.alert_id = fa.alert_id
JOIN TRANSACTIONS t       ON fa.transaction_id = t.transaction_id
JOIN ACCOUNT a            ON t.account_id = a.account_id
JOIN CUSTOMER c           ON a.customer_id = c.customer_id
LEFT JOIN INVESTIGATOR i  ON inv.investigator_id = i.investigator_id;
```

---

## 7. Project Scope, Limitations & Future Enhancements

### Scope
- Focused strictly on core relational modeling, SQL standards, and PL/SQL procedural features mandated by the B.Tech CSE DBMS curriculum.
- Uses realistic Indian banking denominations (INR) and business rules.

### Current Limitations
- Alert thresholding uses deterministic rule heuristics (>₹50,000 threshold, velocity, channel) rather than predictive machine learning models.
- Transaction settlement assumes synchronous local clearing.

### Future Enhancements
- Integration with external message brokers (Apache Kafka) for real-time transaction streaming.
- Biometric authentication logs for mobile banking channel verification.
- Automated regulatory report generation (e.g., Suspicious Transaction Reports - STR for RBI / FIU-IND).
