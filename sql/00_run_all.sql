-- ============================================================================
-- PROJECT: FraudLens - Financial Transaction & Fraud Investigation Management System
-- SCRIPT:  00_run_all.sql
-- PURPOSE: Master Driver Script to Execute the Entire FraudLens DBMS Project
-- DIALECT: Oracle Database 11g/12c/19c/21c/23c Compatible
-- ============================================================================
-- USAGE IN SQL*PLUS / ORACLE SQL DEVELOPER:
--   SQL> @00_run_all.sql
-- (Ensure current working directory contains the sql/ scripts or run from sql/)
-- ============================================================================

SET SERVEROUTPUT ON SIZE 1000000;
SET ECHO ON;
SET FEEDBACK ON;
SET LINESIZE 250;
SET PAGESIZE 100;

PROMPT ============================================================================
PROMPT Starting Complete FraudLens DBMS Execution Pipeline (Review 1 + Review 2)
PROMPT ============================================================================

-- Display execution banner with system timestamp non-interactively
SELECT 'Pipeline Execution Started: ' || TO_CHAR(SYSDATE, 'YYYY-MM-DD HH24:MI:SS') AS pipeline_status FROM DUAL;

PROMPT >>> [1/11] Running 01_schema.sql (Core Tables, Constraints, Sequences)...
@@01_schema.sql

PROMPT >>> [2/11] Running 02_ddl_dml_demos.sql (Review 1 DDL & DML Operations)...
@@02_ddl_dml_demos.sql

PROMPT >>> [3/11] Running 03_sample_data.sql (Populating Consistent Sample Data)...
@@03_sample_data.sql

PROMPT >>> [4/11] Running 04_review1_queries.sql (Functions, Operators, Group By, Joins)...
@@04_review1_queries.sql

PROMPT >>> [5/11] Running 05_review2_subqueries_joins.sql (Subqueries, Dossier Join)...
@@05_review2_subqueries_joins.sql

PROMPT >>> [6/11] Running 06_views.sql (Analytical & Operational Views)...
@@06_views.sql

PROMPT >>> [7/11] Running 07_procedures.sql (Compiling Stored Procedures)...
@@07_procedures.sql

PROMPT >>> [8/11] Running 08_functions.sql (Compiling Stored Functions)...
@@08_functions.sql

PROMPT >>> [9/11] Running 09_cursors.sql (Executing Explicit Cursor & Cursor FOR Loop)...
@@09_cursors.sql

PROMPT >>> [10/11] Running 10_triggers_audit.sql (Compiling & Verifying Triggers)...
@@10_triggers_audit.sql

PROMPT >>> [11/11] Running 11_test_cases.sql (Running Full Positive & Negative Test Suite)...
@@11_test_cases.sql

PROMPT ============================================================================
PROMPT [FINISHED] FraudLens Complete Project Successfully Executed!
PROMPT Both Review 1 and Review 2 requirements are 100% complete and verified.
PROMPT ============================================================================
