-- ============================================================================
-- PROJECT: FraudLens - Financial Transaction & Fraud Investigation Management System
-- SCRIPT:  04_review1_queries.sql
-- PURPOSE: Fulfills All Review 1 Query Requirements:
--          1. Single-row functions (String, Numeric, Date, Null-handling)
--          2. SQL operators & filtering (WHERE, AND/OR/NOT, IN, LIKE, BETWEEN, NULL)
--          3. Group functions (COUNT, SUM, AVG, MIN, MAX) with GROUP BY & HAVING
--          4. Multi-table relational joins & operational reporting
-- DIALECT: Oracle Database 11g/12c/19c/21c/23c Compatible
-- ============================================================================

SET LINESIZE 200;
SET PAGESIZE 100;

-- ============================================================================
-- 1. SINGLE-ROW FUNCTIONS DEMONSTRATION
-- ============================================================================

-- 1.1 Character/String Functions: UPPER, LOWER, INITCAP, LENGTH, SUBSTR, CONCAT
-- Formats customer full names and calculates string properties.
SELECT 
    customer_id,
    UPPER(first_name || ' ' || last_name) AS full_name_uppercase,
    LOWER(email) AS standardized_email,
    INITCAP(first_name) AS formal_first_name,
    LENGTH(phone) AS phone_number_length,
    SUBSTR(phone, 1, 3) AS country_code_prefix
FROM CUSTOMER
ORDER BY customer_id;

-- 1.2 Numeric Functions: ROUND, TRUNC, MOD, ABS
-- Financial calculation showing formatted transaction amounts and currency splits.
SELECT 
    transaction_id,
    amount,
    ROUND(amount, 0) AS rounded_amount,
    TRUNC(amount, -3) AS amount_truncated_thousands,
    MOD(transaction_id, 2) AS parity_flag
FROM TRANSACTIONS
WHERE amount > 50000
ORDER BY amount DESC;

-- 1.3 Date & Timestamp Functions: TO_CHAR, MONTHS_BETWEEN, SYSDATE
-- Demonstrates date formatting and calculation of account age in months.
SELECT 
    account_number,
    account_type,
    TO_CHAR(created_at, 'DD-Mon-YYYY') AS opening_date,
    TO_CHAR(created_at, 'Day') AS day_opened,
    ROUND(MONTHS_BETWEEN(SYSDATE, created_at), 1) AS account_age_months
FROM ACCOUNT
ORDER BY created_at ASC;

-- 1.4 General / Null-Handling Functions: NVL, COALESCE, NVL2
-- Demonstrates safe handling of optional counterparty accounts and end dates.
SELECT 
    transaction_id,
    account_id,
    amount,
    NVL(counterparty_account, 'N/A (Self/Cash Draw)') AS counterparty_display,
    COALESCE(counterparty_account, channel, 'UNSPECIFIED') AS resolved_destination
FROM TRANSACTIONS
ORDER BY transaction_id;

SELECT 
    investigation_id,
    alert_id,
    status,
    NVL2(end_date, TO_CHAR(end_date, 'YYYY-MM-DD'), 'Active Investigation') AS resolution_status
FROM INVESTIGATION
ORDER BY investigation_id;

-- ============================================================================
-- 2. SQL OPERATORS & ADVANCED FILTERING
-- ============================================================================

-- 2.1 Comparison Operators (=, !=, >, <) and Logical Operators (AND, OR, NOT)
-- Finds high-risk or verified customers with elevated risk score.
SELECT 
    customer_id,
    first_name || ' ' || last_name AS customer_name,
    kyc_status,
    risk_score
FROM CUSTOMER
WHERE (kyc_status = 'VERIFIED' AND risk_score >= 50)
   OR (kyc_status != 'VERIFIED' AND risk_score > 30)
ORDER BY risk_score DESC;

-- 2.2 IN and NOT IN Operator: Filtering across discrete categorical channels & statuses
SELECT 
    transaction_id,
    account_id,
    amount,
    channel,
    status
FROM TRANSACTIONS
WHERE channel IN ('NET_BANKING', 'MOBILE_APP')
  AND status NOT IN ('FAILED')
ORDER BY amount DESC;

-- 2.3 BETWEEN Operator: Finding transactions within a financial bracket
SELECT 
    transaction_id,
    account_id,
    amount,
    transaction_type,
    channel
