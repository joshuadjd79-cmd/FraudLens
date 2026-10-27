"""
FraudLens — Investigations API Router
Endpoint group: /api/investigations & /api/investigators
Provides case docket viewing, investigator assignment via SP_ASSIGN_INVESTIGATOR,
status transitions via SP_UPDATE_INVESTIGATION_STATUS, and case creation.
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from app.backend.repositories import get_repo, is_live_mode
from app.backend.schemas.investigation import (
    InvestigationResponse,
    InvestigationListResponse,
    InvestigationCreateRequest,
    InvestigationAssignRequest,
    InvestigationStatusUpdateRequest,
    InvestigatorResponse,
    InvestigationStatus,
    InvestigationOutcome,
)
from app.backend.schemas.common import ApiResponse

router = APIRouter(prefix="/investigations", tags=["Investigations"])
investigators_router = APIRouter(prefix="/investigators", tags=["Investigators"])


@router.get("", response_model=ApiResponse[InvestigationListResponse])
def get_investigations(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    status: Optional[InvestigationStatus] = Query(None, description="Filter by case status"),
    outcome: Optional[InvestigationOutcome] = Query(None, description="Filter by resolution outcome"),
    search: Optional[str] = Query(None, description="Search by case notes, investigator name, or alert ID"),
):
    """
    Retrieve paginated investigation case dockets with optional status/outcome filtering.
    """
    repo = get_repo()
    items, total = repo.get_investigations(
        page=page,
        page_size=page_size,
        status=status.value if status else None,
        outcome=outcome.value if outcome else None,
        search=search,
    )
    total_pages = (total + page_size - 1) // page_size if total > 0 else 1
    return ApiResponse(
        success=True,
        data=InvestigationListResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        ),
        is_live_oracle=is_live_mode(),
    )


@router.get("/{investigation_id}", response_model=ApiResponse[InvestigationResponse])
def get_investigation_detail(investigation_id: int):
    """
    Retrieve full case docket by investigation ID, including investigator and alert context.
    """
    repo = get_repo()
    case = repo.get_investigation_by_id(investigation_id)
    if not case:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Investigation with ID {investigation_id} not found",
        )
    return ApiResponse(
        success=True,
        data=case,
        is_live_oracle=is_live_mode(),
    )


@router.post("", response_model=ApiResponse[InvestigationResponse], status_code=status.HTTP_201_CREATED)
def create_investigation(payload: InvestigationCreateRequest):
    """
    Open a new investigation case docket for an alert.
    Validates that the alert exists and is not already under active investigation.
    """
    repo = get_repo()
    try:
        case = repo.create_investigation(
            alert_id=payload.alert_id,
            investigator_id=payload.investigator_id,
            notes=payload.notes,
        )
        return ApiResponse(
            success=True,
            data=case,
            message="Investigation case opened successfully",
            is_live_oracle=is_live_mode(),
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        err_msg = str(e)
        if "ORA-00001" in err_msg or "unique constraint" in err_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"An investigation case already exists for Alert ID {payload.alert_id}.",
            )
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=err_msg)


@router.post("/{investigation_id}/assign", response_model=ApiResponse[InvestigationResponse])
def assign_investigator(investigation_id: int, payload: InvestigationAssignRequest):
    """
    Assign an active investigator to this case using PL/SQL stored procedure SP_ASSIGN_INVESTIGATOR.
    Enforces active investigator constraint and updates the case record.
    """
    repo = get_repo()
    try:
        repo.assign_investigator(
            investigation_id=investigation_id,
            investigator_id=payload.investigator_id,
        )
        updated = repo.get_investigation_by_id(investigation_id)
        if not updated:
            raise HTTPException(status_code=404, detail="Investigation not found after assignment")
        return ApiResponse(
            success=True,
            data=updated,
            message="Investigator assigned successfully via SP_ASSIGN_INVESTIGATOR",
            is_live_oracle=is_live_mode(),
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.post("/{investigation_id}/status", response_model=ApiResponse[InvestigationResponse])
def update_investigation_status(investigation_id: int, payload: InvestigationStatusUpdateRequest):
    """
    Transition investigation status using PL/SQL stored procedure SP_UPDATE_INVESTIGATION_STATUS.
    Validates that CLOSED cases must specify a valid outcome (CONFIRMED_FRAUD, FALSE_POSITIVE, INCONCLUSIVE).
    Fires row-level trigger TRG_INVESTIGATION_STATUS_AUDIT to log the change into INVESTIGATION_AUDIT.
    """
    repo = get_repo()
    try:
        if payload.new_status == InvestigationStatus.CLOSED:
            if not payload.outcome or payload.outcome == InvestigationOutcome.PENDING:
                raise ValueError("An outcome must be specified when closing an investigation.")

        repo.update_investigation_status(
            investigation_id=investigation_id,
            new_status=payload.new_status.value,
            outcome=payload.outcome.value if payload.outcome else None,
            notes=payload.notes,
        )
        updated = repo.get_investigation_by_id(investigation_id)
        if not updated:
            raise HTTPException(status_code=404, detail="Investigation not found after status update")
        return ApiResponse(
            success=True,
            data=updated,
            message=f"Investigation status updated to {payload.new_status.value} (Trigger logged audit event)",
            is_live_oracle=is_live_mode(),
        )
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@investigators_router.get("", response_model=ApiResponse[List[InvestigatorResponse]])
def get_investigators(active_only: bool = Query(True, description="Filter for active investigators only")):
    """
    Retrieve list of certified investigators for assignment dropdowns.
    """
    repo = get_repo()
    investigators = repo.get_investigators()
    if active_only:
        investigators = [i for i in investigators if i.get("active_status") == "ACTIVE"]
    return ApiResponse(
        success=True,
        data=investigators,
        is_live_oracle=is_live_mode(),
    )
