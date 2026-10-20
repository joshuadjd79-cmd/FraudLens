-- ============================================================================
-- PROJECT: FraudLens - Financial Transaction & Fraud Investigation Management System
-- SCRIPT:  08_functions.sql
-- PURPOSE: Fulfills Review 2 Stored Functions Requirements:
--          1. FN_GET_TOTAL_TX_AMOUNT - Returns cumulative transacted volume for an account
--          2. FN_GET_ACCOUNT_ALERT_COUNT - Returns total alerts triggered by an account
--          3. FN_CALCULATE_RISK_TIER - Classifies customer risk score into tier brackets
-- DIALECT: Oracle Database 11g/12c/19c/21c/23c Compatible (PL/SQL)
-- ============================================================================

SET SERVEROUTPUT ON;

-- ============================================================================
-- FUNCTION 1: FN_GET_TOTAL_TX_AMOUNT
-- Returns the cumulative transaction amount for a given account.
-- Handles accounts with zero transactions gracefully (returns 0.00).
-- Raises application error if account does not exist.
-- ============================================================================
CREATE OR REPLACE FUNCTION FN_GET_TOTAL_TX_AMOUNT (
    p_account_id IN NUMBER
) RETURN NUMBER AS
    v_acc_exists    NUMBER;
    v_total_amount  NUMBER(15,2);
BEGIN
    -- 1. Validate that account exists
    SELECT COUNT(*)
    INTO v_acc_exists
    FROM ACCOUNT
    WHERE account_id = p_account_id;

    IF v_acc_exists = 0 THEN
        RAISE_APPLICATION_ERROR(-20030, 'Account ID ' || p_account_id || ' does not exist.');
    END IF;

    -- 2. Aggregate transactions
    SELECT NVL(SUM(amount), 0.00)
    INTO v_total_amount
    FROM TRANSACTIONS
    WHERE account_id = p_account_id;

    RETURN v_total_amount;

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('[ERROR] FN_GET_TOTAL_TX_AMOUNT failed: ' || SQLERRM);
        RAISE;
END FN_GET_TOTAL_TX_AMOUNT;
/

-- ============================================================================
-- FUNCTION 2: FN_GET_ACCOUNT_ALERT_COUNT
-- Returns the number of fraud alerts generated across all transactions for an account.
-- ============================================================================
CREATE OR REPLACE FUNCTION FN_GET_ACCOUNT_ALERT_COUNT (
    p_account_id IN NUMBER
) RETURN NUMBER AS
    v_acc_exists   NUMBER;
    v_alert_count  NUMBER;
BEGIN
    SELECT COUNT(*)
    INTO v_acc_exists
    FROM ACCOUNT
    WHERE account_id = p_account_id;

    IF v_acc_exists = 0 THEN
        RAISE_APPLICATION_ERROR(-20031, 'Account ID ' || p_account_id || ' does not exist.');
    END IF;

    SELECT COUNT(fa.alert_id)
    INTO v_alert_count
    FROM TRANSACTIONS t
    JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id
    WHERE t.account_id = p_account_id;

    RETURN v_alert_count;

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('[ERROR] FN_GET_ACCOUNT_ALERT_COUNT failed: ' || SQLERRM);
        RAISE;
END FN_GET_ACCOUNT_ALERT_COUNT;
/

-- ============================================================================
-- FUNCTION 3: FN_CALCULATE_RISK_TIER
-- Classifies a customer's numeric risk score (0-100) into a qualitative tier.
-- ============================================================================
CREATE OR REPLACE FUNCTION FN_CALCULATE_RISK_TIER (
    p_customer_id IN NUMBER
) RETURN VARCHAR2 AS
    v_score NUMBER(3);
BEGIN
    SELECT risk_score
    INTO v_score
    FROM CUSTOMER
    WHERE customer_id = p_customer_id;

    IF v_score BETWEEN 0 AND 25 THEN
        RETURN 'LOW_RISK';
    ELSIF v_score BETWEEN 26 AND 50 THEN
        RETURN 'MODERATE_RISK';
    ELSIF v_score BETWEEN 51 AND 75 THEN
        RETURN 'HIGH_RISK';
    ELSE
        RETURN 'CRITICAL_RISK';
    END IF;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        RAISE_APPLICATION_ERROR(-20032, 'Customer ID ' || p_customer_id || ' not found.');
    WHEN OTHERS THEN
        RAISE;
END FN_CALCULATE_RISK_TIER;
/

-- ============================================================================
-- DEMONSTRATION & VERIFICATION OF FUNCTIONS IN SQL QUERIES
-- ============================================================================
PROMPT === Testing Stored Functions in SQL Statements ===

SELECT 
    a.account_id,
    a.account_number,
    a.account_type,
    a.balance,
    FN_GET_TOTAL_TX_AMOUNT(a.account_id) AS total_transacted_volume,
    FN_GET_ACCOUNT_ALERT_COUNT(a.account_id) AS fraud_alerts_count
FROM ACCOUNT a
ORDER BY total_transacted_volume DESC;

SELECT 
    customer_id,
    first_name || ' ' || last_name AS customer_name,
    risk_score,
    FN_CALCULATE_RISK_TIER(customer_id) AS computed_risk_tier
FROM CUSTOMER
ORDER BY risk_score DESC;
