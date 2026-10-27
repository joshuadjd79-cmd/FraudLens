"""
FraudLens: Investigation & Investigator Schemas
"""

from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field

class InvestigationStatus(str, Enum):
    OPEN = "OPEN"
    UNDER_REVIEW = "UNDER REVIEW"
    CLOSED = "CLOSED"

class InvestigationOutcome(str, Enum):
    CONFIRMED_FRAUD = "CONFIRMED_FRAUD"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    INCONCLUSIVE = "INCONCLUSIVE"
    PENDING = "PENDING"

class InvestigatorResponse(BaseModel):
    investigator_id: int
    first_name: str
    last_name: str
    full_name: str
    email: str
    department: str
    experience_years: int
    active_status: str

class InvestigationResponse(BaseModel):
    investigation_id: int
    alert_id: int
    investigator_id: Optional[int] = None
    investigator_name: Optional[str] = "UNASSIGNED"
    investigator_dept: Optional[str] = None
    start_date: str
    end_date: Optional[str] = None
    status: str
    outcome: str
    notes: Optional[str] = None
    
    # Associated alert & transaction details
    alert_type: Optional[str] = None
    severity: Optional[str] = None
    rule_triggered: Optional[str] = None
    transaction_id: Optional[int] = None
    amount: Optional[float] = None
    channel: Optional[str] = None
    account_number: Optional[str] = None
    customer_name: Optional[str] = None
    closed_at: Optional[str] = None

class InvestigationListResponse(BaseModel):
    items: List[InvestigationResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class InvestigationCreateRequest(BaseModel):
    alert_id: int
    investigator_id: Optional[int] = None
    notes: Optional[str] = None

# Aliases
InvestigationCreate = InvestigationCreateRequest

class InvestigationAssignRequest(BaseModel):
    investigator_id: int = Field(..., description="Active Investigator ID (e.g. 301, 302, 303)")

# Aliases
InvestigationAssign = InvestigationAssignRequest

class InvestigationStatusUpdateRequest(BaseModel):
    new_status: InvestigationStatus
    outcome: Optional[InvestigationOutcome] = None
    notes: Optional[str] = None

# Aliases
InvestigationUpdateStatus = InvestigationStatusUpdateRequest

class InvestigationFilter(BaseModel):
    status: Optional[str] = None
    outcome: Optional[str] = None
    investigator_id: Optional[int] = None
    search: Optional[str] = None
    page: int = 1
    page_size: int = 10
