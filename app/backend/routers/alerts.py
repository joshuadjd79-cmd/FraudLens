"""
FraudLens — Alerts API Router
Endpoint group: /api/alerts
Provides alert listing, search, filtering by severity and status, and single-record retrieval.
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.backend.repositories import get_repo, is_live_mode
from app.backend.schemas.alert import AlertResponse, AlertListResponse, SeverityLevel, AlertStatus
from app.backend.schemas.common import ApiResponse

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.get("", response_model=ApiResponse[AlertListResponse])
def get_alerts(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    severity: Optional[SeverityLevel] = Query(None, description="Filter by severity level"),
    status: Optional[AlertStatus] = Query(None, description="Filter by alert status"),
    search: Optional[str] = Query(None, description="Search by transaction ID, reason, or rule name"),
):
    """
    Retrieve paginated fraud alerts with optional filtering by severity, status, and keyword search.
    """
    repo = get_repo()
    items, total = repo.get_alerts(
        page=page,
        page_size=page_size,
        severity=severity.value if severity else None,
        status=status.value if status else None,
        search=search,
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return ApiResponse(
        success=True,
        data=AlertListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        ),
        is_live_oracle=is_live_mode(),
    )


@router.get("/{alert_id}", response_model=ApiResponse[AlertResponse])
def get_alert_detail(alert_id: int):
    """
    Retrieve detailed information for a specific alert, including linked transaction details.
    """
    repo = get_repo()
    alert = repo.get_alert_by_id(alert_id)
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Alert with ID {alert_id} not found",
        )
    return ApiResponse(
        success=True,
        data=alert,
        is_live_oracle=is_live_mode(),
    )
