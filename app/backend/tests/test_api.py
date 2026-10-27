"""
FraudLens Automated API Test Suite
Covers:
- Root and health endpoints
- Dashboard summary & trend metrics
- Transaction listing, pagination, and negative validation
- Normal transaction creation (under ₹50,000 threshold)
- High-amount transaction creation (exceeds ₹50,000 threshold, triggers alert)
- Transaction CSV export
- Alert filtering and detail lookup
- Investigation creation, assignment, and status progression
- Mandatory outcome check on closed cases
- Trigger-logged audit trail retrieval
- Demo scenario automated execution
"""

import pytest
from fastapi.testclient import TestClient
from app.backend.main import app


@pytest.fixture(scope="module")
def client():
    """Initializes TestClient with app lifespan to start database pooling."""
    with TestClient(app) as test_client:
        yield test_client


def test_root_endpoint(client):
    """Verify root landing endpoint status and database mode."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    assert "version" in data
    assert "database_mode" in data


def test_health_endpoint(client):
    """Verify /api/health returns detailed system and database diagnostics."""
    response = client.get("/api/health")
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    data = res_json["data"]
    assert data["status"] in ("HEALTHY", "DEGRADED_DEMO_MODE")
    assert "database" in data
    assert "active_tables" in data["database"]
    assert "high_amount_threshold" in data


def test_dashboard_summary(client):
    """Verify executive dashboard summary returns KPIs and breakdowns."""
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    data = res_json["data"]
    assert "total_transactions" in data
    assert "total_volume_inr" in data
    assert "flagged_transactions" in data
    assert "total_alerts" in data


def test_dashboard_trends(client):
    """Verify time-series trend data for charts."""
    response = client.get("/api/dashboard/trends")
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    assert isinstance(res_json["data"], list)


def test_transactions_pagination(client):
    """Verify transactions table pagination and search."""
    response = client.get("/api/transactions?page=1&page_size=5")
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    data = res_json["data"]
    assert len(data["items"]) <= 5
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert data["total"] >= len(data["items"])


def test_transaction_negative_amount_validation(client):
    """Verify server rejects zero or negative transaction amounts."""
    payload = {
        "account_id": 1001,
        "tx_type": "UPI",
        "amount": -500.0,
        "channel": "MOBILE_APP",
    }
    response = client.post("/api/transactions", json=payload)
    assert response.status_code == 422  # Pydantic validation error


def test_create_normal_transaction(client):
    """
    Test creating a normal transaction under ₹50,000 threshold.
    Should succeed and NOT generate an alert.
    """
    payload = {
        "account_id": 2001,
        "transaction_type": "TRANSFER",
        "amount": 2500.0,
        "channel": "MOBILE_APP",
        "counterparty_account": "ACT-TEST-001",
        "description": "Standard utility bill payment",
    }
    response = client.post("/api/transactions", json=payload)
    assert response.status_code == 201
    res_json = response.json()
    assert res_json["success"] is True
    data = res_json["data"]
    assert data["amount"] == 2500.0
    assert data["alert_generated"] is False


def test_create_high_amount_transaction_triggers_alert(client):
    """
    Test creating a high-amount transaction exceeding ₹50,000 threshold.
    Should trigger SP_EVALUATE_AND_ALERT_TRANSACTION or business rule alert.
    """
    payload = {
        "account_id": 2002,
        "transaction_type": "TRANSFER",
        "amount": 85000.0,
        "channel": "NET_BANKING",
        "counterparty_account": "ACT-TEST-HIGH-01",
        "description": "High value business supplier payment",
    }
    response = client.post("/api/transactions", json=payload)
    assert response.status_code == 201
    res_json = response.json()
    assert res_json["success"] is True
    data = res_json["data"]
    assert data["amount"] == 85000.0
    assert data["alert_generated"] is True


def test_transactions_csv_export(client):
    """Verify CSV export endpoint returns text/csv content."""
    response = client.get("/api/transactions/export/csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers.get("content-type", "")
    assert "Transaction ID,Account ID" in response.text


def test_alerts_list_and_filter(client):
    """Verify alerts endpoint filtering and pagination."""
    response = client.get("/api/alerts?page=1&page_size=10")
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    data = res_json["data"]
    assert len(data["items"]) >= 1


def test_investigators_list(client):
    """Verify active investigators directory."""
    response = client.get("/api/investigators?active_only=true")
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    assert len(res_json["data"]) >= 1


def test_investigations_lifecycle(client):
    """
    Test full case lifecycle:
    1. Create case docket
    2. Assign certified investigator (301)
    3. Transition status to CLOSED with outcome CONFIRMED_FRAUD
    """
    # Find an alert or open investigation to test
    res_alerts = client.get("/api/alerts?page=1&page_size=20")
    alerts = res_alerts.json()["data"]["items"] if res_alerts.status_code == 200 else []

    inv_id = None
    for a in alerts:
        res_create = client.post("/api/investigations", json={
            "alert_id": a["alert_id"],
            "investigator_id": None,
            "notes": "Automated integration test docket",
        })
        if res_create.status_code == 201:
            inv_id = res_create.json()["data"]["investigation_id"]
            break

    if not inv_id:
        res_invs = client.get("/api/investigations?page=1&page_size=10")
        active_invs = [inv for inv in res_invs.json()["data"]["items"] if inv["status"] != "CLOSED"]
        inv_id = active_invs[0]["investigation_id"] if active_invs else 9001

    # Assign active investigator 301
    assign_payload = {"investigator_id": 301}
    res_assign = client.post(f"/api/investigations/{inv_id}/assign", json=assign_payload)
    assert res_assign.status_code == 200

    # Status update with required outcome
    status_payload = {
        "new_status": "CLOSED",
        "outcome": "CONFIRMED_FRAUD",
        "notes": "Resolution confirmed via test suite.",
    }
    res_status = client.post(f"/api/investigations/{inv_id}/status", json=status_payload)
    assert res_status.status_code == 200
    data = res_status.json()["data"]
    assert data["status"] == "CLOSED"
    assert data["outcome"] == "CONFIRMED_FRAUD"


def test_investigation_closed_without_outcome_rejected(client):
    """Verify business rule: CLOSED investigations MUST specify an outcome."""
    status_payload = {
        "new_status": "CLOSED",
        "outcome": None,
        "notes": "Invalid close attempt without outcome",
    }
    res = client.post("/api/investigations/9004/status", json=status_payload)
    assert res.status_code == 400
    assert "outcome must be specified" in res.json()["detail"].lower()


def test_audit_trail_retrieval(client):
    """Verify audit trail endpoint queries trigger logs."""
    response = client.get("/api/audit?page=1&page_size=10")
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    data = res_json["data"]
    assert "items" in data


def test_demo_scenario_runner(client):
    """Verify automated college demo scenario end-to-end runner."""
    response = client.post("/api/demo/run-scenario")
    assert response.status_code == 200
    res_json = response.json()
    assert res_json["success"] is True
    data = res_json["data"]
    assert data["step1_normal_tx"]["alert_generated"] is False
    assert data["step2_high_amount_tx"]["alert_generated"] is True
    assert data["step6_case_closed"]["status"] == "CLOSED"
