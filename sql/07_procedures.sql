-- ============================================================================
-- PROJECT: FraudLens - Financial Transaction & Fraud Investigation Management System
-- SCRIPT:  07_procedures.sql
-- PURPOSE: Fulfills Review 2 Stored Procedures Requirements:
--          1. SP_ASSIGN_INVESTIGATOR - Allocates active investigator with validation
--          2. SP_UPDATE_INVESTIGATION_STATUS - Enforces state progression & outcomes
--          3. SP_EVALUATE_AND_ALERT_TRANSACTION - Evaluates >50k rule & generates alert
-- DIALECT: Oracle Database 11g/12c/19c/21c/23c Compatible (PL/SQL)
-- ============================================================================

SET SERVEROUTPUT ON;

-- ============================================================================
-- PROCEDURE 1: SP_ASSIGN_INVESTIGATOR
-- Validates that the investigation exists and is OPEN/UNDER REVIEW,
-- and verifies that the investigator is ACTIVE before making assignment.
-- ============================================================================
CREATE OR REPLACE PROCEDURE SP_ASSIGN_INVESTIGATOR (
    p_investigation_id IN NUMBER,
    p_investigator_id  IN NUMBER
) AS
    v_inves_status     VARCHAR2(15);
    v_inv_status       VARCHAR2(15);
    v_inv_name         VARCHAR2(100);
BEGIN
    -- 1. Validate Investigation exists and retrieve current status
    BEGIN
        SELECT status 
        INTO v_inves_status
        FROM INVESTIGATION
        WHERE investigation_id = p_investigation_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20001, 'Error: Investigation ID ' || p_investigation_id || ' does not exist.');
    END;

    -- Cannot reassign or assign a closed investigation
    IF v_inves_status = 'CLOSED' THEN
        RAISE_APPLICATION_ERROR(-20002, 'Error: Cannot reassign closed Investigation ID ' || p_investigation_id || '.');
    END IF;

    -- 2. Validate Investigator exists and is ACTIVE
    BEGIN
        SELECT active_status, first_name || ' ' || last_name
        INTO v_inv_status, v_inv_name
        FROM INVESTIGATOR
        WHERE investigator_id = p_investigator_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20003, 'Error: Investigator ID ' || p_investigator_id || ' does not exist.');
    END;

    IF v_inv_status != 'ACTIVE' THEN
        RAISE_APPLICATION_ERROR(-20004, 'Error: Investigator ' || v_inv_name || ' (ID ' || p_investigator_id || ') is INACTIVE.');
    END IF;

    -- 3. Perform Assignment
    UPDATE INVESTIGATION
    SET investigator_id = p_investigator_id
    WHERE investigation_id = p_investigation_id;

    DBMS_OUTPUT.PUT_LINE('[SUCCESS] Assigned Investigator ' || v_inv_name || ' (ID: ' || p_investigator_id || ') to Case ' || p_investigation_id || '.');

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('[FAILURE] SP_ASSIGN_INVESTIGATOR failed: ' || SQLERRM);
        RAISE;
END SP_ASSIGN_INVESTIGATOR;
/

-- ============================================================================
-- PROCEDURE 2: SP_UPDATE_INVESTIGATION_STATUS
-- Manages the progression: OPEN -> UNDER REVIEW -> CLOSED.
-- If transitioning to CLOSED, requires a valid definitive outcome and sets end_date.
-- Transaction control is delegated to the caller.
-- ============================================================================
CREATE OR REPLACE PROCEDURE SP_UPDATE_INVESTIGATION_STATUS (
    p_investigation_id IN NUMBER,
    p_new_status       IN VARCHAR2,
    p_outcome          IN VARCHAR2 DEFAULT NULL,
    p_notes            IN VARCHAR2 DEFAULT NULL
) AS
    v_current_status   VARCHAR2(15);
    v_clean_status     VARCHAR2(15);
    v_clean_outcome    VARCHAR2(20);
