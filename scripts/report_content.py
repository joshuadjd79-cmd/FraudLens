"""
FraudLens: Master Content Repository for Case Study Report
Contains all 31 academic sections, metadata, table data, SQL code snippets,
query results, test cases, and figure references.
"""

STUDENT_INFO = {
    "title": "FraudLens: Financial Transaction and Fraud Investigation Management System",
    "subtitle": "A Comprehensive Database Management Systems Case Study Report",
    "students": [
        {"name": "D Joshua Daniel", "reg_no": "24BCE0436"},
        {"name": "M Saryu", "reg_no": "24BCE2524"}
    ],
    "student_name": "D Joshua Daniel & M Saryu",
    "reg_no": "24BCE0436, 24BCE2524",
    "degree": "Bachelor of Technology in Computer Science and Engineering",
    "subject": "Database Management Systems",
    "institution": "Vellore Institute of Technology",
    "guide": "Prof. Kanagaraj K",
    "submission_date": "October 2026",
    "db_platform": "Oracle AI Database 26ai Free Release 23.26.3.0.0",
    "container": "FREEPDB1",
    "schema": "FRAUDLENS_USER",
}

# 13 Test Cases data
TEST_CASES = [
    {
        "id": "1.1",
        "category": "Functional Workflow",
        "operation": "INSERT INTO TRANSACTIONS (ID 59999, Amount: INR 75,000.00, PENDING, NET_BANKING)",
        "expected": "Row created in TRANSACTIONS with PENDING status",
        "actual": "1 row created. Transaction 59999 inserted successfully.",
        "status": "PASSED"
    },
    {
        "id": "1.2",
        "category": "Stored Procedure",
        "operation": "EXEC SP_EVALUATE_AND_ALERT_TRANSACTION(59999, :v_alert_id)",
        "expected": "Breaches INR 50,000 threshold; generates Alert 7009",
        "actual": "[SUCCESS] Generated Fraud Alert 7009 for Transaction 59999.",
        "status": "PASSED"
    },
    {
        "id": "1.3",
        "category": "Functional Workflow",
        "operation": "INSERT INTO INVESTIGATION (ID 9999, Alert 7009, OPEN, PENDING)",
        "expected": "Case 9999 created in OPEN state linked to Alert 7009",
        "actual": "1 row created. Investigation 9999 opened and linked to Alert.",
        "status": "PASSED"
    },
    {
        "id": "1.4",
        "category": "Stored Procedure",
        "operation": "EXEC SP_ASSIGN_INVESTIGATOR(9999, 302)",
        "expected": "Allocates active investigator Kavita Mishra (ID 302)",
        "actual": "[SUCCESS] Assigned Investigator Kavita Mishra (ID: 302) to Case 9999.",
        "status": "PASSED"
    },
    {
        "id": "1.5",
        "category": "Stored Procedure",
        "operation": "EXEC SP_UPDATE_INVESTIGATION_STATUS(9999, 'CLOSED', 'CONFIRMED_FRAUD', 'Forensic proof validated')",
        "expected": "Transitions case to CLOSED and stamps end_date = SYSDATE",
        "actual": "[SUCCESS] Case 9999 status progressed from OPEN to CLOSED.",
        "status": "PASSED"
    },
    {
        "id": "1.6",
        "category": "Database Trigger",
        "operation": "SELECT COUNT(*) FROM INVESTIGATION_AUDIT WHERE investigation_id = 9999",
        "expected": "Row-level trigger records status transition event automatically",
        "actual": "Audit trigger successfully recorded 1 lifecycle events for Case 9999.",
        "status": "PASSED"
    },
    {
        "id": "1.7",
        "category": "Stored Functions",
        "operation": "SELECT FN_GET_TOTAL_TX_AMOUNT(2001), FN_CALCULATE_RISK_TIER(1001) FROM DUAL",
        "expected": "Returns cumulative transacted sum (INR 92,450) and risk tier LOW_RISK",
        "actual": "Account 2001 Volume: 92450 INR, Customer 1001 Tier: LOW_RISK",
        "status": "PASSED"
    },
    {
        "id": "2.1",
        "category": "Check Constraint",
        "operation": "INSERT INTO TRANSACTIONS with negative amount (-500.00 INR)",
        "expected": "Engine blocks insert with ORA-02290: check constraint CHK_TX_AMOUNT violated",
        "actual": "Blocked by CHECK constraint: ORA-02290: check constraint (FRAUDLENS_USER.CHK_TX_AMOUNT) violated",
        "status": "PASSED"
    },
    {
        "id": "2.2",
        "category": "Unique Constraint",
        "operation": "INSERT INTO CUSTOMER with duplicate email ('aarav.sharma@finmail.in')",
        "expected": "Engine blocks insert with ORA-00001: unique constraint UQ_CUSTOMER_EMAIL violated",
        "actual": "Blocked by UNIQUE constraint: ORA-00001: unique constraint (FRAUDLENS_USER.UQ_CUSTOMER_EMAIL) violated",
        "status": "PASSED"
    },
    {
        "id": "2.3",
        "category": "Foreign Key",
        "operation": "INSERT INTO ACCOUNT with non-existent customer_id = 999999",
        "expected": "Engine blocks orphan record with ORA-02291: integrity constraint FK_ACC_CUSTOMER violated",
        "actual": "Blocked by FOREIGN KEY constraint: ORA-02291: integrity constraint (FRAUDLENS_USER.FK_ACC_CUSTOMER) violated",
        "status": "PASSED"
    },
    {
        "id": "2.4",
        "category": "PL/SQL Exception",
        "operation": "EXEC SP_ASSIGN_INVESTIGATOR(9001, 304) [Investigator Farhan Qureshi is INACTIVE]",
        "expected": "Procedure raises user-defined exception ORA-20004",
        "actual": "Blocked with exception: ORA-20004: Error: Investigator Farhan Qureshi (ID 304) is INACTIVE.",
        "status": "PASSED"
    },
    {
        "id": "2.5",
        "category": "PL/SQL Exception",
        "operation": "EXEC SP_UPDATE_INVESTIGATION_STATUS(9001, 'CLOSED', NULL) [Missing outcome parameter]",
        "expected": "Procedure raises user-defined exception ORA-20012",
        "actual": "Blocked with exception: ORA-20012: Closing a case requires a definitive outcome.",
        "status": "PASSED"
    },
    {
        "id": "2.6",
        "category": "PL/SQL Exception",
        "operation": "SELECT FN_GET_TOTAL_TX_AMOUNT(999999) FROM DUAL [Non-existent account]",
        "expected": "Function raises user-defined exception ORA-20030",
        "actual": "Blocked with exception: ORA-20030: Account ID 999999 does not exist.",
        "status": "PASSED"
    }
]

