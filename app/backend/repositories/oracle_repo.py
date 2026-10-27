"""
FraudLens: Oracle Database Repository
Executes SQL queries, views, and PL/SQL stored procedures against live Oracle AI Database 26ai.
"""

import logging
from typing import List, Dict, Any, Optional, Tuple
import oracledb
from app.backend.database.connection import get_db_connection
from app.backend.config import settings

logger = logging.getLogger("fraudlens.oracle_repo")

def row_to_dict(cursor, row):
    """Converts an Oracle cursor row into a Python dictionary."""
    if row is None:
        return None
    columns = [col[0].lower() for col in cursor.description]
    result = {}
    for col_name, val in zip(columns, row):
        if hasattr(val, "strftime"):
            result[col_name] = val.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(val, (int, float)):
            result[col_name] = val
        elif val is None:
            result[col_name] = None
        else:
            result[col_name] = str(val)
    return result

class OracleRepository:

    @staticmethod
    def get_dashboard_summary() -> Dict[str, Any]:
        """Fetches executive KPIs directly from live Oracle tables."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Total transactions & volume
                cur.execute("""
                    SELECT COUNT(*), NVL(SUM(amount), 0),
                           COUNT(CASE WHEN status = 'FLAGGED' THEN 1 END)
                    FROM TRANSACTIONS
                """)
                tx_count, tx_volume, flagged_tx = cur.fetchone()

                # Alert statistics
                cur.execute("""
                    SELECT COUNT(*),
                           COUNT(CASE WHEN status = 'PENDING' THEN 1 END),
                           COUNT(CASE WHEN severity = 'CRITICAL' THEN 1 END)
                    FROM FRAUD_ALERT
                """)
                alert_count, pending_alerts, critical_alerts = cur.fetchone()

                # Investigation statistics
                cur.execute("""
                    SELECT COUNT(CASE WHEN status = 'OPEN' THEN 1 END),
                           COUNT(CASE WHEN status = 'UNDER REVIEW' THEN 1 END),
                           COUNT(CASE WHEN status = 'CLOSED' THEN 1 END),
                           COUNT(CASE WHEN outcome = 'CONFIRMED_FRAUD' THEN 1 END)
                    FROM INVESTIGATION
                """)
                open_inv, under_review_inv, closed_inv, confirmed_fraud = cur.fetchone()

                # Active investigators
                cur.execute("SELECT COUNT(*) FROM INVESTIGATOR WHERE active_status = 'ACTIVE'")
                active_investigators = cur.fetchone()[0]

                return {
                    "total_transactions": tx_count,
                    "total_volume_inr": float(tx_volume),
                    "flagged_transactions": flagged_tx,
                    "total_alerts": alert_count,
                    "pending_alerts": pending_alerts,
                    "critical_alerts": critical_alerts,
                    "open_investigations": open_inv,
                    "under_review_investigations": under_review_inv,
                    "closed_investigations": closed_inv,
                    "confirmed_fraud_cases": confirmed_fraud,
                    "active_investigators": active_investigators,
                    "high_amount_threshold": settings.HIGH_AMOUNT_THRESHOLD
                }

    @staticmethod
    def get_transaction_trends() -> List[Dict[str, Any]]:
        """Groups transaction volume and counts by day."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT TO_CHAR(transaction_date, 'YYYY-MM-DD') AS tx_date,
                           NVL(SUM(amount), 0) AS total_vol,
                           COUNT(*) AS tx_cnt,
                           COUNT(CASE WHEN status = 'FLAGGED' THEN 1 END) AS flagged_cnt
                    FROM TRANSACTIONS
                    GROUP BY TO_CHAR(transaction_date, 'YYYY-MM-DD')
                    ORDER BY tx_date ASC
                """)
                rows = cur.fetchall()
                return [
                    {
                        "date": r[0],
                        "total_volume": float(r[1]),
                        "tx_count": r[2],
                        "flagged_count": r[3]
                    }
                    for r in rows
                ]

    @staticmethod
    def get_channel_metrics() -> List[Dict[str, Any]]:
        """Channel-wise breakdown demonstrating review group-by aggregations."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT channel,
                           COUNT(*) AS total_tx,
                           NVL(SUM(amount), 0) AS total_volume,
                           ROUND(AVG(amount), 2) AS avg_ticket
                    FROM TRANSACTIONS
                    GROUP BY channel
                    ORDER BY total_volume DESC
                """)
                rows = cur.fetchall()
                return [
                    {
                        "channel": r[0],
                        "total_tx": r[1],
                        "total_volume": float(r[2]),
                        "avg_ticket": float(r[3])
                    }
                    for r in rows
                ]

    @staticmethod
    def get_severity_breakdown() -> List[Dict[str, Any]]:
        """Alert severity breakdown."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT severity, COUNT(*)
                    FROM FRAUD_ALERT
                    GROUP BY severity
                    ORDER BY COUNT(*) DESC
                """)
                return [{"severity": r[0], "count": r[1]} for r in cur.fetchall()]

    @staticmethod
    def get_outcome_breakdown() -> List[Dict[str, Any]]:
        """Investigation outcome breakdown."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT outcome, COUNT(*)
                    FROM INVESTIGATION
                    GROUP BY outcome
                    ORDER BY COUNT(*) DESC
                """)
                return [{"outcome": r[0], "count": r[1]} for r in cur.fetchall()]

    @staticmethod
    def get_transactions(
        page: int = 1,
        page_size: int = 10,
        account_id: Optional[int] = None,
        channel: Optional[str] = None,
        transaction_type: Optional[str] = None,
        status: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Paginated transaction query with multi-column joins and filters."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                where_clauses = ["1=1"]
                params: Dict[str, Any] = {}

                if account_id:
                    where_clauses.append("t.account_id = :acc_id")
                    params["acc_id"] = account_id
                if channel:
                    where_clauses.append("t.channel = :channel")
                    params["channel"] = channel
                if transaction_type:
                    where_clauses.append("t.transaction_type = :tx_type")
                    params["tx_type"] = transaction_type
                if status:
                    where_clauses.append("t.status = :status")
                    params["status"] = status
                if min_amount is not None:
                    where_clauses.append("t.amount >= :min_amt")
                    params["min_amt"] = min_amount
                if max_amount is not None:
                    where_clauses.append("t.amount <= :max_amt")
                    params["max_amt"] = max_amount
                if search:
                    where_clauses.append("(TO_CHAR(t.transaction_id) LIKE :search OR UPPER(t.description) LIKE :search OR UPPER(a.account_number) LIKE :search OR UPPER(c.first_name || ' ' || c.last_name) LIKE :search)")
                    params["search"] = f"%{search.upper()}%"

                where_sql = " AND ".join(where_clauses)

                # Total count
                count_sql = f"""
                    SELECT COUNT(*)
                    FROM TRANSACTIONS t
                    JOIN ACCOUNT a ON t.account_id = a.account_id
                    JOIN CUSTOMER c ON a.customer_id = c.customer_id
                    WHERE {where_sql}
                """
                cur.execute(count_sql, params)
                total = cur.fetchone()[0]

                offset = (page - 1) * page_size
                params["offset"] = offset
                params["limit"] = page_size

                query_sql = f"""
                    SELECT t.transaction_id, t.account_id, a.account_number,
                           c.customer_id, (c.first_name || ' ' || c.last_name) AS customer_name,
                           t.transaction_type, t.amount,
                           TO_CHAR(t.transaction_date, 'YYYY-MM-DD HH24:MI:SS') AS transaction_date,
                           t.channel, t.status, t.counterparty_account, t.description,
                           fa.alert_id, fa.rule_triggered
                    FROM TRANSACTIONS t
                    JOIN ACCOUNT a ON t.account_id = a.account_id
                    JOIN CUSTOMER c ON a.customer_id = c.customer_id
                    LEFT JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id
                    WHERE {where_sql}
                    ORDER BY t.transaction_id DESC
                    OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
                """
                cur.execute(query_sql, params)
                rows = cur.fetchall()

                items = []
                for r in rows:
                    items.append({
                        "transaction_id": r[0],
                        "account_id": r[1],
                        "account_number": r[2],
                        "customer_id": r[3],
                        "customer_name": r[4],
                        "transaction_type": r[5],
                        "amount": float(r[6]),
                        "transaction_date": r[7],
                        "channel": r[8],
                        "status": r[9],
                        "counterparty_account": r[10],
                        "description": r[11],
                        "alert_generated": bool(r[12]),
                        "alert_id": r[12],
                        "rule_triggered": r[13]
                    })
                return items, total

    @staticmethod
    def get_transaction_by_id(tx_id: int) -> Optional[Dict[str, Any]]:
        """Fetches single transaction dossier."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT t.transaction_id, t.account_id, a.account_number,
                           c.customer_id, (c.first_name || ' ' || c.last_name) AS customer_name,
                           t.transaction_type, t.amount,
                           TO_CHAR(t.transaction_date, 'YYYY-MM-DD HH24:MI:SS') AS transaction_date,
                           t.channel, t.status, t.counterparty_account, t.description,
                           fa.alert_id, fa.rule_triggered
                    FROM TRANSACTIONS t
                    JOIN ACCOUNT a ON t.account_id = a.account_id
                    JOIN CUSTOMER c ON a.customer_id = c.customer_id
                    LEFT JOIN FRAUD_ALERT fa ON t.transaction_id = fa.transaction_id
                    WHERE t.transaction_id = :tx_id
                """, {"tx_id": tx_id})
                row = cur.fetchone()
                if not row:
                    return None
                return {
                    "transaction_id": row[0],
                    "account_id": row[1],
                    "account_number": row[2],
                    "customer_id": row[3],
                    "customer_name": row[4],
                    "transaction_type": row[5],
                    "amount": float(row[6]),
                    "transaction_date": row[7],
                    "channel": row[8],
                    "status": row[9],
                    "counterparty_account": row[10],
                    "description": row[11],
                    "alert_generated": bool(row[12]),
                    "alert_id": row[12],
                    "rule_triggered": row[13]
                }

    @staticmethod
    def create_transaction(
        account_id: int,
        transaction_type: str,
        amount: float,
        channel: str,
        counterparty_account: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Inserts new transaction into Oracle, then evaluates the procedural
        surveillance rule via SP_EVALUATE_AND_ALERT_TRANSACTION if amount > threshold.
        """
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # 1. Fetch next transaction ID via sequence
                cur.execute("SELECT seq_transaction_id.NEXTVAL FROM DUAL")
                next_tx_id = cur.fetchone()[0]

                # 2. Insert transaction
                cur.execute("""
                    INSERT INTO TRANSACTIONS (
                        transaction_id, account_id, transaction_type, amount,
                        transaction_date, channel, status, counterparty_account, description
                    ) VALUES (
                        :tx_id, :acc_id, :tx_type, :amount,
                        SYSTIMESTAMP, :channel, 'COMPLETED', :counterparty, :descr
                    )
                """, {
                    "tx_id": next_tx_id,
                    "acc_id": account_id,
                    "tx_type": transaction_type,
                    "amount": amount,
                    "channel": channel,
                    "counterparty": counterparty_account,
                    "descr": description or f"Payment via {channel}"
                })

                alert_id_out = None
                rule_desc = None

                # 3. Call stored procedure SP_EVALUATE_AND_ALERT_TRANSACTION
                p_alert_id = cur.var(oracledb.NUMBER)
                cur.callproc("SP_EVALUATE_AND_ALERT_TRANSACTION", [next_tx_id, p_alert_id])
                alert_val = p_alert_id.getvalue()

                if alert_val is not None:
                    alert_id_out = int(alert_val)
                    cur.execute("SELECT rule_triggered FROM FRAUD_ALERT WHERE alert_id = :aid", {"aid": alert_id_out})
                    r_row = cur.fetchone()
                    rule_desc = r_row[0] if r_row else "High Amount threshold violated"

                conn.commit()

                # Fetch fresh record
                created_record = OracleRepository.get_transaction_by_id(next_tx_id)
                if created_record:
                    created_record["alert_generated"] = (alert_id_out is not None)
                    created_record["alert_id"] = alert_id_out
                    created_record["rule_triggered"] = rule_desc
                return created_record

    @staticmethod
    def get_alerts(
        page: int = 1,
        page_size: int = 10,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        alert_type: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Fetches fraud alerts with related transaction and investigation links."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                where_clauses = ["1=1"]
                params: Dict[str, Any] = {}

                if severity:
                    where_clauses.append("fa.severity = :sev")
                    params["sev"] = severity
                if status:
                    where_clauses.append("fa.status = :status")
                    params["status"] = status
                if alert_type:
                    where_clauses.append("fa.alert_type = :atype")
                    params["atype"] = alert_type
                if search:
                    where_clauses.append("(TO_CHAR(fa.alert_id) LIKE :search OR UPPER(fa.rule_triggered) LIKE :search OR TO_CHAR(fa.transaction_id) LIKE :search)")
                    params["search"] = f"%{search.upper()}%"

                where_sql = " AND ".join(where_clauses)

                count_sql = f"SELECT COUNT(*) FROM FRAUD_ALERT fa WHERE {where_sql}"
                cur.execute(count_sql, params)
                total = cur.fetchone()[0]

                offset = (page - 1) * page_size
                params["offset"] = offset
                params["limit"] = page_size

                query_sql = f"""
                    SELECT fa.alert_id, fa.transaction_id, fa.alert_type, fa.severity,
                           fa.rule_triggered,
                           TO_CHAR(fa.alert_date, 'YYYY-MM-DD HH24:MI:SS') AS alert_date,
                           fa.status,
                           t.amount, t.channel, a.account_number,
                           (c.first_name || ' ' || c.last_name) AS customer_name,
                           inv.investigation_id
                    FROM FRAUD_ALERT fa
                    JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id
                    JOIN ACCOUNT a ON t.account_id = a.account_id
                    JOIN CUSTOMER c ON a.customer_id = c.customer_id
                    LEFT JOIN INVESTIGATION inv ON fa.alert_id = inv.alert_id
                    WHERE {where_sql}
                    ORDER BY fa.alert_id DESC
                    OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
                """
                cur.execute(query_sql, params)
                rows = cur.fetchall()

                items = []
                for r in rows:
                    items.append({
                        "alert_id": r[0],
                        "transaction_id": r[1],
                        "alert_type": r[2],
                        "severity": r[3],
                        "rule_triggered": r[4],
                        "alert_date": r[5],
                        "status": r[6],
                        "amount": float(r[7]),
                        "channel": r[8],
                        "account_number": r[9],
                        "customer_name": r[10],
                        "has_investigation": bool(r[11]),
                        "investigation_id": r[11]
                    })
                return items, total

    @staticmethod
    def get_alert_by_id(alert_id: int) -> Optional[Dict[str, Any]]:
        """Fetches single alert by ID."""
        items, _ = OracleRepository.get_alerts(page=1, page_size=1, search=str(alert_id))
        for item in items:
            if item["alert_id"] == alert_id:
                return item
        return None

    @staticmethod
    def get_investigations(
        page: int = 1,
        page_size: int = 10,
        status: Optional[str] = None,
        outcome: Optional[str] = None,
        investigator_id: Optional[int] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Fetches investigation case dossiers."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                where_clauses = ["1=1"]
                params: Dict[str, Any] = {}

                if status:
                    where_clauses.append("inv.status = :status")
                    params["status"] = status
                if outcome:
                    where_clauses.append("inv.outcome = :outcome")
                    params["outcome"] = outcome
                if investigator_id:
                    where_clauses.append("inv.investigator_id = :invid")
                    params["invid"] = investigator_id
                if search:
                    where_clauses.append("(TO_CHAR(inv.investigation_id) LIKE :search OR UPPER(inv.notes) LIKE :search OR TO_CHAR(inv.alert_id) LIKE :search)")
                    params["search"] = f"%{search.upper()}%"

                where_sql = " AND ".join(where_clauses)

                count_sql = f"SELECT COUNT(*) FROM INVESTIGATION inv WHERE {where_sql}"
                cur.execute(count_sql, params)
                total = cur.fetchone()[0]

                offset = (page - 1) * page_size
                params["offset"] = offset
                params["limit"] = page_size

                query_sql = f"""
                    SELECT inv.investigation_id, inv.alert_id, inv.investigator_id,
                           NVL(i.first_name || ' ' || i.last_name, 'UNASSIGNED') AS investigator_name,
                           i.department AS investigator_dept,
                           TO_CHAR(inv.start_date, 'YYYY-MM-DD') AS start_date,
                           TO_CHAR(inv.end_date, 'YYYY-MM-DD') AS end_date,
                           inv.status, inv.outcome, inv.notes,
                           fa.alert_type, fa.severity, fa.rule_triggered,
                           fa.transaction_id, t.amount, t.channel,
                           a.account_number, (c.first_name || ' ' || c.last_name) AS customer_name
                    FROM INVESTIGATION inv
                    JOIN FRAUD_ALERT fa ON inv.alert_id = fa.alert_id
                    JOIN TRANSACTIONS t ON fa.transaction_id = t.transaction_id
                    JOIN ACCOUNT a ON t.account_id = a.account_id
                    JOIN CUSTOMER c ON a.customer_id = c.customer_id
                    LEFT JOIN INVESTIGATOR i ON inv.investigator_id = i.investigator_id
                    WHERE {where_sql}
                    ORDER BY inv.investigation_id DESC
                    OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
                """
                cur.execute(query_sql, params)
                rows = cur.fetchall()

                items = []
                for r in rows:
                    items.append({
                        "investigation_id": r[0],
                        "alert_id": r[1],
                        "investigator_id": r[2],
                        "investigator_name": r[3],
                        "investigator_dept": r[4],
                        "start_date": r[5],
                        "end_date": r[6],
                        "status": r[7],
                        "outcome": r[8],
                        "notes": r[9],
                        "alert_type": r[10],
                        "severity": r[11],
                        "rule_triggered": r[12],
                        "transaction_id": r[13],
                        "amount": float(r[14]),
                        "channel": r[15],
                        "account_number": r[16],
                        "customer_name": r[17]
                    })
                return items, total

    @staticmethod
    def get_investigation_by_id(investigation_id: int) -> Optional[Dict[str, Any]]:
        """Fetches single investigation dossier by ID."""
        items, _ = OracleRepository.get_investigations(page=1, page_size=1, search=str(investigation_id))
        for item in items:
            if item["investigation_id"] == investigation_id:
                return item
        return None

    @staticmethod
    def create_investigation(alert_id: int, investigator_id: Optional[int] = None, notes: Optional[str] = None) -> Dict[str, Any]:
        """Creates a new case docket in OPEN status linking to unassigned alert."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT seq_investigation_id.NEXTVAL FROM DUAL")
                inv_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO INVESTIGATION (
                        investigation_id, alert_id, investigator_id,
                        start_date, status, outcome, notes
                    ) VALUES (
                        :invid, :aid, :iid,
                        SYSDATE, 'OPEN', 'PENDING', :notes
                    )
                """, {
                    "invid": inv_id,
                    "aid": alert_id,
                    "iid": investigator_id,
                    "notes": notes or "Case docket opened via Web Application"
                })

                # If investigator assigned initially, call procedure
                if investigator_id:
                    cur.callproc("SP_ASSIGN_INVESTIGATOR", [inv_id, investigator_id])

                conn.commit()

                # Fetch newly created investigation
                items, _ = OracleRepository.get_investigations(page=1, page_size=1, search=str(inv_id))
                return items[0] if items else {"investigation_id": inv_id, "alert_id": alert_id, "status": "OPEN"}

    @staticmethod
    def assign_investigator(investigation_id: int, investigator_id: int) -> bool:
        """Executes SP_ASSIGN_INVESTIGATOR stored procedure."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.callproc("SP_ASSIGN_INVESTIGATOR", [investigation_id, investigator_id])
                conn.commit()
                return True

    @staticmethod
    def update_investigation_status(
        investigation_id: int,
        new_status: str,
        outcome: Optional[str] = None,
        notes: Optional[str] = None
    ) -> bool:
        """
        Executes SP_UPDATE_INVESTIGATION_STATUS stored procedure.
        Fires TRG_INVESTIGATION_STATUS_AUDIT trigger to log status transition.
        """
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.callproc("SP_UPDATE_INVESTIGATION_STATUS", [investigation_id, new_status, outcome, notes])
                conn.commit()
                return True

    @staticmethod
    def get_audit_logs(
        page: int = 1,
        page_size: int = 15,
        source_table: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Fetches trigger-generated audit records from INVESTIGATION_AUDIT & ALERT_AUDIT."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                union_parts = []
                if not source_table or source_table == "INVESTIGATION_AUDIT":
                    union_parts.append("""
                        SELECT audit_id, 'INVESTIGATION_AUDIT' AS source_table,
                               investigation_id AS record_id, old_status, new_status,
                               changed_by, TO_CHAR(change_timestamp, 'YYYY-MM-DD HH24:MI:SS') AS change_timestamp,
                               change_action AS action_type, NULL AS remarks
                        FROM INVESTIGATION_AUDIT
                    """)
                if not source_table or source_table == "ALERT_AUDIT":
                    union_parts.append("""
                        SELECT audit_id, 'ALERT_AUDIT' AS source_table,
                               alert_id AS record_id, old_status, new_status,
                               changed_by, TO_CHAR(change_timestamp, 'YYYY-MM-DD HH24:MI:SS') AS change_timestamp,
                               'STATUS_UPDATE' AS action_type, remarks
                        FROM ALERT_AUDIT
                    """)

                full_sql = " UNION ALL ".join(union_parts)

                where_clause = "1=1"
                params: Dict[str, Any] = {}
                if search:
                    where_clause = "(TO_CHAR(record_id) LIKE :search OR UPPER(changed_by) LIKE :search OR UPPER(old_status) LIKE :search OR UPPER(new_status) LIKE :search)"
                    params["search"] = f"%{search.upper()}%"

                count_sql = f"SELECT COUNT(*) FROM ({full_sql}) WHERE {where_clause}"
                cur.execute(count_sql, params)
                total = cur.fetchone()[0]

                offset = (page - 1) * page_size
                params["offset"] = offset
                params["limit"] = page_size

                paged_sql = f"""
                    SELECT audit_id, source_table, record_id, old_status, new_status,
                           changed_by, change_timestamp, action_type, remarks
                    FROM ({full_sql})
                    WHERE {where_clause}
                    ORDER BY change_timestamp DESC, audit_id DESC
                    OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
                """
                cur.execute(paged_sql, params)
                rows = cur.fetchall()

                items = []
                for r in rows:
                    items.append({
                        "audit_id": r[0],
                        "source_table": r[1],
                        "record_id": r[2],
                        "old_status": r[3],
                        "new_status": r[4],
                        "changed_by": r[5],
                        "change_timestamp": r[6],
                        "action_type": r[7],
                        "remarks": r[8]
                    })
                return items, total

    @staticmethod
    def get_investigators() -> List[Dict[str, Any]]:
        """Lists directory of investigators."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT investigator_id, first_name, last_name,
                           (first_name || ' ' || last_name) AS full_name,
                           email, department, experience_years, active_status
                    FROM INVESTIGATOR
                    ORDER BY investigator_id
                """)
                return [
                    {
                        "investigator_id": r[0],
                        "first_name": r[1],
                        "last_name": r[2],
                        "full_name": r[3],
                        "email": r[4],
                        "department": r[5],
                        "experience_years": r[6],
                        "active_status": r[7]
                    }
                    for r in cur.fetchall()
                ]

    @staticmethod
    def get_active_accounts() -> List[Dict[str, Any]]:
        """Lists active accounts for transaction creation form dropdown."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT a.account_id, a.account_number, a.account_type, a.balance,
                           c.customer_id, (c.first_name || ' ' || c.last_name) AS customer_name
                    FROM ACCOUNT a
                    JOIN CUSTOMER c ON a.customer_id = c.customer_id
                    WHERE a.status = 'ACTIVE'
                    ORDER BY a.account_id
                """)
                return [
                    {
                        "account_id": r[0],
                        "account_number": r[1],
                        "account_type": r[2],
                        "balance": float(r[3]),
                        "customer_id": r[4],
                        "customer_name": r[5]
                    }
                    for r in cur.fetchall()
                ]

    @staticmethod
    def get_customer_exposure() -> List[Dict[str, Any]]:
        """Surfaces customer fraud risk metrics from VW_CUSTOMER_FRAUD_EXPOSURE view."""
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT customer_id, customer_name, kyc_status, risk_score,
                           total_accounts, total_transacted_volume, total_tx_count, alerts_incurred
                    FROM VW_CUSTOMER_FRAUD_EXPOSURE
                    ORDER BY risk_score DESC
                """)
                return [
                    {
                        "customer_id": r[0],
                        "customer_name": r[1],
                        "kyc_status": r[2],
                        "risk_score": r[3],
                        "total_accounts": r[4],
                        "total_transacted_volume": float(r[5]),
                        "total_tx_count": r[6],
                        "alerts_incurred": r[7]
                    }
                    for r in cur.fetchall()
                ]
