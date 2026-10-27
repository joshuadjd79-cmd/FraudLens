"""
FraudLens: In-Memory Demo Repository Fallback
Provides an exact clone of repository operations for offline environments or unit testing.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from app.backend.database import mock_data
from app.backend.config import settings

class DemoRepository:
    
    @staticmethod
    def get_dashboard_summary() -> Dict[str, Any]:
        tx_count = len(mock_data.TRANSACTIONS)
        tx_volume = sum(t["amount"] for t in mock_data.TRANSACTIONS)
        flagged_tx = sum(1 for t in mock_data.TRANSACTIONS if t["status"] == "FLAGGED")
        alert_count = len(mock_data.FRAUD_ALERTS)
        pending_alerts = sum(1 for a in mock_data.FRAUD_ALERTS if a["status"] == "PENDING")
        critical_alerts = sum(1 for a in mock_data.FRAUD_ALERTS if a["severity"] == "CRITICAL")
        open_inv = sum(1 for i in mock_data.INVESTIGATIONS if i["status"] == "OPEN")
        under_review_inv = sum(1 for i in mock_data.INVESTIGATIONS if i["status"] == "UNDER REVIEW")
        closed_inv = sum(1 for i in mock_data.INVESTIGATIONS if i["status"] == "CLOSED")
        confirmed_fraud = sum(1 for i in mock_data.INVESTIGATIONS if i["outcome"] == "CONFIRMED_FRAUD")
        active_investigators = sum(1 for inv in mock_data.INVESTIGATORS if inv["active_status"] == "ACTIVE")
        
        return {
            "total_transactions": tx_count,
            "total_volume_inr": tx_volume,
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
        date_map = {}
        for t in mock_data.TRANSACTIONS:
            d = t["transaction_date"][:10]
            if d not in date_map:
                date_map[d] = {"date": d, "total_volume": 0.0, "tx_count": 0, "flagged_count": 0}
            date_map[d]["total_volume"] += t["amount"]
            date_map[d]["tx_count"] += 1
            if t["status"] == "FLAGGED":
                date_map[d]["flagged_count"] += 1
        return sorted(list(date_map.values()), key=lambda x: x["date"])

    @staticmethod
    def get_channel_metrics() -> List[Dict[str, Any]]:
        channel_map = {}
        for t in mock_data.TRANSACTIONS:
            ch = t["channel"]
            if ch not in channel_map:
                channel_map[ch] = {"channel": ch, "total_tx": 0, "total_volume": 0.0}
            channel_map[ch]["total_tx"] += 1
            channel_map[ch]["total_volume"] += t["amount"]
        result = []
        for ch, data in channel_map.items():
            result.append({
                "channel": ch,
                "total_tx": data["total_tx"],
                "total_volume": data["total_volume"],
                "avg_ticket": round(data["total_volume"] / data["total_tx"], 2) if data["total_tx"] > 0 else 0
            })
        return sorted(result, key=lambda x: x["total_volume"], reverse=True)

    @staticmethod
    def get_severity_breakdown() -> List[Dict[str, Any]]:
        counts = {}
        for a in mock_data.FRAUD_ALERTS:
            sev = a["severity"]
            counts[sev] = counts.get(sev, 0) + 1
        return [{"severity": k, "count": v} for k, v in counts.items()]

    @staticmethod
    def get_outcome_breakdown() -> List[Dict[str, Any]]:
        counts = {}
        for i in mock_data.INVESTIGATIONS:
            outc = i["outcome"]
            counts[outc] = counts.get(outc, 0) + 1
        return [{"outcome": k, "count": v} for k, v in counts.items()]

    @staticmethod
    def get_transactions(page=1, page_size=10, **filters) -> Tuple[List[Dict[str, Any]], int]:
        all_tx = []
        acc_dict = {a["account_id"]: a for a in mock_data.ACCOUNTS}
        cust_dict = {c["customer_id"]: c for c in mock_data.CUSTOMERS}
        alert_dict = {a["transaction_id"]: a for a in mock_data.FRAUD_ALERTS}

        for t in sorted(mock_data.TRANSACTIONS, key=lambda x: x["transaction_id"], reverse=True):
            acc = acc_dict.get(t["account_id"], {})
            cust = cust_dict.get(acc.get("customer_id"), {})
            alt = alert_dict.get(t["transaction_id"])
            
            # Apply filters
            if filters.get("account_id") and t["account_id"] != filters["account_id"]:
                continue
            if filters.get("channel") and t["channel"] != filters["channel"]:
                continue
            if filters.get("transaction_type") and t["transaction_type"] != filters["transaction_type"]:
                continue
            if filters.get("status") and t["status"] != filters["status"]:
                continue
            if filters.get("min_amount") is not None and t["amount"] < filters["min_amount"]:
                continue
            if filters.get("max_amount") is not None and t["amount"] > filters["max_amount"]:
                continue
            if filters.get("search"):
                s = filters["search"].lower()
                cname = f"{cust.get('first_name','')} {cust.get('last_name','')}".lower()
                if (s not in str(t["transaction_id"]) and 
                    s not in (t.get("description") or "").lower() and
                    s not in acc.get("account_number", "").lower() and
                    s not in cname):
                    continue

            all_tx.append({
                "transaction_id": t["transaction_id"],
                "account_id": t["account_id"],
                "account_number": acc.get("account_number", "N/A"),
                "customer_id": cust.get("customer_id"),
                "customer_name": f"{cust.get('first_name', '')} {cust.get('last_name', '')}".strip() or "N/A",
                "transaction_type": t["transaction_type"],
                "amount": t["amount"],
                "transaction_date": t["transaction_date"],
                "channel": t["channel"],
                "status": t["status"],
                "counterparty_account": t.get("counterparty_account"),
                "description": t.get("description"),
                "alert_generated": bool(alt),
                "alert_id": alt["alert_id"] if alt else None,
                "rule_triggered": alt["rule_triggered"] if alt else None
            })

        total = len(all_tx)
        start = (page - 1) * page_size
        return all_tx[start:start + page_size], total

    @staticmethod
    def get_transaction_by_id(tx_id: int) -> Optional[Dict[str, Any]]:
        tx_list, _ = DemoRepository.get_transactions(page=1, page_size=1, search=str(tx_id))
        for t in tx_list:
            if t["transaction_id"] == tx_id:
                return t
        return None

    @staticmethod
    def create_transaction(account_id: int, transaction_type: str, amount: float, channel: str, counterparty_account=None, description=None):
        new_id = max([t["transaction_id"] for t in mock_data.TRANSACTIONS], default=50000) + 1
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "FLAGGED" if amount > settings.HIGH_AMOUNT_THRESHOLD else "COMPLETED"
        
        new_tx = {
            "transaction_id": new_id,
            "account_id": account_id,
            "transaction_type": transaction_type,
            "amount": amount,
            "transaction_date": now_str,
            "channel": channel,
            "status": status,
            "counterparty_account": counterparty_account,
            "description": description or f"Payment via {channel}"
        }
        mock_data.TRANSACTIONS.append(new_tx)
        
        alert_id = None
        rule_desc = None
        if amount > settings.HIGH_AMOUNT_THRESHOLD:
            alert_id = max([a["alert_id"] for a in mock_data.FRAUD_ALERTS], default=7000) + 1
            rule_desc = f"Rule 101: Transaction amount {amount:,.2f} INR exceeds {settings.HIGH_AMOUNT_THRESHOLD:,.0f} threshold"
            new_alert = {
                "alert_id": alert_id,
                "transaction_id": new_id,
                "alert_type": "HIGH_AMOUNT",
                "severity": "HIGH",
                "rule_triggered": rule_desc,
                "alert_date": now_str,
                "status": "PENDING"
            }
            mock_data.FRAUD_ALERTS.append(new_alert)

        return DemoRepository.get_transaction_by_id(new_id)

    @staticmethod
    def get_alerts(page=1, page_size=10, **filters) -> Tuple[List[Dict[str, Any]], int]:
        all_alerts = []
        tx_dict = {t["transaction_id"]: t for t in mock_data.TRANSACTIONS}
        acc_dict = {a["account_id"]: a for a in mock_data.ACCOUNTS}
        cust_dict = {c["customer_id"]: c for c in mock_data.CUSTOMERS}
        inv_dict = {i["alert_id"]: i for i in mock_data.INVESTIGATIONS}

        for a in sorted(mock_data.FRAUD_ALERTS, key=lambda x: x["alert_id"], reverse=True):
            if filters.get("severity") and a["severity"] != filters["severity"]:
                continue
            if filters.get("status") and a["status"] != filters["status"]:
                continue
            if filters.get("alert_type") and a["alert_type"] != filters["alert_type"]:
                continue
            if filters.get("search"):
                s = filters["search"].lower()
                if s not in str(a["alert_id"]) and s not in a["rule_triggered"].lower() and s not in str(a["transaction_id"]):
                    continue

            tx = tx_dict.get(a["transaction_id"], {})
            acc = acc_dict.get(tx.get("account_id"), {})
            cust = cust_dict.get(acc.get("customer_id"), {})
            inv = inv_dict.get(a["alert_id"])

            all_alerts.append({
                "alert_id": a["alert_id"],
                "transaction_id": a["transaction_id"],
                "alert_type": a["alert_type"],
                "severity": a["severity"],
                "rule_triggered": a["rule_triggered"],
                "alert_date": a["alert_date"],
                "status": a["status"],
                "amount": tx.get("amount", 0.0),
                "channel": tx.get("channel", "N/A"),
                "account_number": acc.get("account_number", "N/A"),
                "customer_name": f"{cust.get('first_name', '')} {cust.get('last_name', '')}".strip() or "N/A",
                "has_investigation": bool(inv),
                "investigation_id": inv["investigation_id"] if inv else None
            })

        total = len(all_alerts)
        start = (page - 1) * page_size
        return all_alerts[start:start + page_size], total

    @staticmethod
    def get_alert_by_id(alert_id: int) -> Optional[Dict[str, Any]]:
        items, _ = DemoRepository.get_alerts(page=1, page_size=100)
        for item in items:
            if item["alert_id"] == alert_id:
                return item
        return None

    @staticmethod
    def get_investigations(page=1, page_size=10, **filters) -> Tuple[List[Dict[str, Any]], int]:
        all_inv = []
        alert_dict = {a["alert_id"]: a for a in mock_data.FRAUD_ALERTS}
        tx_dict = {t["transaction_id"]: t for t in mock_data.TRANSACTIONS}
        acc_dict = {a["account_id"]: a for a in mock_data.ACCOUNTS}
        cust_dict = {c["customer_id"]: c for c in mock_data.CUSTOMERS}
        invr_dict = {i["investigator_id"]: i for i in mock_data.INVESTIGATORS}

        for inv in sorted(mock_data.INVESTIGATIONS, key=lambda x: x["investigation_id"], reverse=True):
            if filters.get("status") and inv["status"] != filters["status"]:
                continue
            if filters.get("outcome") and inv["outcome"] != filters["outcome"]:
                continue
            if filters.get("investigator_id") and inv.get("investigator_id") != filters["investigator_id"]:
                continue
            if filters.get("search"):
                s = filters["search"].lower()
                if s not in str(inv["investigation_id"]) and s not in (inv.get("notes") or "").lower():
                    continue

            alt = alert_dict.get(inv["alert_id"], {})
            tx = tx_dict.get(alt.get("transaction_id"), {})
            acc = acc_dict.get(tx.get("account_id"), {})
            cust = cust_dict.get(acc.get("customer_id"), {})
            invr = invr_dict.get(inv.get("investigator_id"))

            all_inv.append({
                "investigation_id": inv["investigation_id"],
                "alert_id": inv["alert_id"],
                "investigator_id": inv.get("investigator_id"),
                "investigator_name": f"{invr['first_name']} {invr['last_name']}" if invr else "UNASSIGNED",
                "investigator_dept": invr.get("department") if invr else None,
                "start_date": inv["start_date"],
                "end_date": inv.get("end_date"),
                "status": inv["status"],
                "outcome": inv["outcome"],
                "notes": inv.get("notes"),
                "alert_type": alt.get("alert_type"),
                "severity": alt.get("severity"),
                "rule_triggered": alt.get("rule_triggered"),
                "transaction_id": alt.get("transaction_id"),
                "amount": tx.get("amount", 0.0),
                "channel": tx.get("channel"),
                "account_number": acc.get("account_number"),
                "customer_name": f"{cust.get('first_name', '')} {cust.get('last_name', '')}".strip() or "N/A"
            })

        total = len(all_inv)
        start = (page - 1) * page_size
        return all_inv[start:start + page_size], total

    @staticmethod
    def get_investigation_by_id(investigation_id: int) -> Optional[Dict[str, Any]]:
        items, _ = DemoRepository.get_investigations(page=1, page_size=100)
        for item in items:
            if item["investigation_id"] == investigation_id:
                return item
        return None

    @staticmethod
    def create_investigation(alert_id: int, investigator_id=None, notes=None):
        new_id = max([i["investigation_id"] for i in mock_data.INVESTIGATIONS], default=9000) + 1
        now_date = datetime.now().strftime("%Y-%m-%d")
        
        new_inv = {
            "investigation_id": new_id,
            "alert_id": alert_id,
            "investigator_id": investigator_id,
            "start_date": now_date,
            "end_date": None,
            "status": "OPEN",
            "outcome": "PENDING",
            "notes": notes or "Case docket opened via Web Application"
        }
        mock_data.INVESTIGATIONS.append(new_inv)
        
        # Log to audit
        mock_data.INVESTIGATION_AUDITS.append({
            "audit_id": len(mock_data.INVESTIGATION_AUDITS) + 1,
            "investigation_id": new_id,
            "old_status": None,
            "new_status": "OPEN",
            "changed_by": "WEB_USER",
            "change_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "change_action": "CASE_CREATED"
        })
        
        # Update alert status to ESCALATED
        for a in mock_data.FRAUD_ALERTS:
            if a["alert_id"] == alert_id:
                a["status"] = "ESCALATED"
                break
                
        items, _ = DemoRepository.get_investigations(page=1, page_size=1, search=str(new_id))
        return items[0] if items else new_inv

    @staticmethod
    def assign_investigator(investigation_id: int, investigator_id: int) -> bool:
        # Check if investigator is active
        invr = next((i for i in mock_data.INVESTIGATORS if i["investigator_id"] == investigator_id), None)
        if not invr:
            raise ValueError(f"Investigator ID {investigator_id} does not exist.")
        if invr["active_status"] != "ACTIVE":
            raise ValueError(f"Investigator {invr['first_name']} {invr['last_name']} (ID {investigator_id}) is INACTIVE.")

        for inv in mock_data.INVESTIGATIONS:
            if inv["investigation_id"] == investigation_id:
                inv["investigator_id"] = investigator_id
                if inv["status"] == "OPEN":
                    inv["status"] = "UNDER REVIEW"
                    mock_data.INVESTIGATION_AUDITS.append({
                        "audit_id": len(mock_data.INVESTIGATION_AUDITS) + 1,
                        "investigation_id": investigation_id,
                        "old_status": "OPEN",
                        "new_status": "UNDER REVIEW",
                        "changed_by": "WEB_USER",
                        "change_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "change_action": "ASSIGNED_INVESTIGATOR"
                    })
                return True
        raise ValueError(f"Investigation ID {investigation_id} not found.")

    @staticmethod
    def update_investigation_status(investigation_id: int, new_status: str, outcome: Optional[str] = None, notes: Optional[str] = None) -> bool:
        new_status = new_status.upper().strip()
        if new_status not in ['OPEN', 'UNDER REVIEW', 'CLOSED']:
            raise ValueError(f"Invalid status: {new_status}")
            
        for inv in mock_data.INVESTIGATIONS:
            if inv["investigation_id"] == investigation_id:
                old_status = inv["status"]
                if new_status == "CLOSED":
                    if not outcome or outcome not in ['CONFIRMED_FRAUD', 'FALSE_POSITIVE', 'INCONCLUSIVE']:
                        raise ValueError("Closing a case requires a definitive outcome (CONFIRMED_FRAUD, FALSE_POSITIVE, or INCONCLUSIVE).")
                    inv["outcome"] = outcome
                    inv["end_date"] = datetime.now().strftime("%Y-%m-%d")
                
                inv["status"] = new_status
                if notes:
                    inv["notes"] = notes

                mock_data.INVESTIGATION_AUDITS.append({
                    "audit_id": len(mock_data.INVESTIGATION_AUDITS) + 1,
                    "investigation_id": investigation_id,
                    "old_status": old_status,
                    "new_status": new_status,
                    "changed_by": "WEB_USER",
                    "change_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "change_action": "STATUS_TRANSITION"
                })
                return True
        raise ValueError(f"Investigation ID {investigation_id} not found.")

    @staticmethod
    def get_audit_logs(page=1, page_size=15, source_table=None, search=None) -> Tuple[List[Dict[str, Any]], int]:
        combined = []
        for a in mock_data.INVESTIGATION_AUDITS:
            combined.append({
                "audit_id": a["audit_id"],
                "source_table": "INVESTIGATION_AUDIT",
                "record_id": a["investigation_id"],
                "old_status": a.get("old_status"),
                "new_status": a["new_status"],
                "changed_by": a["changed_by"],
                "change_timestamp": a["change_timestamp"],
                "action_type": a["change_action"],
                "remarks": None
            })
        for a in mock_data.ALERT_AUDITS:
            combined.append({
                "audit_id": a["audit_id"],
                "source_table": "ALERT_AUDIT",
                "record_id": a["alert_id"],
                "old_status": a.get("old_status"),
                "new_status": a["new_status"],
                "changed_by": a["changed_by"],
                "change_timestamp": a["change_timestamp"],
                "action_type": "STATUS_UPDATE",
                "remarks": a.get("remarks")
            })
            
        if source_table:
            combined = [c for c in combined if c["source_table"] == source_table]
        if search:
            s = search.lower()
            combined = [c for c in combined if s in str(c["record_id"]) or s in c["changed_by"].lower() or s in (c.get("new_status") or "").lower()]

        total = len(combined)
        start = (page - 1) * page_size
        return sorted(combined, key=lambda x: x["change_timestamp"], reverse=True)[start:start + page_size], total

    @staticmethod
    def get_investigators() -> List[Dict[str, Any]]:
        return [
            {
                "investigator_id": i["investigator_id"],
                "first_name": i["first_name"],
                "last_name": i["last_name"],
                "full_name": f"{i['first_name']} {i['last_name']}",
                "email": i["email"],
                "department": i["department"],
                "experience_years": i["experience_years"],
                "active_status": i["active_status"]
            }
            for i in mock_data.INVESTIGATORS
        ]

    @staticmethod
    def get_active_accounts() -> List[Dict[str, Any]]:
        cust_map = {c["customer_id"]: c for c in mock_data.CUSTOMERS}
        return [
            {
                "account_id": a["account_id"],
                "account_number": a["account_number"],
                "account_type": a["account_type"],
                "balance": a["balance"],
                "customer_id": a["customer_id"],
                "customer_name": f"{cust_map.get(a['customer_id'], {}).get('first_name', '')} {cust_map.get(a['customer_id'], {}).get('last_name', '')}".strip()
            }
            for a in mock_data.ACCOUNTS if a["status"] == "ACTIVE"
        ]

    @staticmethod
    def get_customer_exposure() -> List[Dict[str, Any]]:
        results = []
        for c in mock_data.CUSTOMERS:
            cid = c["customer_id"]
            accs = [a for a in mock_data.ACCOUNTS if a["customer_id"] == cid]
            acc_ids = [a["account_id"] for a in accs]
            txs = [t for t in mock_data.TRANSACTIONS if t["account_id"] in acc_ids]
            tx_ids = [t["transaction_id"] for t in txs]
            alts = [a for a in mock_data.FRAUD_ALERTS if a["transaction_id"] in tx_ids]
            results.append({
                "customer_id": cid,
                "customer_name": f"{c['first_name']} {c['last_name']}",
                "kyc_status": c["kyc_status"],
                "risk_score": c["risk_score"],
                "total_accounts": len(accs),
                "total_transacted_volume": sum(t["amount"] for t in txs),
                "total_tx_count": len(txs),
                "alerts_incurred": len(alts)
            })
        return sorted(results, key=lambda x: x["risk_score"], reverse=True)