# Database Object Inventory
DB_INVENTORY = [
    ("Tables", "8", "VALID", "CUSTOMER, ACCOUNT, TRANSACTIONS, FRAUD_ALERT, INVESTIGATOR, INVESTIGATION, INVESTIGATION_AUDIT, ALERT_AUDIT"),
    ("Baseline Records", "56", "VERIFIED", "10 Customers, 12 Accounts, 18 Transactions, 7 Fraud Alerts, 4 Investigators, 5 Investigations"),
    ("Sequences", "8", "VALID", "SEQ_CUSTOMER_ID (1011), SEQ_ACCOUNT_ID (2013), SEQ_TRANSACTION_ID (50019), SEQ_ALERT_ID (7009), SEQ_INVESTIGATOR_ID (305), SEQ_INVESTIGATION_ID (9006), SEQ_INVES_AUDIT_ID (4), SEQ_ALERT_AUDIT_ID (3)"),
    ("Views", "4", "VALID", "VW_HIGH_RISK_TRANSACTIONS, VW_INVESTIGATION_SUMMARY, VW_CUSTOMER_FRAUD_EXPOSURE, VW_UNASSIGNED_ALERTS"),
    ("Stored Procedures", "3", "VALID", "SP_ASSIGN_INVESTIGATOR, SP_UPDATE_INVESTIGATION_STATUS, SP_EVALUATE_AND_ALERT_TRANSACTION"),
    ("Stored Functions", "3", "VALID", "FN_GET_TOTAL_TX_AMOUNT, FN_GET_ACCOUNT_ALERT_COUNT, FN_CALCULATE_RISK_TIER"),
    ("Database Triggers", "2", "ENABLED", "TRG_INVESTIGATION_STATUS_AUDIT, TRG_FRAUD_ALERT_AUDIT"),
    ("Integrity Constraints", "71", "ENABLED", "53 CHECK constraints, 8 Primary Keys, 5 Foreign Keys (ON DELETE CASCADE), 5 Unique Keys"),
]

