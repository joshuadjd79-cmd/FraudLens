"""
FraudLens: In-Memory Baseline Demo Dataset
Provides exact mirror of the 56 baseline operational records in 03_sample_data.sql.
Used for offline testing, UI dev, and fallback if Oracle is disconnected.
"""

from datetime import datetime

CUSTOMERS = [
    {"customer_id": 1001, "first_name": "Aarav", "last_name": "Sharma", "email": "aarav.sharma@finmail.in", "phone": "+919876543210", "kyc_status": "VERIFIED", "risk_score": 15, "created_at": "2023-01-15"},
    {"customer_id": 1002, "first_name": "Priya", "last_name": "Nair", "email": "priya.nair@corpmail.com", "phone": "+919876543211", "kyc_status": "VERIFIED", "risk_score": 20, "created_at": "2023-02-10"},
    {"customer_id": 1003, "first_name": "Rohan", "last_name": "Verma", "email": "rohan.verma@quickpay.in", "phone": "+919876543212", "kyc_status": "VERIFIED", "risk_score": 78, "created_at": "2023-03-05"},
    {"customer_id": 1004, "first_name": "Ananya", "last_name": "Deshmukh", "email": "ananya.d@globalbiz.com", "phone": "+919876543213", "kyc_status": "VERIFIED", "risk_score": 10, "created_at": "2023-04-18"},
    {"customer_id": 1005, "first_name": "Vikram", "last_name": "Singhania", "email": "vikram.s@apexholdings.in", "phone": "+919876543214", "kyc_status": "VERIFIED", "risk_score": 85, "created_at": "2023-05-22"},
    {"customer_id": 1006, "first_name": "Sneha", "last_name": "Patel", "email": "sneha.patel@webmail.in", "phone": "+919876543215", "kyc_status": "PENDING", "risk_score": 45, "created_at": "2023-06-30"},
    {"customer_id": 1007, "first_name": "Karan", "last_name": "Mehta", "email": "karan.mehta@freelance.org", "phone": "+919876543216", "kyc_status": "VERIFIED", "risk_score": 62, "created_at": "2023-07-12"},
    {"customer_id": 1008, "first_name": "Divya", "last_name": "Iyer", "email": "divya.iyer@technowave.com", "phone": "+919876543217", "kyc_status": "VERIFIED", "risk_score": 8, "created_at": "2023-08-04"},
    {"customer_id": 1009, "first_name": "Sameer", "last_name": "Khan", "email": "sameer.k@shadownet.me", "phone": "+919876543218", "kyc_status": "REJECTED", "risk_score": 95, "created_at": "2023-09-19"},
    {"customer_id": 1010, "first_name": "Meera", "last_name": "Reddy", "email": "meera.reddy@apexcloud.in", "phone": "+919876543219", "kyc_status": "VERIFIED", "risk_score": 25, "created_at": "2023-10-01"},
]

