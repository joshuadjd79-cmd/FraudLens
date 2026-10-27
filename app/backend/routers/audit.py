"""
FraudLens — Audit Trail API Router
Endpoint group: /api/audit
Provides query endpoints for database trigger-generated audit trails:
- INVESTIGATION_AUDIT (populated by TRG_INVESTIGATION_STATUS_AUDIT)
- ALERT_AUDIT (populated by TRG_FRAUD_ALERT_AUDIT)
"""

from typing import Optional
from fastapi import APIRouter, Query

from app.backend.repositories import get_repo, is_live_mode
from app.backend.schemas.audit import AuditListResponse
from app.backend.schemas.common import ApiResponse

router = APIRouter(prefix="/audit", tags=["Audit Trail"])


@router.get("", response_model=ApiResponse[AuditListResponse])
def get_audit_trail(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(15, ge=1, le=100, description="Items per page"),
    table_name: Optional[str] = Query(None, description="Filter by table name: INVESTIGATION_AUDIT or ALERT_AUDIT"),
    search: Optional[str] = Query(None, description="Search by ID, action, user, or status"),
):
    """
    Retrieve trigger-generated audit records tracking row-level mutations.
    """
    repo = get_repo()
    items, total = repo.get_audit_logs(
        page=page,
        page_size=page_size,
        source_table=table_name,
        search=search,
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return ApiResponse(
        success=True,
        data=AuditListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        ),
        is_live_oracle=is_live_mode(),
    )