# Table Structures Definitions
TABLE_DEFINITIONS = [
    {
        "name": "CUSTOMER",
        "purpose": "Stores core retail and corporate banking client profiles, contact information, regulatory KYC status, and baseline risk indicators.",
        "pk": "customer_id NUMBER(10)",
        "fks": "None",
        "uks": "email VARCHAR2(100), phone VARCHAR2(15)",
        "checks": "kyc_status IN ('VERIFIED', 'PENDING', 'REJECTED'), risk_score BETWEEN 0 AND 100",
        "columns": [
            ("customer_id", "NUMBER(10)", "No", "None", "PK - Primary Key", "Unique identifier for each customer"),
            ("first_name", "VARCHAR2(50)", "No", "None", "NOT NULL", "Customer given name"),
            ("last_name", "VARCHAR2(50)", "No", "None", "NOT NULL", "Customer family name"),
            ("email", "VARCHAR2(100)", "No", "None", "UK, NOT NULL", "Unique customer electronic mail"),
            ("phone", "VARCHAR2(15)", "No", "None", "UK, NOT NULL", "Unique telephone number with country code"),
            ("kyc_status", "VARCHAR2(15)", "No", "'PENDING'", "CHECK Enum", "KYC compliance tier: VERIFIED, PENDING, REJECTED"),
            ("risk_score", "NUMBER(3)", "No", "10", "CHECK (0..100)", "Baseline heuristic credit/fraud risk score (0-100)"),
            ("created_at", "DATE", "No", "SYSDATE", "NOT NULL", "Date of customer onboarding")
        ]
    },
    {
        "name": "ACCOUNT",
        "purpose": "Maintains bank accounts linked to customers, holding operational balances, account types, currencies, and account lifecycle status.",
        "pk": "account_id NUMBER(10)",
        "fks": "customer_id -> CUSTOMER(customer_id) ON DELETE CASCADE",
        "uks": "account_number VARCHAR2(20)",
        "checks": "account_type IN ('SAVINGS', 'CURRENT', 'SALARY', 'NRI'), balance >= 0, status IN ('ACTIVE', 'FROZEN', 'DORMANT', 'CLOSED')",
        "columns": [
            ("account_id", "NUMBER(10)", "No", "None", "PK - Primary Key", "Unique internal account identifier"),
            ("customer_id", "NUMBER(10)", "No", "None", "FK -> CUSTOMER", "Foreign key identifying account owner"),
            ("account_number", "VARCHAR2(20)", "No", "None", "UK, NOT NULL", "Standardized external account number (e.g. SB-1001-01)"),
            ("account_type", "VARCHAR2(20)", "No", "'SAVINGS'", "CHECK Enum", "Category: SAVINGS, CURRENT, SALARY, NRI"),
            ("balance", "NUMBER(15,2)", "No", "0.00", "CHECK >= 0", "Current ledger balance (non-negative)"),
            ("currency", "VARCHAR2(5)", "No", "'INR'", "NOT NULL", "Currency code (default INR)"),
            ("status", "VARCHAR2(15)", "No", "'ACTIVE'", "CHECK Enum", "Operational state: ACTIVE, FROZEN, DORMANT, CLOSED"),
            ("created_at", "DATE", "No", "SYSDATE", "NOT NULL", "Timestamp of account opening")
        ]
    },
    {
        "name": "TRANSACTIONS",
        "purpose": "Auditable financial movement ledger recording all monetary debits, credits, transfers, and digital payment operations across channels.",
        "pk": "transaction_id NUMBER(12)",
        "fks": "account_id -> ACCOUNT(account_id) ON DELETE CASCADE",
        "uks": "None",
        "checks": "transaction_type IN ('DEPOSIT', 'WITHDRAWAL', 'TRANSFER', 'PAYMENT'), amount > 0, channel IN ('MOBILE_APP', 'NET_BANKING', 'ATM', 'POS', 'UPI'), status IN ('COMPLETED', 'PENDING', 'FLAGGED', 'FAILED')",
        "columns": [
            ("transaction_id", "NUMBER(12)", "No", "None", "PK - Primary Key", "Unique transaction reference sequence"),
            ("account_id", "NUMBER(10)", "No", "None", "FK -> ACCOUNT", "Account from which funds move"),
            ("transaction_type", "VARCHAR2(20)", "No", "None", "CHECK Enum", "Movement type: DEPOSIT, WITHDRAWAL, TRANSFER, PAYMENT"),
            ("amount", "NUMBER(15,2)", "No", "None", "CHECK > 0, NOT NULL", "Monetary transaction value in INR"),
            ("transaction_date", "TIMESTAMP", "No", "SYSTIMESTAMP", "NOT NULL", "Precise timestamp of execution"),
            ("channel", "VARCHAR2(20)", "No", "None", "CHECK Enum", "Execution medium: MOBILE_APP, NET_BANKING, ATM, POS, UPI"),
            ("status", "VARCHAR2(15)", "No", "'COMPLETED'", "CHECK Enum", "State: COMPLETED, PENDING, FLAGGED, FAILED"),
            ("counterparty_account", "VARCHAR2(30)", "Yes", "None", "Optional", "Destination account or merchant reference"),
            ("description", "VARCHAR2(200)", "Yes", "None", "Optional", "Transaction remarks or narration")
        ]
    },
    {
        "name": "FRAUD_ALERT",
        "purpose": "Stores anomaly signals triggered when transactions breach heuristic thresholds. A fraud alert is an investigative signal, not legal proof of fraud.",
        "pk": "alert_id NUMBER(10)",
        "fks": "transaction_id -> TRANSACTIONS(transaction_id) ON DELETE CASCADE",
        "uks": "None",
        "checks": "alert_type IN ('HIGH_AMOUNT', 'RAPID_VELOCITY', 'SUSPICIOUS_CHANNEL', 'UNUSUAL_HOURS', 'CROSS_BORDER', 'STRUCTURING'), severity IN ('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'), status IN ('PENDING', 'ESCALATED', 'DISMISSED', 'RESOLVED')",
        "columns": [
            ("alert_id", "NUMBER(10)", "No", "None", "PK - Primary Key", "Unique surveillance alert identifier"),
            ("transaction_id", "NUMBER(12)", "No", "None", "FK -> TRANSACTIONS", "Reference to the suspicious transaction"),
            ("alert_type", "VARCHAR2(30)", "No", "None", "CHECK Enum", "Categorization of anomaly"),
            ("severity", "VARCHAR2(15)", "No", "'MEDIUM'", "CHECK Enum", "Risk level: LOW, MEDIUM, HIGH, CRITICAL"),
            ("rule_triggered", "VARCHAR2(150)", "No", "None", "NOT NULL", "Text description of rule criteria violated"),
            ("alert_date", "TIMESTAMP", "No", "SYSTIMESTAMP", "NOT NULL", "Timestamp of automated alert generation"),
            ("status", "VARCHAR2(15)", "No", "'PENDING'", "CHECK Enum", "Triage status: PENDING, ESCALATED, DISMISSED, RESOLVED")
        ]
    },
    {
        "name": "INVESTIGATOR",
        "purpose": "Maintains directory of authorized compliance officers, Anti-Money Laundering (AML) analysts, and cyber-forensic caseworkers.",
        "pk": "investigator_id NUMBER(6)",
        "fks": "None",
        "uks": "email VARCHAR2(100)",
        "checks": "experience_years >= 0, active_status IN ('ACTIVE', 'INACTIVE')",
        "columns": [
            ("investigator_id", "NUMBER(6)", "No", "None", "PK - Primary Key", "Unique investigator credential identifier"),
            ("first_name", "VARCHAR2(50)", "No", "None", "NOT NULL", "Forensic officer given name"),
            ("last_name", "VARCHAR2(50)", "No", "None", "NOT NULL", "Forensic officer surname"),
            ("email", "VARCHAR2(100)", "No", "None", "UK, NOT NULL", "Official investigator corporate email"),
            ("department", "VARCHAR2(50)", "No", "None", "NOT NULL", "Division: AML, Forensic Cyber, Risk Triage"),
            ("experience_years", "NUMBER(3)", "No", "0", "CHECK >= 0", "Professional tenure in fraud analysis"),
            ("active_status", "VARCHAR2(15)", "No", "'ACTIVE'", "CHECK Enum", "Casework eligibility: ACTIVE, INACTIVE")
        ]
    },
    {
        "name": "INVESTIGATION",
        "purpose": "Formal investigative case dossier linking a high-severity fraud alert to a designated investigator, tracking findings and final verdict.",
        "pk": "investigation_id NUMBER(10)",
        "fks": "alert_id -> FRAUD_ALERT(alert_id) ON DELETE CASCADE UNIQUE, investigator_id -> INVESTIGATOR(investigator_id)",
        "uks": "alert_id (1:1 Relationship with Alert)",
        "checks": "status IN ('OPEN', 'UNDER REVIEW', 'CLOSED'), outcome IN ('CONFIRMED_FRAUD', 'FALSE_POSITIVE', 'INCONCLUSIVE', 'PENDING'), end_date IS NULL OR end_date >= start_date",
        "columns": [
            ("investigation_id", "NUMBER(10)", "No", "None", "PK - Primary Key", "Unique case docket identifier"),
            ("alert_id", "NUMBER(10)", "No", "None", "FK, UK -> FRAUD_ALERT", "Unique link to source fraud alert (1:1)"),
            ("investigator_id", "NUMBER(6)", "Yes", "None", "FK -> INVESTIGATOR", "Assigned lead investigator officer"),
            ("start_date", "DATE", "No", "SYSDATE", "NOT NULL", "Date case investigation initiated"),
            ("end_date", "DATE", "Yes", "None", "CHECK >= start_date", "Date case officially concluded"),
            ("status", "VARCHAR2(15)", "No", "'OPEN'", "CHECK Enum", "Lifecycle: OPEN, UNDER REVIEW, CLOSED"),
            ("outcome", "VARCHAR2(20)", "No", "'PENDING'", "CHECK Enum", "Verdict: CONFIRMED_FRAUD, FALSE_POSITIVE, INCONCLUSIVE, PENDING"),
            ("notes", "VARCHAR2(1000)", "Yes", "None", "Optional", "Forensic narrative and evidentiary remarks")
        ]
    },
    {
        "name": "INVESTIGATION_AUDIT",
        "purpose": "Chronological audit event log populated autonomously by row-level triggers to capture lifecycle state transitions of investigation dockets.",
        "pk": "audit_id NUMBER(10)",
        "fks": "None (Decoupled audit log)",
        "uks": "None",
        "checks": "Populated exclusively via row-level triggers",
        "columns": [
            ("audit_id", "NUMBER(10)", "No", "None", "PK - Primary Key", "Audit sequence identifier"),
            ("investigation_id", "NUMBER(10)", "No", "None", "NOT NULL", "Reference to the modified investigation docket"),
            ("old_status", "VARCHAR2(15)", "Yes", "None", "Optional", "Status before change (e.g. OPEN)"),
            ("new_status", "VARCHAR2(15)", "Yes", "None", "Optional", "Status after transition (e.g. CLOSED)"),
            ("changed_by", "VARCHAR2(50)", "No", "USER", "NOT NULL", "Oracle database session user executing update"),
            ("change_timestamp", "TIMESTAMP", "No", "SYSTIMESTAMP", "NOT NULL", "Exact system timestamp of modification"),
            ("change_action", "VARCHAR2(20)", "No", "'STATUS_UPDATE'", "NOT NULL", "Audit action classification")
        ]
    },
    {
        "name": "ALERT_AUDIT",
        "purpose": "Chronological audit event log populated autonomously by row-level triggers to track alert triage state changes.",
        "pk": "audit_id NUMBER(10)",
        "fks": "None (Decoupled audit log)",
        "uks": "None",
        "checks": "Populated exclusively via row-level triggers",
        "columns": [
            ("audit_id", "NUMBER(10)", "No", "None", "PK - Primary Key", "Audit sequence identifier"),
            ("alert_id", "NUMBER(10)", "No", "None", "NOT NULL", "Reference to modified fraud alert"),
            ("old_status", "VARCHAR2(15)", "Yes", "None", "Optional", "Previous triage state"),
            ("new_status", "VARCHAR2(15)", "Yes", "None", "Optional", "New triage state"),
            ("changed_by", "VARCHAR2(50)", "No", "USER", "NOT NULL", "Database session user"),
            ("change_timestamp", "TIMESTAMP", "No", "SYSTIMESTAMP", "NOT NULL", "Timestamp of modification"),
            ("remarks", "VARCHAR2(200)", "Yes", "None", "Optional", "Audit narrative remarks")
        ]
    }
]
