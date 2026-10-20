-- ============================================================================
-- PROJECT: FraudLens - Financial Transaction & Fraud Investigation Management System
-- SCRIPT:  03_sample_data.sql
-- PURPOSE: Populates rich, consistent, domain-realistic sample dataset.
--          All 6 core entities populated in strict referential dependency order.
-- DIALECT: Oracle Database 11g/12c/19c/21c/23c Compatible
-- ============================================================================

-- Clean out existing rows in reverse dependency order
DELETE FROM INVESTIGATION;
DELETE FROM INVESTIGATOR;
DELETE FROM FRAUD_ALERT;
DELETE FROM TRANSACTIONS;
DELETE FROM ACCOUNT;
DELETE FROM CUSTOMER;
DELETE FROM INVESTIGATION_AUDIT;
DELETE FROM ALERT_AUDIT;
COMMIT;

-- ============================================================================
-- 1. INSERT CUSTOMERS (10 Diverse Profiles)
-- ============================================================================
INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score, created_at)
VALUES (1001, 'Aarav', 'Sharma', 'aarav.sharma@finmail.in', '+919876543210', 'VERIFIED', 15, TO_DATE('2023-01-15', 'YYYY-MM-DD'));

INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score, created_at)
VALUES (1002, 'Priya', 'Nair', 'priya.nair@corpmail.com', '+919876543211', 'VERIFIED', 20, TO_DATE('2023-02-10', 'YYYY-MM-DD'));

INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score, created_at)
VALUES (1003, 'Rohan', 'Verma', 'rohan.verma@quickpay.in', '+919876543212', 'VERIFIED', 78, TO_DATE('2023-03-05', 'YYYY-MM-DD'));

INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score, created_at)
VALUES (1004, 'Ananya', 'Deshmukh', 'ananya.d@globalbiz.com', '+919876543213', 'VERIFIED', 10, TO_DATE('2023-04-18', 'YYYY-MM-DD'));

INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score, created_at)
VALUES (1005, 'Vikram', 'Singhania', 'vikram.s@apexholdings.in', '+919876543214', 'VERIFIED', 85, TO_DATE('2023-05-22', 'YYYY-MM-DD'));

INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score, created_at)
VALUES (1006, 'Sneha', 'Patel', 'sneha.patel@webmail.in', '+919876543215', 'PENDING', 45, TO_DATE('2023-06-30', 'YYYY-MM-DD'));

INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score, created_at)
VALUES (1007, 'Karan', 'Mehta', 'karan.mehta@freelance.org', '+919876543216', 'VERIFIED', 62, TO_DATE('2023-07-12', 'YYYY-MM-DD'));

INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score, created_at)
VALUES (1008, 'Divya', 'Iyer', 'divya.iyer@technowave.com', '+919876543217', 'VERIFIED', 8, TO_DATE('2023-08-04', 'YYYY-MM-DD'));

INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score, created_at)
VALUES (1009, 'Sameer', 'Khan', 'sameer.k@shadownet.me', '+919876543218', 'REJECTED', 95, TO_DATE('2023-09-19', 'YYYY-MM-DD'));

INSERT INTO CUSTOMER (customer_id, first_name, last_name, email, phone, kyc_status, risk_score, created_at)
VALUES (1010, 'Meera', 'Reddy', 'meera.reddy@apexcloud.in', '+919876543219', 'VERIFIED', 25, TO_DATE('2023-10-01', 'YYYY-MM-DD'));

-- ============================================================================
-- 2. INSERT ACCOUNTS (12 Accounts linked to Customers)
-- ============================================================================
INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2001, 1001, 'SB-1001-01', 'SAVINGS', 85400.00, 'INR', 'ACTIVE', TO_DATE('2023-01-16', 'YYYY-MM-DD'));

INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2002, 1002, 'CA-1002-01', 'CURRENT', 420000.00, 'INR', 'ACTIVE', TO_DATE('2023-02-12', 'YYYY-MM-DD'));

INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2003, 1003, 'SB-1003-01', 'SAVINGS', 14500.00, 'INR', 'ACTIVE', TO_DATE('2023-03-08', 'YYYY-MM-DD'));

INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2004, 1003, 'CA-1003-02', 'CURRENT', 189000.00, 'INR', 'ACTIVE', TO_DATE('2023-03-15', 'YYYY-MM-DD'));

INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2005, 1004, 'SL-1004-01', 'SALARY', 125000.00, 'INR', 'ACTIVE', TO_DATE('2023-04-20', 'YYYY-MM-DD'));

INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2006, 1005, 'CA-1005-01', 'CURRENT', 980000.00, 'INR', 'FROZEN', TO_DATE('2023-05-25', 'YYYY-MM-DD'));

INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2007, 1006, 'SB-1006-01', 'SAVINGS', 3200.00, 'INR', 'DORMANT', TO_DATE('2023-07-02', 'YYYY-MM-DD'));

INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2008, 1007, 'SB-1007-01', 'SAVINGS', 74000.00, 'INR', 'ACTIVE', TO_DATE('2023-07-15', 'YYYY-MM-DD'));

INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2009, 1008, 'SL-1008-01', 'SALARY', 215000.00, 'INR', 'ACTIVE', TO_DATE('2023-08-06', 'YYYY-MM-DD'));

INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2010, 1009, 'SB-1009-01', 'SAVINGS', 500.00, 'INR', 'FROZEN', TO_DATE('2023-09-20', 'YYYY-MM-DD'));

INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2011, 1010, 'SB-1010-01', 'SAVINGS', 62000.00, 'INR', 'ACTIVE', TO_DATE('2023-10-05', 'YYYY-MM-DD'));

INSERT INTO ACCOUNT (account_id, customer_id, account_number, account_type, balance, currency, status, created_at)
VALUES (2012, 1005, 'NRI-1005-02', 'NRI', 1540000.00, 'INR', 'ACTIVE', TO_DATE('2023-10-10', 'YYYY-MM-DD'));

-- ============================================================================
-- 3. INSERT TRANSACTIONS (18 Realistic Movements: Standard + High-Risk Anomaly)
-- Illustrative threshold rule: Amount > 50,000 INR
-- ============================================================================
-- Normal retail & salary
INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50001, 2001, 'DEPOSIT', 15000.00, TO_TIMESTAMP('2024-01-05 10:15:00', 'YYYY-MM-DD HH24:MI:SS'), 'UPI', 'COMPLETED', 'EXTERNAL-UPI-01', 'Monthly client consultation fee');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50002, 2001, 'PAYMENT', 2450.00, TO_TIMESTAMP('2024-01-08 18:30:00', 'YYYY-MM-DD HH24:MI:SS'), 'POS', 'COMPLETED', 'MERCHANT-RETAIL-44', 'Grocery supermarket purchase');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50003, 2005, 'DEPOSIT', 125000.00, TO_TIMESTAMP('2024-01-31 09:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'NET_BANKING', 'COMPLETED', 'CORP-PAYROLL-99', 'January Corporate Salary Credit');

-- High value & suspicious (Threshold > 50,000)
INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50004, 2004, 'TRANSFER', 85000.00, TO_TIMESTAMP('2024-02-01 02:14:00', 'YYYY-MM-DD HH24:MI:SS'), 'NET_BANKING', 'FLAGGED', 'BENEFICIARY-EXT-889', 'Unscheduled nocturnal wire transfer');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50005, 2004, 'TRANSFER', 95000.00, TO_TIMESTAMP('2024-02-01 02:18:00', 'YYYY-MM-DD HH24:MI:SS'), 'NET_BANKING', 'FLAGGED', 'BENEFICIARY-EXT-889', 'Rapid velocity burst transfer to same counterparty');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50006, 2006, 'WITHDRAWAL', 250000.00, TO_TIMESTAMP('2024-02-03 14:20:00', 'YYYY-MM-DD HH24:MI:SS'), 'ATM', 'FLAGGED', NULL, 'High value ATM multi-draw exceeds daily tier');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50007, 2006, 'TRANSFER', 650000.00, TO_TIMESTAMP('2024-02-04 11:45:00', 'YYYY-MM-DD HH24:MI:SS'), 'NET_BANKING', 'FLAGGED', 'OFFSHORE-ESCROW-002', 'High-volume international remittance');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50008, 2002, 'TRANSFER', 180000.00, TO_TIMESTAMP('2024-02-10 16:10:00', 'YYYY-MM-DD HH24:MI:SS'), 'NET_BANKING', 'COMPLETED', 'VENDOR-RAW-MATERIALS', 'Vendor invoice settlement');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50009, 2003, 'WITHDRAWAL', 10000.00, TO_TIMESTAMP('2024-02-11 12:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'ATM', 'COMPLETED', NULL, 'Branch ATM cash withdrawal');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50010, 2008, 'TRANSFER', 58000.00, TO_TIMESTAMP('2024-02-14 23:50:00', 'YYYY-MM-DD HH24:MI:SS'), 'MOBILE_APP', 'FLAGGED', 'UNKNOWN-PEER-77', 'Late night high value peer transfer');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50011, 2010, 'DEPOSIT', 49500.00, TO_TIMESTAMP('2024-02-16 08:30:00', 'YYYY-MM-DD HH24:MI:SS'), 'UPI', 'FLAGGED', 'SUSPECT-MULE-01', 'Structuring near 50k threshold deposit');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50012, 2010, 'TRANSFER', 49000.00, TO_TIMESTAMP('2024-02-16 08:45:00', 'YYYY-MM-DD HH24:MI:SS'), 'UPI', 'FLAGGED', 'SUSPECT-MULE-02', 'Immediate layering transfer following deposit');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50013, 2009, 'PAYMENT', 3500.00, TO_TIMESTAMP('2024-02-18 19:10:00', 'YYYY-MM-DD HH24:MI:SS'), 'POS', 'COMPLETED', 'AIRLINE-TICKETING', 'Flight ticket booking');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50014, 2011, 'TRANSFER', 15000.00, TO_TIMESTAMP('2024-02-20 13:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'UPI', 'COMPLETED', 'FAMILY-TRANSFER-11', 'Inter-family assistance');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50015, 2012, 'DEPOSIT', 500000.00, TO_TIMESTAMP('2024-02-22 15:30:00', 'YYYY-MM-DD HH24:MI:SS'), 'NET_BANKING', 'COMPLETED', 'OVERSEAS-PARENT-CORP', 'Foreign portfolio remittance');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50016, 2007, 'WITHDRAWAL', 2000.00, TO_TIMESTAMP('2024-02-25 11:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'ATM', 'COMPLETED', NULL, 'Dormant account reactivation test withdrawal');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50017, 2004, 'TRANSFER', 110000.00, TO_TIMESTAMP('2024-02-26 03:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'NET_BANKING', 'FLAGGED', 'CRYPTO-EXCHANGE-IN', 'Off-hours high value virtual asset offramp');

