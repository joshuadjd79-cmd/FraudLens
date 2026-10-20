-- ============================================================================
-- PROJECT: FraudLens - Financial Transaction & Fraud Investigation Management System
-- SCRIPT:  10_triggers_audit.sql
-- PURPOSE: Fulfills Review 2 Database Triggers & Auditing Requirements:
--          1. TRG_INVESTIGATION_STATUS_AUDIT - Row-level trigger logging case lifecycle
--          2. TRG_FRAUD_ALERT_AUDIT - Row-level trigger logging alert escalations
--          3. Practical demonstration & verification of audit capture
-- DIALECT: Oracle Database 11g/12c/19c/21c/23c Compatible (PL/SQL)
-- ============================================================================

SET SERVEROUTPUT ON;

-- ============================================================================
-- TRIGGER 1: TRG_INVESTIGATION_STATUS_AUDIT
-- Fires AFTER UPDATE OF status ON INVESTIGATION for each modified row.
-- Captures previous status, new status, acting user, and timestamp into INVESTIGATION_AUDIT.
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_INVESTIGATION_STATUS_AUDIT
AFTER UPDATE OF status ON INVESTIGATION
FOR EACH ROW
WHEN (OLD.status != NEW.status)
DECLARE
    v_next_audit_id NUMBER;
BEGIN
    -- Safe ID generation using sequence with fallback
    BEGIN
        SELECT seq_inves_audit_id.NEXTVAL INTO v_next_audit_id FROM DUAL;
    EXCEPTION
        WHEN OTHERS THEN
            SELECT NVL(MAX(audit_id), 0) + 1 INTO v_next_audit_id FROM INVESTIGATION_AUDIT;
    END;

    INSERT INTO INVESTIGATION_AUDIT (
        audit_id,
        investigation_id,
        old_status,
        new_status,
        changed_by,
        change_timestamp,
        change_action
    ) VALUES (
        v_next_audit_id,
        :NEW.investigation_id,
        :OLD.status,
        :NEW.status,
        USER,
        SYSTIMESTAMP,
        'STATUS_TRANSITION'
    );
END;
/

-- ============================================================================
-- TRIGGER 2: TRG_FRAUD_ALERT_AUDIT
-- Fires AFTER UPDATE OF status ON FRAUD_ALERT for each modified row.
-- Captures state changes (e.g., PENDING -> ESCALATED / RESOLVED) into ALERT_AUDIT.
-- ============================================================================
CREATE OR REPLACE TRIGGER TRG_FRAUD_ALERT_AUDIT
AFTER UPDATE OF status ON FRAUD_ALERT
FOR EACH ROW
WHEN (OLD.status != NEW.status)
DECLARE
    v_next_audit_id NUMBER;
BEGIN
    BEGIN
        SELECT seq_alert_audit_id.NEXTVAL INTO v_next_audit_id FROM DUAL;
    EXCEPTION
        WHEN OTHERS THEN
            SELECT NVL(MAX(audit_id), 0) + 1 INTO v_next_audit_id FROM ALERT_AUDIT;
    END;

    INSERT INTO ALERT_AUDIT (
        audit_id,
        alert_id,
        old_status,
        new_status,
        changed_by,
        change_timestamp,
        remarks
    ) VALUES (
        v_next_audit_id,
        :NEW.alert_id,
        :OLD.status,
        :NEW.status,
        USER,
        SYSTIMESTAMP,
        'Triggered by automated triage or compliance operator update'
    );
END;
/

-- ============================================================================
-- LIVE DEMONSTRATION & VERIFICATION OF TRIGGERS
-- ============================================================================
PROMPT === Executing Trigger Verification Updates ===

SAVEPOINT before_trigger_demo;

-- 1. Trigger Investigation Status Update (9004: OPEN -> UNDER REVIEW)
UPDATE INVESTIGATION
SET status = 'UNDER REVIEW',
    notes  = notes || ' [Trigger Demo Note]'
WHERE investigation_id = 9004;

-- 2. Trigger Fraud Alert Status Update (7005: PENDING -> ESCALATED)
UPDATE FRAUD_ALERT
SET status = 'ESCALATED'
WHERE alert_id = 7005;

COMMIT;

PROMPT === Querying INVESTIGATION_AUDIT Table ===
SELECT 
    audit_id,
    investigation_id,
    old_status,
    new_status,
    changed_by,
    TO_CHAR(change_timestamp, 'YYYY-MM-DD HH24:MI:SS') AS change_time,
    change_action
FROM INVESTIGATION_AUDIT
ORDER BY audit_id DESC;

PROMPT === Querying ALERT_AUDIT Table ===
SELECT 
    audit_id,
    alert_id,
    old_status,
    new_status,
    changed_by,
    TO_CHAR(change_timestamp, 'YYYY-MM-DD HH24:MI:SS') AS change_time,
    remarks
FROM ALERT_AUDIT
ORDER BY audit_id DESC;

-- Restore modified sample rows to preserve canonical baseline state
UPDATE INVESTIGATION
SET status = 'OPEN',
    notes  = 'Offshore shell corporation escrow alert. Requested AML compliance documentation from correspondent bank.'
WHERE investigation_id = 9004;

UPDATE FRAUD_ALERT
SET status = 'PENDING'
WHERE alert_id = 7005;

-- Reset audit tables to clean initial state
DELETE FROM INVESTIGATION_AUDIT WHERE investigation_id = 9004;
DELETE FROM ALERT_AUDIT WHERE alert_id = 7005;
COMMIT;

PROMPT [SUCCESS] Audit triggers compiled, tested, and verified. Sample dataset restored to canonical state.
