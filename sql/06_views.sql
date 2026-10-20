-- ============================================================================
-- PROJECT: FraudLens - Financial Transaction & Fraud Investigation Management System
-- SCRIPT:  06_views.sql
-- PURPOSE: Fulfills Review 2 Database Views Requirements:
--          1. VW_HIGH_RISK_TRANSACTIONS - Surveillance and anomaly monitoring
--          2. VW_INVESTIGATION_SUMMARY - Forensic case lifecycle dashboard
--          3. VW_CUSTOMER_FRAUD_EXPOSURE - Customer portfolio risk posture
--          4. VW_UNASSIGNED_ALERTS - Real-time triage queue for triage officers
-- DIALECT: Oracle Database 11g/12c/19c/21c/23c Compatible
-- ============================================================================

-- 1. VIEW: VW_HIGH_RISK_TRANSACTIONS
-- Surfaces high-ticket (>50k INR) or system-flagged transactions with customer context.
CREATE OR REPLACE VIEW VW_HIGH_RISK_TRANSACTIONS AS
SELECT 
    t.transaction_id,
    t.account_id,
    a.account_number,
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.risk_score AS customer_risk_score,
    t.transaction_type,
    t.amount,
    t.channel,
    t.transaction_date,
    t.status AS tx_status,
    t.counterparty_account,
    fa.alert_id,
    fa.alert_type,
    fa.severity AS alert_severity
FROM TRANSACTIONS t
JOIN ACCOUNT a ON t.account_id = a.account_id
JOIN CUSTOMER c ON a.customer_id = c.customer_id
LEFT JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id
WHERE t.amount > 50000.00 OR t.status = 'FLAGGED';

COMMENT ON TABLE VW_HIGH_RISK_TRANSACTIONS IS 'Surveillance view aggregating high-value and system-flagged transactions';

-- 2. VIEW: VW_INVESTIGATION_SUMMARY
-- Forensic dashboard showing case lifecycle, assigned investigator, and duration.
CREATE OR REPLACE VIEW VW_INVESTIGATION_SUMMARY AS
SELECT 
    inv.investigation_id,
    inv.status AS investigation_status,
    inv.outcome,
    fa.alert_id,
    fa.alert_type,
    fa.severity AS alert_severity,
    fa.rule_triggered,
    t.transaction_id,
    t.amount AS transaction_amount,
    i.investigator_id,
    NVL(i.first_name || ' ' || i.last_name, 'UNASSIGNED') AS lead_investigator,
    i.department,
    inv.start_date,
    inv.end_date,
    CASE 
        WHEN inv.end_date IS NOT NULL THEN (inv.end_date - inv.start_date)
        ELSE ROUND(SYSDATE - inv.start_date, 1)
    END AS duration_days
FROM INVESTIGATION inv
JOIN FRAUD_ALERT fa ON inv.alert_id = fa.alert_id
JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id
LEFT JOIN INVESTIGATOR i ON inv.investigator_id = i.investigator_id;

COMMENT ON TABLE VW_INVESTIGATION_SUMMARY IS 'Operational case management view displaying investigative outcomes and turnaround time';

-- 3. VIEW: VW_CUSTOMER_FRAUD_EXPOSURE
-- Aggregates customer-level risk, account counts, transacted volumes, and alert counts.
CREATE OR REPLACE VIEW VW_CUSTOMER_FRAUD_EXPOSURE AS
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.kyc_status,
    c.risk_score,
    COUNT(DISTINCT a.account_id) AS total_accounts,
    NVL(SUM(t.amount), 0) AS total_transacted_volume,
    COUNT(DISTINCT t.transaction_id) AS total_tx_count,
    COUNT(DISTINCT CASE WHEN t.status = 'FLAGGED' THEN t.transaction_id END) AS flagged_tx_count,
    COUNT(DISTINCT fa.alert_id) AS alerts_incurred
FROM CUSTOMER c
LEFT JOIN ACCOUNT a ON c.customer_id = a.customer_id
LEFT JOIN TRANSACTIONS t ON a.account_id = t.account_id
LEFT JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id
GROUP BY c.customer_id, c.first_name, c.last_name, c.kyc_status, c.risk_score;

COMMENT ON TABLE VW_CUSTOMER_FRAUD_EXPOSURE IS '360-degree risk exposure view aggregating accounts, transaction volumes, and fraud signals';

-- 4. VIEW: VW_UNASSIGNED_ALERTS
-- Real-time triage queue showing pending alerts awaiting formal investigation.
CREATE OR REPLACE VIEW VW_UNASSIGNED_ALERTS AS
SELECT 
    fa.alert_id,
    fa.transaction_id,
    t.amount,
    t.channel,
    fa.alert_type,
    fa.severity,
    fa.rule_triggered,
    fa.alert_date,
    fa.status AS alert_status
FROM FRAUD_ALERT fa
JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id
WHERE fa.alert_id NOT IN (SELECT alert_id FROM INVESTIGATION)
  AND fa.status NOT IN ('DISMISSED', 'RESOLVED');

COMMENT ON TABLE VW_UNASSIGNED_ALERTS IS 'Active triage queue of anomalous signals requiring investigator allocation';

-- ============================================================================
-- VERIFICATION QUERIES ON CREATED VIEWS
-- ============================================================================
PROMPT === Testing VW_HIGH_RISK_TRANSACTIONS ===
SELECT transaction_id, customer_name, amount, alert_severity, tx_status 
FROM VW_HIGH_RISK_TRANSACTIONS
FETCH FIRST 5 ROWS ONLY;

PROMPT === Testing VW_INVESTIGATION_SUMMARY ===
SELECT investigation_id, investigation_status, lead_investigator, outcome, duration_days 
FROM VW_INVESTIGATION_SUMMARY;

PROMPT === Testing VW_CUSTOMER_FRAUD_EXPOSURE ===
SELECT customer_id, customer_name, risk_score, flagged_tx_count, alerts_incurred 
FROM VW_CUSTOMER_FRAUD_EXPOSURE
WHERE alerts_incurred > 0
ORDER BY risk_score DESC;

PROMPT === Testing VW_UNASSIGNED_ALERTS ===
SELECT alert_id, transaction_id, amount, alert_type, severity 
FROM VW_UNASSIGNED_ALERTS;