INSERT INTO TRANSACTIONS (transaction_id, account_id, transaction_type, amount, transaction_date, channel, status, counterparty_account, description)
VALUES (50018, 2002, 'PAYMENT', 75000.00, TO_TIMESTAMP('2024-02-28 14:00:00', 'YYYY-MM-DD HH24:MI:SS'), 'NET_BANKING', 'COMPLETED', 'TAX-AUTHORITY-GST', 'Quarterly GST statutory tax filing');

-- ============================================================================
-- 4. INSERT FRAUD_ALERT (7 Strategic Alerts)
-- Rule: Alert is a signal for investigation, not proof of fraud.
-- ============================================================================
INSERT INTO FRAUD_ALERT (alert_id, transaction_id, alert_type, severity, rule_triggered, alert_date, status)
VALUES (7001, 50004, 'UNUSUAL_HOURS', 'HIGH', 'Rule 101: Net-banking transaction > 50,000 INR between 01:00-05:00', TO_TIMESTAMP('2024-02-01 02:14:05', 'YYYY-MM-DD HH24:MI:SS'), 'ESCALATED');

INSERT INTO FRAUD_ALERT (alert_id, transaction_id, alert_type, severity, rule_triggered, alert_date, status)
VALUES (7002, 50005, 'RAPID_VELOCITY', 'CRITICAL', 'Rule 104: Consecutive transfers > 50,000 INR to same counterparty within 5 mins', TO_TIMESTAMP('2024-02-01 02:18:05', 'YYYY-MM-DD HH24:MI:SS'), 'ESCALATED');

INSERT INTO FRAUD_ALERT (alert_id, transaction_id, alert_type, severity, rule_triggered, alert_date, status)
VALUES (7003, 50006, 'HIGH_AMOUNT', 'HIGH', 'Rule 102: ATM withdrawal cumulative amount > 100,000 INR threshold', TO_TIMESTAMP('2024-02-03 14:20:10', 'YYYY-MM-DD HH24:MI:SS'), 'RESOLVED');

INSERT INTO FRAUD_ALERT (alert_id, transaction_id, alert_type, severity, rule_triggered, alert_date, status)
VALUES (7004, 50007, 'CROSS_BORDER', 'CRITICAL', 'Rule 108: Offshore escrow transfer > 500,000 INR on flagged account', TO_TIMESTAMP('2024-02-04 11:45:15', 'YYYY-MM-DD HH24:MI:SS'), 'ESCALATED');

INSERT INTO FRAUD_ALERT (alert_id, transaction_id, alert_type, severity, rule_triggered, alert_date, status)
VALUES (7005, 50010, 'HIGH_AMOUNT', 'MEDIUM', 'Rule 101: Mobile App transfer > 50,000 INR illustrative rule', TO_TIMESTAMP('2024-02-14 23:50:08', 'YYYY-MM-DD HH24:MI:SS'), 'PENDING');

INSERT INTO FRAUD_ALERT (alert_id, transaction_id, alert_type, severity, rule_triggered, alert_date, status)
VALUES (7006, 50011, 'STRUCTURING', 'HIGH', 'Rule 106: Structuring near 50k threshold under KYC-rejected account', TO_TIMESTAMP('2024-02-16 08:30:12', 'YYYY-MM-DD HH24:MI:SS'), 'ESCALATED');