ACCOUNTS = [
    {"account_id": 2001, "customer_id": 1001, "account_number": "SB-1001-01", "account_type": "SAVINGS", "balance": 85400.00, "currency": "INR", "status": "ACTIVE", "created_at": "2023-01-16"},
    {"account_id": 2002, "customer_id": 1002, "account_number": "CA-1002-01", "account_type": "CURRENT", "balance": 420000.00, "currency": "INR", "status": "ACTIVE", "created_at": "2023-02-12"},
    {"account_id": 2003, "customer_id": 1003, "account_number": "SB-1003-01", "account_type": "SAVINGS", "balance": 14500.00, "currency": "INR", "status": "ACTIVE", "created_at": "2023-03-08"},
    {"account_id": 2004, "customer_id": 1003, "account_number": "CA-1003-02", "account_type": "CURRENT", "balance": 189000.00, "currency": "INR", "status": "ACTIVE", "created_at": "2023-03-15"},
    {"account_id": 2005, "customer_id": 1004, "account_number": "SL-1004-01", "account_type": "SALARY", "balance": 125000.00, "currency": "INR", "status": "ACTIVE", "created_at": "2023-04-20"},
    {"account_id": 2006, "customer_id": 1005, "account_number": "CA-1005-01", "account_type": "CURRENT", "balance": 980000.00, "currency": "INR", "status": "FROZEN", "created_at": "2023-05-25"},
    {"account_id": 2007, "customer_id": 1006, "account_number": "SB-1006-01", "account_type": "SAVINGS", "balance": 3200.00, "currency": "INR", "status": "DORMANT", "created_at": "2023-07-02"},
    {"account_id": 2008, "customer_id": 1007, "account_number": "SB-1007-01", "account_type": "SAVINGS", "balance": 74000.00, "currency": "INR", "status": "ACTIVE", "created_at": "2023-07-15"},
    {"account_id": 2009, "customer_id": 1008, "account_number": "SL-1008-01", "account_type": "SALARY", "balance": 215000.00, "currency": "INR", "status": "ACTIVE", "created_at": "2023-08-06"},
    {"account_id": 2010, "customer_id": 1009, "account_number": "SB-1009-01", "account_type": "SAVINGS", "balance": 500.00, "currency": "INR", "status": "FROZEN", "created_at": "2023-09-20"},
    {"account_id": 2011, "customer_id": 1010, "account_number": "SB-1010-01", "account_type": "SAVINGS", "balance": 62000.00, "currency": "INR", "status": "ACTIVE", "created_at": "2023-10-05"},
    {"account_id": 2012, "customer_id": 1005, "account_number": "NRI-1005-02", "account_type": "NRI", "balance": 1540000.00, "currency": "INR", "status": "ACTIVE", "created_at": "2023-10-10"},
]

