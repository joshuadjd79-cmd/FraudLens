-- ============================================================================
-- PROJECT: FraudLens - Financial Transaction & Fraud Investigation Management System
-- SCRIPT:  05_review2_subqueries_joins.sql
-- PURPOSE: Fulfills Review 2 Subqueries & Advanced Joins Requirements:
--          1. Single-row subqueries (scalar comparisons)
--          2. Multi-row subqueries (IN, ANY, ALL)
--          3. Correlated subqueries (EXISTS, NOT EXISTS, comparative aggregates)
--          4. Comprehensive multi-table INNER and LEFT OUTER joins
--          5. End-to-End Master Fraud Investigation Dossier Report
-- DIALECT: Oracle Database 11g/12c/19c/21c/23c Compatible
-- ============================================================================

SET LINESIZE 250;
SET PAGESIZE 100;

-- ============================================================================
-- 1. SUBQUERIES DEMONSTRATIONS
-- ============================================================================

-- 1.1 Single-Row Subquery: Identify transactions strictly greater than the overall system average
-- Demonstrates scalar subquery comparison in the WHERE clause.
SELECT 
    t.transaction_id,
    t.account_id,
    t.amount,
    t.channel,
    t.status,
    ROUND((SELECT AVG(amount) FROM TRANSACTIONS), 2) AS system_avg_amount,
    ROUND(t.amount - (SELECT AVG(amount) FROM TRANSACTIONS), 2) AS variance_from_avg
FROM TRANSACTIONS t
WHERE t.amount > (SELECT AVG(amount) FROM TRANSACTIONS)
ORDER BY t.amount DESC;

-- 1.2 Single-Row Subquery: Customer who owns the single largest account balance
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    a.account_number,
    a.balance
FROM CUSTOMER c
JOIN ACCOUNT a ON c.customer_id = a.customer_id
WHERE a.balance = (SELECT MAX(balance) FROM ACCOUNT);

-- 1.3 Multi-Row Subquery with IN: Customers associated with at least one FLAGGED transaction
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    c.risk_score
FROM CUSTOMER c
WHERE c.customer_id IN (
    SELECT a.customer_id 
    FROM ACCOUNT a 
    WHERE a.account_id IN (
        SELECT t.account_id 
        FROM TRANSACTIONS t 
        WHERE t.status = 'FLAGGED'
    )
)
ORDER BY c.risk_score DESC;

-- 1.4 Multi-Row Subquery with > ALL: High-value transactions exceeding ALL deposits in the system
-- Demonstrates multi-row ALL operator.
SELECT 
    transaction_id,
    account_id,
    transaction_type,
    amount,
    channel
FROM TRANSACTIONS
WHERE amount > ALL (
    SELECT amount 
    FROM TRANSACTIONS 
    WHERE transaction_type = 'DEPOSIT'
)
ORDER BY amount DESC;

-- 1.5 Multi-Row Subquery with > ANY: Transactions larger than AT LEAST ONE transfer amount
SELECT 
    transaction_id,
    account_id,
    transaction_type,
    amount
FROM TRANSACTIONS
WHERE amount > ANY (
    SELECT amount 
    FROM TRANSACTIONS 
    WHERE transaction_type = 'TRANSFER'
)
ORDER BY amount ASC;

-- 1.6 Correlated Subquery: Find accounts where cumulative transaction total exceeds account balance
-- The subquery correlates with the outer ACCOUNT row via `a.account_id`.
SELECT 
    a.account_id,
    a.account_number,
    a.balance,
    (SELECT SUM(t.amount) 
     FROM TRANSACTIONS t 
     WHERE t.account_id = a.account_id) AS total_transacted
FROM ACCOUNT a
WHERE (SELECT SUM(t.amount) 
       FROM TRANSACTIONS t 
       WHERE t.account_id = a.account_id) > a.balance
ORDER BY total_transacted DESC;

-- 1.7 Correlated Subquery with EXISTS: Accounts that have generated CRITICAL fraud alerts
SELECT 
    a.account_id,
    a.account_number,
    a.account_type,
    a.status
FROM ACCOUNT a
WHERE EXISTS (
    SELECT 1 
    FROM TRANSACTIONS t
    JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id
    WHERE t.account_id = a.account_id
      AND fa.severity = 'CRITICAL'
);

-- 1.8 Correlated Subquery with NOT EXISTS: Investigators currently NOT assigned to any case
SELECT 
    i.investigator_id,
    i.first_name || ' ' || i.last_name AS investigator_name,
    i.department,
    i.experience_years
FROM INVESTIGATOR i
WHERE NOT EXISTS (
    SELECT 1 
    FROM INVESTIGATION inv 
    WHERE inv.investigator_id = i.investigator_id
);

-- ============================================================================
-- 2. ADVANCED JOINS DEMONSTRATIONS
-- ============================================================================

-- 2.1 LEFT OUTER JOIN: All Investigators and their assigned investigations
-- Shows unassigned investigators with NULL values on the right side.
SELECT 
    i.investigator_id,
    i.first_name || ' ' || i.last_name AS investigator_name,
    i.department,
    inv.investigation_id,
    inv.status AS case_status,
    inv.outcome
FROM INVESTIGATOR i
LEFT JOIN INVESTIGATION inv ON i.investigator_id = inv.investigator_id
ORDER BY i.investigator_id, inv.investigation_id;

-- 2.2 LEFT OUTER JOIN: All Fraud Alerts and their corresponding investigation details
-- Highlights alerts that are still unassigned or dismissed without investigation.
SELECT 
    fa.alert_id,
    fa.alert_type,
    fa.severity,
    fa.status AS alert_status,
    inv.investigation_id,
    NVL(inv.status, 'NO_INVESTIGATION_OPENED') AS investigation_progress
FROM FRAUD_ALERT fa
LEFT JOIN INVESTIGATION inv ON fa.alert_id = inv.alert_id
ORDER BY fa.alert_id;

-- 2.3 Comprehensive 6-Table Relational Join: Full Fraud Investigation Dossier
-- Links: CUSTOMER -> ACCOUNT -> TRANSACTIONS -> FRAUD_ALERT -> INVESTIGATION -> INVESTIGATOR
SELECT 
    inv.investigation_id AS case_ref,
    inv.status AS case_status,
    inv.outcome AS final_outcome,
    fa.alert_id,
    fa.alert_type,
    fa.severity AS risk_level,
    t.transaction_id AS tx_id,
    t.amount AS amount_inr,
    t.channel,
    t.transaction_date,
    a.account_number,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.kyc_status,
    c.risk_score,
    i.first_name || ' ' || i.last_name AS assigned_lead,
    i.department AS lead_dept
FROM INVESTIGATION inv
JOIN FRAUD_ALERT fa       ON inv.alert_id = fa.alert_id
JOIN TRANSACTIONS t       ON fa.transaction_id = t.transaction_id
JOIN ACCOUNT a            ON t.account_id = a.account_id
JOIN CUSTOMER c           ON a.customer_id = c.customer_id
LEFT JOIN INVESTIGATOR i  ON inv.investigator_id = i.investigator_id
ORDER BY inv.investigation_id;