INSERT INTO FRAUD_ALERT (alert_id, transaction_id, alert_type, severity, rule_triggered, alert_date, status)
VALUES (7007, 50017, 'SUSPICIOUS_CHANNEL', 'HIGH', 'Rule 109: High-risk counterparty crypto-gateway connection', TO_TIMESTAMP('2024-02-26 03:00:10', 'YYYY-MM-DD HH24:MI:SS'), 'DISMISSED');

-- ============================================================================
-- 5. INSERT INVESTIGATOR (4 Specialist Officers)
-- ============================================================================
INSERT INTO INVESTIGATOR (investigator_id, first_name, last_name, email, department, experience_years, active_status)
VALUES (301, 'Rajesh', 'Sen', 'rajesh.sen@fraudlens-aml.org', 'Anti-Money Laundering', 9, 'ACTIVE');

INSERT INTO INVESTIGATOR (investigator_id, first_name, last_name, email, department, experience_years, active_status)
VALUES (302, 'Kavita', 'Mishra', 'kavita.m@fraudlens-aml.org', 'Cyber Intelligence', 6, 'ACTIVE');

INSERT INTO INVESTIGATOR (investigator_id, first_name, last_name, email, department, experience_years, active_status)
VALUES (303, 'Suresh', 'Bose', 'suresh.bose@fraudlens-ops.org', 'Risk Operations', 4, 'ACTIVE');

INSERT INTO INVESTIGATOR (investigator_id, first_name, last_name, email, department, experience_years, active_status)
VALUES (304, 'Farhan', 'Qureshi', 'farhan.q@fraudlens-aml.org', 'Financial Crimes', 11, 'INACTIVE');

-- ============================================================================
-- 6. INSERT INVESTIGATION (Formal cases linking Alert to Investigator)
-- Status progression: OPEN -> UNDER REVIEW -> CLOSED
-- ============================================================================
INSERT INTO INVESTIGATION (investigation_id, alert_id, investigator_id, start_date, end_date, status, outcome, notes)
VALUES (9001, 7001, 302, TO_DATE('2024-02-01', 'YYYY-MM-DD'), NULL, 'UNDER REVIEW', 'PENDING', 
        'IP geolocation indicates overseas proxy used during midnight transfer. Awaiting telecom ISP logs.');

INSERT INTO INVESTIGATION (investigation_id, alert_id, investigator_id, start_date, end_date, status, outcome, notes)
VALUES (9002, 7002, 301, TO_DATE('2024-02-01', 'YYYY-MM-DD'), TO_DATE('2024-02-05', 'YYYY-MM-DD'), 'CLOSED', 'CONFIRMED_FRAUD', 
        'Corroborated account takeover. Mule counterparty frozen by law enforcement agency.');

INSERT INTO INVESTIGATION (investigation_id, alert_id, investigator_id, start_date, end_date, status, outcome, notes)
VALUES (9003, 7003, 303, TO_DATE('2024-02-03', 'YYYY-MM-DD'), TO_DATE('2024-02-04', 'YYYY-MM-DD'), 'CLOSED', 'FALSE_POSITIVE', 
        'Customer confirmed legitimate cash requirement for property registration. High wealth tier verified.');

INSERT INTO INVESTIGATION (investigation_id, alert_id, investigator_id, start_date, end_date, status, outcome, notes)
VALUES (9004, 7004, 301, TO_DATE('2024-02-04', 'YYYY-MM-DD'), NULL, 'OPEN', 'PENDING', 
        'Offshore shell corporation escrow alert. Requested AML compliance documentation from correspondent bank.');

INSERT INTO INVESTIGATION (investigation_id, alert_id, investigator_id, start_date, end_date, status, outcome, notes)
VALUES (9005, 7006, 302, TO_DATE('2024-02-16', 'YYYY-MM-DD'), NULL, 'UNDER REVIEW', 'PENDING', 
        'Smurfing pattern detected across UPI channels. Linked multiple dummy accounts to same device hardware ID.');

-- Note: Alert 7005 remains in PENDING status without an investigation yet (unassigned alert test case)
-- Note: Alert 7007 was dismissed directly before opening an investigation

COMMIT;

-- Verification: Display row counts across all tables
SELECT 'CUSTOMER' AS entity, COUNT(*) AS total_rows FROM CUSTOMER
UNION ALL SELECT 'ACCOUNT', COUNT(*) FROM ACCOUNT
UNION ALL SELECT 'TRANSACTIONS', COUNT(*) FROM TRANSACTIONS
UNION ALL SELECT 'FRAUD_ALERT', COUNT(*) FROM FRAUD_ALERT
UNION ALL SELECT 'INVESTIGATOR', COUNT(*) FROM INVESTIGATOR
UNION ALL SELECT 'INVESTIGATION', COUNT(*) FROM INVESTIGATION;