TRANSACTIONS = [
    {"transaction_id": 50001, "account_id": 2001, "transaction_type": "DEPOSIT", "amount": 15000.00, "transaction_date": "2024-01-05 10:15:00", "channel": "UPI", "status": "COMPLETED", "counterparty_account": "EXTERNAL-UPI-01", "description": "Monthly client consultation fee"},
    {"transaction_id": 50002, "account_id": 2001, "transaction_type": "PAYMENT", "amount": 2450.00, "transaction_date": "2024-01-08 18:30:00", "channel": "POS", "status": "COMPLETED", "counterparty_account": "MERCHANT-RETAIL-44", "description": "Grocery supermarket purchase"},
    {"transaction_id": 50003, "account_id": 2005, "transaction_type": "DEPOSIT", "amount": 125000.00, "transaction_date": "2024-01-31 09:00:00", "channel": "NET_BANKING", "status": "COMPLETED", "counterparty_account": "CORP-PAYROLL-99", "description": "January Corporate Salary Credit"},
    {"transaction_id": 50004, "account_id": 2004, "transaction_type": "TRANSFER", "amount": 85000.00, "transaction_date": "2024-02-01 02:14:00", "channel": "NET_BANKING", "status": "FLAGGED", "counterparty_account": "BENEFICIARY-EXT-889", "description": "Unscheduled nocturnal wire transfer"},
    {"transaction_id": 50005, "account_id": 2004, "transaction_type": "TRANSFER", "amount": 95000.00, "transaction_date": "2024-02-01 02:18:00", "channel": "NET_BANKING", "status": "FLAGGED", "counterparty_account": "BENEFICIARY-EXT-889", "description": "Rapid velocity burst transfer to same counterparty"},
    {"transaction_id": 50006, "account_id": 2006, "transaction_type": "WITHDRAWAL", "amount": 250000.00, "transaction_date": "2024-02-03 14:20:00", "channel": "ATM", "status": "FLAGGED", "counterparty_account": None, "description": "High value ATM multi-draw exceeds daily tier"},
    {"transaction_id": 50007, "account_id": 2006, "transaction_type": "TRANSFER", "amount": 650000.00, "transaction_date": "2024-02-04 11:45:00", "channel": "NET_BANKING", "status": "FLAGGED", "counterparty_account": "OFFSHORE-ESCROW-002", "description": "High-volume international remittance"},
    {"transaction_id": 50008, "account_id": 2002, "transaction_type": "TRANSFER", "amount": 180000.00, "transaction_date": "2024-02-10 16:10:00", "channel": "NET_BANKING", "status": "COMPLETED", "counterparty_account": "VENDOR-RAW-MATERIALS", "description": "Vendor invoice settlement"},
    {"transaction_id": 50009, "account_id": 2003, "transaction_type": "WITHDRAWAL", "amount": 10000.00, "transaction_date": "2024-02-11 12:00:00", "channel": "ATM", "status": "COMPLETED", "counterparty_account": None, "description": "Branch ATM cash withdrawal"},
    {"transaction_id": 50010, "account_id": 2008, "transaction_type": "TRANSFER", "amount": 58000.00, "transaction_date": "2024-02-14 23:50:00", "channel": "MOBILE_APP", "status": "FLAGGED", "counterparty_account": "UNKNOWN-PEER-77", "description": "Late night high value peer transfer"},
    {"transaction_id": 50011, "account_id": 2010, "transaction_type": "DEPOSIT", "amount": 49500.00, "transaction_date": "2024-02-16 08:30:00", "channel": "UPI", "status": "FLAGGED", "counterparty_account": "SUSPECT-MULE-01", "description": "Structuring near 50k threshold deposit"},
    {"transaction_id": 50012, "account_id": 2010, "transaction_type": "TRANSFER", "amount": 49000.00, "transaction_date": "2024-02-16 08:45:00", "channel": "UPI", "status": "FLAGGED", "counterparty_account": "SUSPECT-MULE-02", "description": "Immediate layering transfer following deposit"},
    {"transaction_id": 50013, "account_id": 2009, "transaction_type": "PAYMENT", "amount": 3500.00, "transaction_date": "2024-02-18 19:10:00", "channel": "POS", "status": "COMPLETED", "counterparty_account": "AIRLINE-TICKETING", "description": "Flight ticket booking"},
    {"transaction_id": 50014, "account_id": 2011, "transaction_type": "TRANSFER", "amount": 15000.00, "transaction_date": "2024-02-20 13:00:00", "channel": "UPI", "status": "COMPLETED", "counterparty_account": "FAMILY-TRANSFER-11", "description": "Inter-family assistance"},
    {"transaction_id": 50015, "account_id": 2012, "transaction_type": "DEPOSIT", "amount": 500000.00, "transaction_date": "2024-02-22 15:30:00", "channel": "NET_BANKING", "status": "COMPLETED", "counterparty_account": "OVERSEAS-PARENT-CORP", "description": "Foreign portfolio remittance"},
    {"transaction_id": 50016, "account_id": 2007, "transaction_type": "WITHDRAWAL", "amount": 2000.00, "transaction_date": "2024-02-25 11:00:00", "channel": "ATM", "status": "COMPLETED", "counterparty_account": None, "description": "Dormant account reactivation test withdrawal"},
    {"transaction_id": 50017, "account_id": 2004, "transaction_type": "TRANSFER", "amount": 110000.00, "transaction_date": "2024-02-26 03:00:00", "channel": "NET_BANKING", "status": "FLAGGED", "counterparty_account": "CRYPTO-EXCHANGE-IN", "description": "Off-hours high value virtual asset offramp"},
    {"transaction_id": 50018, "account_id": 2002, "transaction_type": "PAYMENT", "amount": 75000.00, "transaction_date": "2024-02-28 14:00:00", "channel": "NET_BANKING", "status": "COMPLETED", "counterparty_account": "TAX-AUTHORITY-GST", "description": "Quarterly GST statutory tax filing"},
]

