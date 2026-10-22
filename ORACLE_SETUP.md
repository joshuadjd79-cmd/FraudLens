# FraudLens: Oracle Database Setup & Execution Guide

This document outlines the verified configuration and execution procedures for running the **FraudLens** database project against a local Oracle Database instance.

---

## 1. Verified Environment Specifications

* **Database Engine**: Oracle AI Database 26ai Free (Release `23.26.3.0.0`)
* **Host / Listener**: `localhost:1521` (TCP Protocol)
* **Root Container (CDB)**: `FREE`
* **Pluggable Database (PDB)**: `FREEPDB1` (Status: `READ WRITE`, Unrestricted)
* **Dedicated Project User**: `FRAUDLENS_USER`
* **Default Tablespace**: `USERS`
* **Temporary Tablespace**: `TEMP`
* **SQL Client**: Oracle SQL*Plus (`C:\app\Steven\product\26ai\dbhomeFree\bin\sqlplus.exe`)

---

## 2. Dedicated User & Security Configuration

The dedicated schema `FRAUDLENS_USER` was created inside the pluggable database `FREEPDB1`. The user has been granted strictly the privileges required for the coursework:

```sql
-- Connect as SYSDBA to the Root Container
sqlplus / as sysdba

-- Switch to the Pluggable Database
ALTER SESSION SET CONTAINER = FREEPDB1;

-- Create Dedicated User (Set your own secure password locally)
CREATE USER FRAUDLENS_USER IDENTIFIED BY "<your_password>"
    DEFAULT TABLESPACE USERS
    TEMPORARY TABLESPACE TEMP
    QUOTA UNLIMITED ON USERS;

-- Grant Necessary Development Privileges
GRANT CREATE SESSION TO FRAUDLENS_USER;
GRANT CREATE TABLE TO FRAUDLENS_USER;
GRANT CREATE SEQUENCE TO FRAUDLENS_USER;
GRANT CREATE VIEW TO FRAUDLENS_USER;
GRANT CREATE PROCEDURE TO FRAUDLENS_USER;
GRANT CREATE TRIGGER TO FRAUDLENS_USER;
GRANT ALTER SESSION TO FRAUDLENS_USER;
GRANT UNLIMITED TABLESPACE TO FRAUDLENS_USER;

-- Ensure FREEPDB1 opens automatically on system reboot
ALTER PLUGGABLE DATABASE SAVE STATE;
```

---

## 3. How to Connect

### Via SQL*Plus (Command Line)
```cmd
sqlplus FRAUDLENS_USER/<your_password>@localhost:1521/freepdb1
```
*(Note: Replace `<your_password>` with the password specified during user creation)*

### Via Oracle SQL Developer (GUI)
1. Open SQL Developer.
2. Click the green **+** icon (New Connection).
3. Fill in:
   * **Connection Name**: `FraudLens_PDB`
   * **Username**: `FRAUDLENS_USER`
   * **Password**: *(your password)*
   * **Connection Type**: Basic
   * **Hostname**: `localhost`
   * **Port**: `1521`
   * **Service Name**: `freepdb1`
4. Click **Test** (Status should be *Success*), then click **Connect**.

---

## 4. Executing the Project Pipeline

To run the complete FraudLens project non-interactively from start to finish:

1. Open Command Prompt in the `sql/` directory:
   ```cmd
   cd C:\Users\Steven\OneDrive\Desktop\dbms\sql
   ```
2. Launch SQL*Plus:
   ```cmd
   sqlplus FRAUDLENS_USER/<your_password>@//localhost:1521/freepdb1 @00_run_all.sql
   ```

The master script `00_run_all.sql` automatically coordinates execution of all 11 modules in dependency order:
* `01_schema.sql`: Sequences, Tables, Primary/Foreign Keys, and Check Constraints.
* `02_ddl_dml_demos.sql`: Schema Alteration demos (ALTER, DROP) and safe DML under savepoints.
* `03_sample_data.sql`: 56 baseline records with realistic Indian banking amounts.
* `04_review1_queries.sql`: Character, math, date single-row functions, range filters, and group aggregations.
* `05_review2_subqueries_joins.sql`: Scalar, multi-row, and correlated subqueries, plus 6-table Relational Dossier.
* `06_views.sql`: Analytical & surveillance views (`VW_HIGH_RISK_TRANSACTIONS`, `VW_INVESTIGATION_SUMMARY`, etc.).
* `07_procedures.sql`: Stored procedures for investigator assignment and case state updates.
* `08_functions.sql`: Stored functions for risk tiers and account volume.
* `09_cursors.sql`: Explicit cursors and parameterized cursor FOR loops.
* `10_triggers_audit.sql`: Row-level AFTER UPDATE audit triggers.
* `11_test_cases.sql`: 13 automated positive and negative test cases.

---

## 5. Automated Evidence Generation

To rerun the automated test harness and update execution evidence:
```cmd
python scripts\execute_oracle_pipeline.py
python scripts\generate_oracle_evidence_images.py
```
All outputs and console screenshots are saved directly to `evidence/oracle/`.
