-- ============================================================================
-- PROJECT: FraudLens - Financial Transaction & Fraud Investigation Management System
-- SCRIPT:  01_schema.sql
-- PURPOSE: Core DDL - Tables, Sequences, Primary Keys, Foreign Keys, 
--          Unique Constraints, Check Constraints, and Defaults.
-- DIALECT: Oracle Database 11g/12c/19c/21c/23c Compatible
-- ============================================================================

-- Clean up existing objects if re-running (safe drop in reverse dependency order)
BEGIN
    FOR t IN (SELECT table_name FROM user_tables WHERE table_name IN (
        'ALERT_AUDIT', 'INVESTIGATION_AUDIT', 'INVESTIGATION', 'INVESTIGATOR', 
        'FRAUD_ALERT', 'TRANSACTIONS', 'ACCOUNT', 'CUSTOMER'
    )) LOOP
        EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS PURGE';
    END LOOP;
END;
/

BEGIN
    FOR s IN (SELECT sequence_name FROM user_sequences WHERE sequence_name IN (
        'SEQ_CUSTOMER_ID', 'SEQ_ACCOUNT_ID', 'SEQ_TRANSACTION_ID', 
        'SEQ_ALERT_ID', 'SEQ_INVESTIGATOR_ID', 'SEQ_INVESTIGATION_ID',
        'SEQ_INVES_AUDIT_ID', 'SEQ_ALERT_AUDIT_ID'
    )) LOOP
        EXECUTE IMMEDIATE 'DROP SEQUENCE ' || s.sequence_name;
    END LOOP;
END;
/

-- ============================================================================
-- 1. SEQUENCES FOR PRIMARY KEY GENERATION
-- ============================================================================
CREATE SEQUENCE seq_customer_id      START WITH 1001 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_account_id       START WITH 2001 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_transaction_id   START WITH 50001 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_alert_id         START WITH 7001 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_investigator_id  START WITH 301  INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_investigation_id START WITH 9001 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_inves_audit_id   START WITH 1    INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_alert_audit_id   START WITH 1    INCREMENT BY 1 NOCACHE;

-- ============================================================================
-- 2. CORE TABLE: CUSTOMER
-- Represents the retail and corporate banking clients.
-- ============================================================================
CREATE TABLE CUSTOMER (
    customer_id      NUMBER(10)          CONSTRAINT pk_customer PRIMARY KEY,
    first_name       VARCHAR2(50)        NOT NULL,
    last_name        VARCHAR2(50)        NOT NULL,
    email            VARCHAR2(100)       CONSTRAINT uq_customer_email UNIQUE NOT NULL,
    phone            VARCHAR2(15)        CONSTRAINT uq_customer_phone UNIQUE NOT NULL,
    kyc_status       VARCHAR2(15)        DEFAULT 'PENDING' 
                                         CONSTRAINT chk_cust_kyc 
                                         CHECK (kyc_status IN ('VERIFIED', 'PENDING', 'REJECTED')),
    risk_score       NUMBER(3)           DEFAULT 10 
                                         CONSTRAINT chk_cust_risk 
                                         CHECK (risk_score BETWEEN 0 AND 100),
    created_at       DATE                DEFAULT SYSDATE NOT NULL
);

COMMENT ON TABLE  CUSTOMER IS 'Core retail banking customer profile and baseline fraud risk indicator';
COMMENT ON COLUMN CUSTOMER.risk_score IS 'Customer baseline risk score calculated from KYC and historical behavior (0=Lowest, 100=Highest)';

-- ============================================================================
-- 3. CORE TABLE: ACCOUNT
-- Represents checking, savings, or current accounts owned by customers.
-- Business Rule: Each account belongs to exactly one customer (1:N).
-- ============================================================================
CREATE TABLE ACCOUNT (
    account_id       NUMBER(10)          CONSTRAINT pk_account PRIMARY KEY,
    customer_id      NUMBER(10)          CONSTRAINT fk_acc_customer 
                                         REFERENCES CUSTOMER(customer_id) 
                                         ON DELETE CASCADE NOT NULL,
    account_number   VARCHAR2(20)        CONSTRAINT uq_acc_number UNIQUE NOT NULL,
    account_type     VARCHAR2(20)        DEFAULT 'SAVINGS' 
                                         CONSTRAINT chk_acc_type 
                                         CHECK (account_type IN ('SAVINGS', 'CURRENT', 'SALARY', 'NRI')),
    balance          NUMBER(15,2)        DEFAULT 0.00 
                                         CONSTRAINT chk_acc_balance 
                                         CHECK (balance >= 0),
    currency         VARCHAR2(5)         DEFAULT 'INR' NOT NULL,
    status           VARCHAR2(15)        DEFAULT 'ACTIVE' 
                                         CONSTRAINT chk_acc_status 
                                         CHECK (status IN ('ACTIVE', 'FROZEN', 'DORMANT', 'CLOSED')),
    created_at       DATE                DEFAULT SYSDATE NOT NULL
);