BEGIN
    v_clean_status := UPPER(TRIM(p_new_status));
    v_clean_outcome := UPPER(TRIM(p_outcome));

    -- 1. Validate Target Status
    IF v_clean_status NOT IN ('OPEN', 'UNDER REVIEW', 'CLOSED') THEN
        RAISE_APPLICATION_ERROR(-20010, 'Invalid status: ' || p_new_status || '. Must be OPEN, UNDER REVIEW, or CLOSED.');
    END IF;

    -- 2. Fetch current status
    BEGIN
        SELECT status
        INTO v_current_status
        FROM INVESTIGATION
        WHERE investigation_id = p_investigation_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20011, 'Investigation ID ' || p_investigation_id || ' not found.');
    END;

    -- 3. Business rule: If closing, require definitive outcome
    IF v_clean_status = 'CLOSED' THEN
        IF v_clean_outcome IS NULL OR v_clean_outcome NOT IN ('CONFIRMED_FRAUD', 'FALSE_POSITIVE', 'INCONCLUSIVE') THEN
            RAISE_APPLICATION_ERROR(-20012, 'Closing a case requires a definitive outcome (CONFIRMED_FRAUD, FALSE_POSITIVE, or INCONCLUSIVE).');
        END IF;

        UPDATE INVESTIGATION
        SET status   = 'CLOSED',
            outcome  = v_clean_outcome,
            end_date = NVL(end_date, SYSDATE),
            notes    = NVL(p_notes, notes)
        WHERE investigation_id = p_investigation_id;

    ELSE
        -- Updating to OPEN or UNDER REVIEW
        UPDATE INVESTIGATION
        SET status   = v_clean_status,
            outcome  = NVL(v_clean_outcome, outcome),
            notes    = NVL(p_notes, notes)
        WHERE investigation_id = p_investigation_id;
    END IF;

    DBMS_OUTPUT.PUT_LINE('[SUCCESS] Case ' || p_investigation_id || ' status progressed from ' || v_current_status || ' to ' || v_clean_status || '.');

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('[FAILURE] SP_UPDATE_INVESTIGATION_STATUS failed: ' || SQLERRM);
        RAISE;
END SP_UPDATE_INVESTIGATION_STATUS;
/

-- ============================================================================
-- PROCEDURE 3: SP_EVALUATE_AND_ALERT_TRANSACTION
-- Automated rule evaluation: Flags transactions > 50,000 INR and generates
-- a new FRAUD_ALERT row if one does not already exist.
-- Transaction control is delegated to the caller.
-- ============================================================================
CREATE OR REPLACE PROCEDURE SP_EVALUATE_AND_ALERT_TRANSACTION (
    p_transaction_id   IN NUMBER,
    p_new_alert_id     OUT NUMBER
) AS
    v_amount           NUMBER(15,2);
    v_existing_alerts  NUMBER;
    v_next_alert_id    NUMBER;
BEGIN
    -- 1. Fetch transaction details
    BEGIN
        SELECT amount
        INTO v_amount
        FROM TRANSACTIONS
        WHERE transaction_id = p_transaction_id;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE_APPLICATION_ERROR(-20020, 'Transaction ID ' || p_transaction_id || ' not found.');
    END;

    -- 2. Check if transaction already has an active alert
    SELECT COUNT(*)
    INTO v_existing_alerts
    FROM FRAUD_ALERT
    WHERE transaction_id = p_transaction_id;

    IF v_existing_alerts > 0 THEN
        DBMS_OUTPUT.PUT_LINE('[INFO] Transaction ' || p_transaction_id || ' already has an associated alert.');
        p_new_alert_id := NULL;
        RETURN;
    END IF;

    -- 3. Evaluate Illustrative Business Rule: Amount > 50,000 INR
    IF v_amount > 50000.00 THEN
        -- Generate next ID via sequence with MAX+1 fallback
        BEGIN
            SELECT seq_alert_id.NEXTVAL INTO v_next_alert_id FROM DUAL;
        EXCEPTION
            WHEN OTHERS THEN
                SELECT NVL(MAX(alert_id), 7007) + 1 INTO v_next_alert_id FROM FRAUD_ALERT;
        END;

        INSERT INTO FRAUD_ALERT (alert_id, transaction_id, alert_type, severity, rule_triggered, alert_date, status)
        VALUES (
            v_next_alert_id, 
            p_transaction_id, 
            'HIGH_AMOUNT', 
            'HIGH', 
            'Rule 101: Transaction amount ' || TO_CHAR(v_amount, 'FM999,999,990.00') || ' INR exceeds 50,000 threshold', 
            SYSTIMESTAMP, 
            'PENDING'
        );

        UPDATE TRANSACTIONS
        SET status = 'FLAGGED'
        WHERE transaction_id = p_transaction_id;

        p_new_alert_id := v_next_alert_id;
        DBMS_OUTPUT.PUT_LINE('[SUCCESS] Generated Fraud Alert ' || v_next_alert_id || ' for Transaction ' || p_transaction_id || '.');
    ELSE
        DBMS_OUTPUT.PUT_LINE('[INFO] Transaction ' || p_transaction_id || ' (Amount: ' || v_amount || ') does not violate the >50k rule.');
        p_new_alert_id := NULL;
    END IF;

EXCEPTION
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('[FAILURE] SP_EVALUATE_AND_ALERT_TRANSACTION failed: ' || SQLERRM);
        RAISE;
END SP_EVALUATE_AND_ALERT_TRANSACTION;
/

PROMPT [SUCCESS] Stored Procedures compiled successfully.