FROM TRANSACTIONS
WHERE amount BETWEEN 50000 AND 200000
ORDER BY amount ASC;

-- 2.4 LIKE Operator: Pattern matching on accounts, emails, and rules
-- Finds corporate or apex business accounts and rules citing thresholds.
SELECT 
    customer_id,
    email,
    first_name || ' ' || last_name AS name
FROM CUSTOMER
WHERE email LIKE '%@%.in' OR email LIKE '%@corp%.com'
ORDER BY customer_id;

SELECT 
    alert_id,
    alert_type,
    rule_triggered
FROM FRAUD_ALERT
WHERE rule_triggered LIKE '%50,000%'
ORDER BY alert_id;

-- 2.5 IS NULL and IS NOT NULL: Locating open investigations without closure dates
SELECT 
    investigation_id,
    investigator_id,
    status,
    notes
FROM INVESTIGATION
WHERE end_date IS NULL
  AND status != 'CLOSED';

-- ============================================================================
-- 3. GROUP FUNCTIONS, GROUP BY & HAVING
-- ============================================================================

-- 3.1 Basic Aggregate Metrics across the entire transaction ledger
SELECT 
    COUNT(*) AS total_tx_count,
    SUM(amount) AS total_volume_inr,
    ROUND(AVG(amount), 2) AS average_tx_amount,
    MIN(amount) AS lowest_tx_amount,
    MAX(amount) AS highest_tx_amount
FROM TRANSACTIONS;

-- 3.2 GROUP BY: Transaction volume, count, and averages grouped by Channel
SELECT 
    channel,
    COUNT(*) AS total_transactions,
    SUM(amount) AS total_amount,
    ROUND(AVG(amount), 2) AS avg_amount,
    MAX(amount) AS peak_amount
FROM TRANSACTIONS
GROUP BY channel
ORDER BY total_amount DESC;

-- 3.3 GROUP BY: Fraud alerts grouped by severity and alert type
SELECT 
    severity,
    alert_type,
    COUNT(*) AS alert_count
FROM FRAUD_ALERT
GROUP BY severity, alert_type
ORDER BY severity DESC, alert_count DESC;

-- 3.4 GROUP BY with HAVING: Accounts with total transaction volume > 100,000 INR
SELECT 
    account_id,
    COUNT(transaction_id) AS transactions_conducted,
    SUM(amount) AS cumulative_volume
FROM TRANSACTIONS
GROUP BY account_id
HAVING SUM(amount) > 100000
ORDER BY cumulative_volume DESC;

-- 3.5 GROUP BY with HAVING: High-velocity channels having at least 3 transactions
SELECT 
    channel,
    COUNT(transaction_id) AS tx_count,
    ROUND(AVG(amount), 2) AS avg_ticket_size
FROM TRANSACTIONS
GROUP BY channel
HAVING COUNT(transaction_id) >= 3
ORDER BY tx_count DESC;

-- ============================================================================
-- 4. REVIEW 1 RELATIONAL JOINS
-- ============================================================================

-- 4.1 2-Table Join: Customer linked to their Accounts
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS customer_name,
    c.kyc_status,
    a.account_number,
    a.account_type,
    a.balance,
    a.status AS account_status
FROM CUSTOMER c
JOIN ACCOUNT a ON c.customer_id = a.customer_id
ORDER BY c.customer_id, a.account_number;

-- 4.2 3-Table Join: Customer -> Account -> Transactions
SELECT 
    c.first_name || ' ' || c.last_name AS customer_name,
    a.account_number,
    t.transaction_id,
    t.transaction_type,
    t.amount,
    t.channel,
    t.status AS tx_status
FROM CUSTOMER c
JOIN ACCOUNT a ON c.customer_id = a.customer_id
JOIN TRANSACTIONS t ON a.account_id = t.account_id
WHERE t.amount > 50000
ORDER BY t.amount DESC;

-- 4.3 Join: Fraud Alert linked with Transaction & Account
SELECT 
    fa.alert_id,
    fa.alert_type,
    fa.severity,
    t.transaction_id,
    t.amount,
    t.channel,
    a.account_number,
    fa.status AS alert_status
FROM FRAUD_ALERT fa
JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id
JOIN ACCOUNT a ON t.account_id = a.account_id
ORDER BY fa.alert_id;