COMMENT ON TABLE  ACCOUNT IS 'Bank accounts linked to customers; maintains operational balance and status';

-- ============================================================================
-- 4. CORE TABLE: TRANSACTIONS
-- Financial transactions performed via accounts.
-- Business Rule: Each transaction belongs to exactly one account.
-- Illustrative Rule: Amounts > 50,000 INR qualify as high-value thresholds.
-- ============================================================================
CREATE TABLE TRANSACTIONS (
    transaction_id       NUMBER(12)      CONSTRAINT pk_transactions PRIMARY KEY,
    account_id           NUMBER(10)      CONSTRAINT fk_tx_account 
                                         REFERENCES ACCOUNT(account_id) 
                                         ON DELETE CASCADE NOT NULL,
    transaction_type     VARCHAR2(20)    NOT NULL
                                         CONSTRAINT chk_tx_type 
                                         CHECK (transaction_type IN ('DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'PAYMENT')),
    amount               NUMBER(15,2)    CONSTRAINT chk_tx_amount 
                                         CHECK (amount > 0) NOT NULL,
    transaction_date     TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
    channel              VARCHAR2(20)    NOT NULL
                                         CONSTRAINT chk_tx_channel 
                                         CHECK (channel IN ('MOBILE_APP', 'NET_BANKING', 'ATM', 'POS', 'UPI')),
    status               VARCHAR2(15)    DEFAULT 'COMPLETED' 
                                         CONSTRAINT chk_tx_status 
                                         CHECK (status IN ('COMPLETED', 'PENDING', 'FLAGGED', 'FAILED')),
    counterparty_account VARCHAR2(30),
    description          VARCHAR2(200)
);

COMMENT ON TABLE  TRANSACTIONS IS 'Auditable financial movement records across banking channels';

-- ============================================================================
-- 5. CORE TABLE: FRAUD_ALERT
-- Automated anomaly signals flagged by rule engines.
-- Business Rule: Each fraud alert references a recorded transaction.
-- A fraud alert is a signal for investigation, NOT proof of fraud.
-- ============================================================================
CREATE TABLE FRAUD_ALERT (
    alert_id             NUMBER(10)      CONSTRAINT pk_fraud_alert PRIMARY KEY,
    transaction_id       NUMBER(12)      CONSTRAINT fk_alert_tx 
                                         REFERENCES TRANSACTIONS(transaction_id) 
                                         ON DELETE CASCADE NOT NULL,
    alert_type           VARCHAR2(30)    NOT NULL
                                         CONSTRAINT chk_alert_type 
                                         CHECK (alert_type IN ('HIGH_AMOUNT', 'RAPID_VELOCITY', 'SUSPICIOUS_CHANNEL', 'UNUSUAL_HOURS', 'CROSS_BORDER', 'STRUCTURING')),
    severity             VARCHAR2(15)    DEFAULT 'MEDIUM' 
                                         CONSTRAINT chk_alert_severity 
                                         CHECK (severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL')) NOT NULL,
    rule_triggered       VARCHAR2(150)   NOT NULL,
    alert_date           TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
    status               VARCHAR2(15)    DEFAULT 'PENDING' 
                                         CONSTRAINT chk_alert_status 
                                         CHECK (status IN ('PENDING', 'ESCALATED', 'DISMISSED', 'RESOLVED')) NOT NULL
);

COMMENT ON TABLE  FRAUD_ALERT IS 'Automated fraud risk signals generated from heuristic/velocity thresholds';

-- ============================================================================
-- 6. CORE TABLE: INVESTIGATOR
-- Compliance officers, anti-money laundering (AML), and fraud analysts.
-- ============================================================================
CREATE TABLE INVESTIGATOR (
    investigator_id      NUMBER(6)       CONSTRAINT pk_investigator PRIMARY KEY,
    first_name           VARCHAR2(50)    NOT NULL,
    last_name            VARCHAR2(50)    NOT NULL,
    email                VARCHAR2(100)   CONSTRAINT uq_inv_email UNIQUE NOT NULL,
    department           VARCHAR2(50)    NOT NULL,
    experience_years     NUMBER(3)       DEFAULT 0 
                                         CONSTRAINT chk_inv_exp 
                                         CHECK (experience_years >= 0),
    active_status        VARCHAR2(15)    DEFAULT 'ACTIVE' 
                                         CONSTRAINT chk_inv_status 
                                         CHECK (active_status IN ('ACTIVE', 'INACTIVE')) NOT NULL
);

COMMENT ON TABLE  INVESTIGATOR IS 'Authorized fraud analysts, compliance officers, and forensic investigators';

-- ============================================================================
-- 7. CORE TABLE: INVESTIGATION
-- The formal investigative case linking a fraud alert to an investigator.
-- Business Rules:
-- - Each investigation links an alert to an investigator.
-- - Status progresses through OPEN -> UNDER REVIEW -> CLOSED.
-- ============================================================================
CREATE TABLE INVESTIGATION (
    investigation_id     NUMBER(10)      CONSTRAINT pk_investigation PRIMARY KEY,
    alert_id             NUMBER(10)      CONSTRAINT fk_inv_alert 
                                         REFERENCES FRAUD_ALERT(alert_id) 
                                         ON DELETE CASCADE 
                                         CONSTRAINT uq_inv_alert UNIQUE NOT NULL,
    investigator_id      NUMBER(6)       CONSTRAINT fk_inv_investigator 
                                         REFERENCES INVESTIGATOR(investigator_id),
    start_date           DATE            DEFAULT SYSDATE NOT NULL,
    end_date             DATE,
    status               VARCHAR2(15)    DEFAULT 'OPEN' 
                                         CONSTRAINT chk_inves_status 
                                         CHECK (status IN ('OPEN', 'UNDER REVIEW', 'CLOSED')) NOT NULL,
    outcome              VARCHAR2(20)    DEFAULT 'PENDING' 
                                         CONSTRAINT chk_inves_outcome 
                                         CHECK (outcome IN ('CONFIRMED_FRAUD', 'FALSE_POSITIVE', 'INCONCLUSIVE', 'PENDING')) NOT NULL,
    notes                VARCHAR2(1000),
    CONSTRAINT chk_inves_dates CHECK (end_date IS NULL OR end_date >= start_date)
);

COMMENT ON TABLE  INVESTIGATION IS 'Formal case record documenting evidence, forensic notes, and verdict';

-- ============================================================================
-- 8. AUDIT TABLES (SUPPORTING REVIEW 2 TRIGGERS)
-- ============================================================================
CREATE TABLE INVESTIGATION_AUDIT (
    audit_id             NUMBER(10)      CONSTRAINT pk_inves_audit PRIMARY KEY,
    investigation_id     NUMBER(10)      NOT NULL,
    old_status           VARCHAR2(15),
    new_status           VARCHAR2(15),
    changed_by           VARCHAR2(50)    DEFAULT USER NOT NULL,
    change_timestamp     TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
    change_action        VARCHAR2(20)    DEFAULT 'STATUS_UPDATE' NOT NULL
);

CREATE TABLE ALERT_AUDIT (
    audit_id             NUMBER(10)      CONSTRAINT pk_alert_audit PRIMARY KEY,
    alert_id             NUMBER(10)      NOT NULL,
    old_status           VARCHAR2(15),
    new_status           VARCHAR2(15),
    changed_by           VARCHAR2(50)    DEFAULT USER NOT NULL,
    change_timestamp     TIMESTAMP       DEFAULT SYSTIMESTAMP NOT NULL,
    remarks              VARCHAR2(200)
);

-- Verification: Display created tables
SELECT table_name FROM user_tables WHERE table_name IN (
    'CUSTOMER', 'ACCOUNT', 'TRANSACTIONS', 'FRAUD_ALERT', 
    'INVESTIGATOR', 'INVESTIGATION', 'INVESTIGATION_AUDIT', 'ALERT_AUDIT'
) ORDER BY table_name;
