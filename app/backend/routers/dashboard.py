"""
FraudLens: Dashboard Executive Router
"""

from fastapi import APIRouter
from app.backend.repositories import get_repo, is_live_mode
from app.backend.schemas.common import ApiResponse
from app.backend.schemas.dashboard import DashboardSummary

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=ApiResponse[DashboardSummary])
def get_summary():
    """Returns database-backed executive KPI metrics."""
    repo = get_repo()
    summary_data = repo.get_dashboard_summary()
    return ApiResponse(
        success=True,
        data=summary_data,
        is_live_oracle=is_live_mode()
    )

@router.get("/trends")
def get_trends():
    """Returns daily transaction and flagged volume trends."""
    repo = get_repo()
    trends = repo.get_transaction_trends()
    return ApiResponse(
        success=True,
        data=trends,
        is_live_oracle=is_live_mode()
    )
