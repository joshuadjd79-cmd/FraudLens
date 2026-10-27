"""
FraudLens: Alert Schemas
"""

from typing import Optional, Literal, List
from enum import Enum
from pydantic import BaseModel
from app.backend.schemas.common import PaginatedData

class SeverityLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class AlertStatus(str, Enum):
    PENDING = "PENDING"
    ESCALATED = "ESCALATED"
    DISMISSED = "DISMISSED"
    RESOLVED = "RESOLVED"

class AlertResponse(BaseModel):
    alert_id: int
    transaction_id: int
    alert_type: str
    severity: str
    rule_triggered: str
    alert_date: str
    status: str
    
    # Associated transaction details
    amount: Optional[float] = None
    channel: Optional[str] = None
    account_number: Optional[str] = None
    customer_name: Optional[str] = None
    has_investigation: Optional[bool] = False
    investigation_id: Optional[int] = None

class AlertListResponse(BaseModel):
    items: List[AlertResponse]
    total: int
    page: int
    page_size: int
    total_pages: int

class AlertFilter(BaseModel):
    severity: Optional[str] = None
    status: Optional[str] = None
    alert_type: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    page_size: int = 10

class AlertStatusUpdate(BaseModel):
    new_status: str
    remarks: Optional[str] = None
