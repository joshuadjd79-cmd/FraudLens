"""
FraudLens: Dashboard & Analytics Schemas
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class DashboardSummary(BaseModel):
    total_transactions: int
    total_volume_inr: float
    flagged_transactions: int
    total_alerts: int
    pending_alerts: int
    critical_alerts: int
    open_investigations: int
    under_review_investigations: int
    closed_investigations: int
    confirmed_fraud_cases: int
    active_investigators: int
    high_amount_threshold: float

class TrendItem(BaseModel):
    date: str
    total_volume: float
    tx_count: int
    flagged_count: int

class ChannelVolume(BaseModel):
    channel: str
    total_tx: int
    total_volume: float
    avg_ticket: float

class SeverityBreakdown(BaseModel):
    severity: str
    count: int

class OutcomeBreakdown(BaseModel):
    outcome: str
    count: int

class CustomerExposure(BaseModel):
    customer_id: int
    customer_name: str
    kyc_status: str
    risk_score: int
    total_accounts: int
    total_transacted_volume: float
    total_tx_count: int
    alerts_incurred: int
