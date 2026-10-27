"""
FraudLens — Analytics & Reporting API Router
Endpoint group: /api/analytics
Provides aggregate metrics, channel comparisons, risk distributions,
and exposure reports backed by SQL aggregation and Oracle views.
"""

from typing import Any, Dict, List
from fastapi import APIRouter

from app.backend.repositories import get_repo, is_live_mode
from app.backend.schemas.common import ApiResponse

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=ApiResponse[Dict[str, Any]])
def get_analytics_summary():
    """
    Get consolidated high-level analytics for reports and executive view.
    """
    repo = get_repo()
    summary = repo.get_dashboard_summary()
    trends = repo.get_transaction_trends()
    channels = repo.get_channel_metrics()
    severities = repo.get_severity_breakdown()
    outcomes = repo.get_outcome_breakdown()
    return ApiResponse(
        success=True,
        data={
            "kpis": summary,
            "channel_breakdown": channels,
            "severity_breakdown": severities,
            "outcome_breakdown": outcomes,
            "timeline": trends,
        },
        is_live_oracle=is_live_mode(),
    )


@router.get("/customer-exposure", response_model=ApiResponse[List[Dict[str, Any]]])
def get_customer_exposure():
    """
    Query customer risk exposure data backed by the Oracle view VW_CUSTOMER_FRAUD_EXPOSURE.
    Aggregates transactions, alerts, and total exposure value per customer.
    """
    repo = get_repo()
    data = repo.get_customer_exposure()
    return ApiResponse(
        success=True,
        data=data,
        is_live_oracle=is_live_mode(),
    )