FRAUD_ALERTS = [
    {"alert_id": 7001, "transaction_id": 50004, "alert_type": "UNUSUAL_HOURS", "severity": "HIGH", "rule_triggered": "Rule 101: Net-banking transaction > 50,000 INR between 01:00-05:00", "alert_date": "2024-02-01 02:14:05", "status": "ESCALATED"},
    {"alert_id": 7002, "transaction_id": 50005, "alert_type": "RAPID_VELOCITY", "severity": "CRITICAL", "rule_triggered": "Rule 104: Consecutive transfers > 50,000 INR to same counterparty within 5 mins", "alert_date": "2024-02-01 02:18:05", "status": "ESCALATED"},
    {"alert_id": 7003, "transaction_id": 50006, "alert_type": "HIGH_AMOUNT", "severity": "HIGH", "rule_triggered": "Rule 102: ATM withdrawal cumulative amount > 100,000 INR threshold", "alert_date": "2024-02-03 14:20:10", "status": "RESOLVED"},
    {"alert_id": 7004, "transaction_id": 50007, "alert_type": "CROSS_BORDER", "severity": "CRITICAL", "rule_triggered": "Rule 108: Offshore escrow transfer > 500,000 INR on flagged account", "alert_date": "2024-02-04 11:45:15", "status": "ESCALATED"},
    {"alert_id": 7005, "transaction_id": 50010, "alert_type": "HIGH_AMOUNT", "severity": "MEDIUM", "rule_triggered": "Rule 101: Mobile App transfer > 50,000 INR illustrative rule", "alert_date": "2024-02-14 23:50:08", "status": "PENDING"},
    {"alert_id": 7006, "transaction_id": 50011, "alert_type": "STRUCTURING", "severity": "HIGH", "rule_triggered": "Rule 106: Structuring near 50k threshold under KYC-rejected account", "alert_date": "2024-02-16 08:30:12", "status": "ESCALATED"},
    {"alert_id": 7007, "transaction_id": 50017, "alert_type": "SUSPICIOUS_CHANNEL", "severity": "HIGH", "rule_triggered": "Rule 109: High-risk counterparty crypto-gateway connection", "alert_date": "2024-02-26 03:00:10", "status": "DISMISSED"},
]

INVESTIGATORS = [
    {"investigator_id": 301, "first_name": "Rajesh", "last_name": "Sen", "email": "rajesh.sen@fraudlens-aml.org", "department": "Anti-Money Laundering", "experience_years": 9, "active_status": "ACTIVE"},
    {"investigator_id": 302, "first_name": "Kavita", "last_name": "Mishra", "email": "kavita.m@fraudlens-aml.org", "department": "Cyber Intelligence", "experience_years": 6, "active_status": "ACTIVE"},
    {"investigator_id": 303, "first_name": "Suresh", "last_name": "Bose", "email": "suresh.bose@fraudlens-ops.org", "department": "Risk Operations", "experience_years": 4, "active_status": "ACTIVE"},
    {"investigator_id": 304, "first_name": "Farhan", "last_name": "Qureshi", "email": "farhan.q@fraudlens-aml.org", "department": "Financial Crimes", "experience_years": 11, "active_status": "INACTIVE"},
]

INVESTIGATIONS = [
    {"investigation_id": 9001, "alert_id": 7001, "investigator_id": 302, "start_date": "2024-02-01", "end_date": None, "status": "UNDER REVIEW", "outcome": "PENDING", "notes": "IP geolocation indicates overseas proxy used during midnight transfer. Awaiting telecom ISP logs."},
    {"investigation_id": 9002, "alert_id": 7002, "investigator_id": 301, "start_date": "2024-02-01", "end_date": "2024-02-05", "status": "CLOSED", "outcome": "CONFIRMED_FRAUD", "notes": "Corroborated account takeover. Mule counterparty frozen by law enforcement agency."},
    {"investigation_id": 9003, "alert_id": 7003, "investigator_id": 303, "start_date": "2024-02-03", "end_date": "2024-02-04", "status": "CLOSED", "outcome": "FALSE_POSITIVE", "notes": "Customer confirmed legitimate cash requirement for property registration. High wealth tier verified."},
    {"investigation_id": 9004, "alert_id": 7004, "investigator_id": 301, "start_date": "2024-02-04", "end_date": None, "status": "OPEN", "outcome": "PENDING", "notes": "Offshore shell corporation escrow alert. Requested AML compliance documentation from correspondent bank."},
    {"investigation_id": 9005, "alert_id": 7006, "investigator_id": 302, "start_date": "2024-02-16", "end_date": None, "status": "UNDER REVIEW", "outcome": "PENDING", "notes": "Smurfing pattern detected across UPI channels. Linked multiple dummy accounts to same device hardware ID."},
]

INVESTIGATION_AUDITS = []
ALERT_AUDITS = []
