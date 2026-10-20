-- ============================================================================
-- PROJECT: FraudLens - Financial Transaction & Fraud Investigation Management System
-- SCRIPT:  02_ddl_dml_demos.sql
-- PURPOSE: Academic Demonstrations for Review 1:
--          1. DDL: CREATE (demonstrated via staging table), ALTER (ADD, MODIFY, 
--             DROP, RENAME, ADD CONSTRAINT, DROP CONSTRAINT), DROP.
--          2. DML: INSERT, UPDATE, DELETE with rollback/commit boundaries.
-- DIALECT: Oracle Database 11g/12c/19c/21c/23c Compatible
-- ============================================================================

SET SERVEROUTPUT ON;

-- ============================================================================
-- SECTION 1: DDL DEMONSTRATIONS (ALTER & DROP SAFEGUARDED)
-- We demonstrate full DDL capabilities on an auxiliary table 'FRAUD_RULE_CONFIG'
-- so core business entities remain pristine and consistent.
-- ============================================================================

-- 1.1 CREATE TABLE demonstration with column-level constraints
CREATE TABLE FRAUD_RULE_CONFIG (
    rule_id          NUMBER(5)           CONSTRAINT pk_rule_config PRIMARY KEY,
    rule_code        VARCHAR2(30)        NOT NULL,
    threshold_value  NUMBER(12,2)        DEFAULT 50000.00 NOT NULL,
    is_active        CHAR(1)             DEFAULT 'Y' CONSTRAINT chk_rule_active CHECK (is_active IN ('Y', 'N')),
    created_date     DATE                DEFAULT SYSDATE
);

-- 1.2 ALTER: Add a new column
ALTER TABLE FRAUD_RULE_CONFIG 
ADD (rule_description VARCHAR2(250));

-- 1.3 ALTER: Modify an existing column (expand datatype length)
ALTER TABLE FRAUD_RULE_CONFIG 
MODIFY (rule_code VARCHAR2(60));

-- 1.4 ALTER: Add a new UNIQUE constraint
ALTER TABLE FRAUD_RULE_CONFIG 
ADD CONSTRAINT uq_rule_code UNIQUE (rule_code);

-- 1.5 ALTER: Add a CHECK constraint to enforce non-negative threshold
ALTER TABLE FRAUD_RULE_CONFIG 
ADD CONSTRAINT chk_rule_threshold CHECK (threshold_value >= 0);

-- 1.6 ALTER: Rename a column
ALTER TABLE FRAUD_RULE_CONFIG 
RENAME COLUMN is_active TO status_flag;

-- 1.7 ALTER: Drop a constraint
ALTER TABLE FRAUD_RULE_CONFIG 
DROP CONSTRAINT chk_rule_threshold;

-- 1.8 ALTER: Drop a column
ALTER TABLE FRAUD_RULE_CONFIG 
DROP COLUMN rule_description;

-- 1.9 DROP TABLE demonstration (with PURGE to bypass recyclebin)
DROP TABLE FRAUD_RULE_CONFIG PURGE;

-- ============================================================================
-- SECTION 2: DML DEMONSTRATIONS (INSERT, UPDATE, DELETE)
-- Demonstrates row operations, constraint enforcement, and transactional integrity.
-- ============================================================================

-- Savepoint before demonstration
SAVEPOINT dml_demo_start;

-- 2.1 INSERT: Basic row insert into CUSTOMER
INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score, created_at)
VALUES (9999, 'Test', 'Subject', 'test.subject@fraudlens-demo.com', '+919999900001', 'PENDING', 15, SYSDATE);

-- 2.2 INSERT with DEFAULT values (omitting defaults to let table defaults populate)
INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone)
VALUES (9998, 'Default', 'Tester', 'default.tester@fraudlens-demo.com', '+919999900002');

-- Verify inserted rows
SELECT customer_id, first_name, last_name, email, kyc_status, risk_score 
FROM CUSTOMER 
WHERE customer_id IN (9998, 9999);

-- 2.3 UPDATE: Modify customer KYC status and adjust risk score
UPDATE CUSTOMER
SET kyc_status = 'VERIFIED',
    risk_score = 5
WHERE customer_id = 9999;

-- Verify update
SELECT customer_id, first_name, last_name, kyc_status, risk_score 
FROM CUSTOMER 
WHERE customer_id = 9999;

-- 2.4 UPDATE with expression: Increment risk score by 10 for pending customers
UPDATE CUSTOMER
SET risk_score = LEAST(100, risk_score + 10)
WHERE kyc_status = 'PENDING'
  AND customer_id = 9998;

-- 2.5 DELETE: Remove the demo test subjects
DELETE FROM CUSTOMER
WHERE customer_id IN (9998, 9999);

-- Verify deletion completed
SELECT COUNT(*) AS remaining_test_records 
FROM CUSTOMER 
WHERE customer_id IN (9998, 9999);

-- Roll back to clean state so sample data script has a pristine starting point
ROLLBACK TO dml_demo_start;

PROMPT [SUCCESS] 02_ddl_dml_demos.sql executed successfully. All temporary rows rolled back.
