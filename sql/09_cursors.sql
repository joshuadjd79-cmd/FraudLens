-- ============================================================================
-- PROJECT: FraudLens - Financial Transaction & Fraud Investigation Management System
-- SCRIPT:  09_cursors.sql
-- PURPOSE: Fulfills Review 2 Database Cursor Requirements:
--          1. Explicit Cursor (OPEN, FETCH, %FOUND, %NOTFOUND, CLOSE)
--             Processes high-risk fraud alerts and computes flagged exposure.
--          2. Parameterized Cursor FOR Loop
--             Batch processes pending cases and prints an investigation docket.
-- DIALECT: Oracle Database 11g/12c/19c/21c/23c Compatible (PL/SQL)
-- ============================================================================

SET SERVEROUTPUT ON SIZE 1000000;

PROMPT ============================================================================
PROMPT DEMO 1: EXPLICIT CURSOR - High Risk Fraud Alert Surveillance Docket
PROMPT ============================================================================

DECLARE
    -- 1. Declare explicit cursor for CRITICAL and HIGH severity alerts
    CURSOR cur_high_risk_alerts IS
        SELECT 
            fa.alert_id,
            fa.alert_type,
            fa.severity,
            fa.rule_triggered,
            t.transaction_id,
            t.amount,
            t.channel,
            a.account_number,
            c.first_name || ' ' || c.last_name AS customer_name
        FROM FRAUD_ALERT fa
        JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id
        JOIN ACCOUNT a ON t.account_id = a.account_id
        JOIN CUSTOMER c ON a.customer_id = c.customer_id
        WHERE fa.severity IN ('CRITICAL', 'HIGH')
        ORDER BY t.amount DESC;

    -- Record variable to hold fetched row
    v_alert_rec         cur_high_risk_alerts%ROWTYPE;
    v_processed_count   PLS_INTEGER := 0;
    v_total_exposure    NUMBER(15,2) := 0.00;

BEGIN
    DBMS_OUTPUT.PUT_LINE('------------------------------------------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE(RPAD('ALERT ID', 10) || RPAD('SEVERITY', 12) || RPAD('TYPE', 20) || RPAD('AMOUNT (INR)', 15) || RPAD('ACCOUNT', 14) || 'CUSTOMER');
    DBMS_OUTPUT.PUT_LINE('------------------------------------------------------------------------------------------------------');

    -- 2. Open the explicit cursor
    OPEN cur_high_risk_alerts;

    -- 3. Fetch loop using %NOTFOUND condition
    LOOP
        FETCH cur_high_risk_alerts INTO v_alert_rec;
        EXIT WHEN cur_high_risk_alerts%NOTFOUND;

        v_processed_count := v_processed_count + 1;
        v_total_exposure  := v_total_exposure + v_alert_rec.amount;

        DBMS_OUTPUT.PUT_LINE(
            RPAD(TO_CHAR(v_alert_rec.alert_id), 10) ||
            RPAD(v_alert_rec.severity, 12) ||
            RPAD(v_alert_rec.alert_type, 20) ||
            RPAD(TO_CHAR(v_alert_rec.amount, '999,999,990.00'), 15) ||
            RPAD(v_alert_rec.account_number, 14) ||
            v_alert_rec.customer_name
        );
        DBMS_OUTPUT.PUT_LINE('   Rule: ' || v_alert_rec.rule_triggered);
    END LOOP;

    -- 4. Close the explicit cursor
    CLOSE cur_high_risk_alerts;

    DBMS_OUTPUT.PUT_LINE('------------------------------------------------------------------------------------------------------');
    DBMS_OUTPUT.PUT_LINE('TOTAL ALERTS PROCESSED : ' || v_processed_count);
    DBMS_OUTPUT.PUT_LINE('CUMULATIVE RISK EXPOSURE: ' || TO_CHAR(v_total_exposure, '999,999,990.00') || ' INR');
    DBMS_OUTPUT.PUT_LINE('------------------------------------------------------------------------------------------------------');

EXCEPTION
    WHEN OTHERS THEN
        IF cur_high_risk_alerts%ISOPEN THEN
            CLOSE cur_high_risk_alerts;
        END IF;
        DBMS_OUTPUT.PUT_LINE('[ERROR] Explicit cursor execution failed: ' || SQLERRM);
        RAISE;
END;
/

PROMPT ============================================================================
PROMPT DEMO 2: PARAMETERIZED CURSOR FOR LOOP - Active Investigations Caseload
PROMPT ============================================================================

DECLARE
    -- Cursor with parameter for filtering by investigation status
    CURSOR cur_caseload (p_status VARCHAR2) IS
        SELECT 
            inv.investigation_id,
            inv.status,
            inv.start_date,
            NVL(i.first_name || ' ' || i.last_name, 'UNASSIGNED') AS investigator_name,
            NVL(i.department, 'N/A') AS department,
            fa.alert_type,
            fa.severity,
            t.amount
        FROM INVESTIGATION inv
        JOIN FRAUD_ALERT fa ON inv.alert_id = fa.alert_id
        JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id
        LEFT JOIN INVESTIGATOR i ON inv.investigator_id = i.investigator_id
        WHERE inv.status = p_status
        ORDER BY inv.start_date ASC;

    v_case_count PLS_INTEGER := 0;

BEGIN
    DBMS_OUTPUT.PUT_LINE('>>> ACTIVE CASELOAD FOR STATUS: [UNDER REVIEW] <<<');
    DBMS_OUTPUT.PUT_LINE('------------------------------------------------------------------------------------------------------');

    -- Cursor FOR loop automatically manages OPEN, FETCH, and CLOSE
    FOR r IN cur_caseload('UNDER REVIEW') LOOP
        v_case_count := v_case_count + 1;
        DBMS_OUTPUT.PUT_LINE(
            'Case #' || r.investigation_id || 
            ' | Lead: ' || RPAD(r.investigator_name, 18) || 
            ' | Dept: ' || RPAD(r.department, 22) || 
            ' | Alert: ' || RPAD(r.alert_type, 18) || 
            ' | Value: ' || TO_CHAR(r.amount, '999,990.00') || ' INR'
        );
    END LOOP;

    DBMS_OUTPUT.PUT_LINE('Total cases currently under active review: ' || v_case_count);
    DBMS_OUTPUT.PUT_LINE('------------------------------------------------------------------------------------------------------');
END;
/

PROMPT [SUCCESS] Cursor scripts executed successfully.
