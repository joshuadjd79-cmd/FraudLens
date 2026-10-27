"""
FraudLens: Audit Schemas
"""

from typing import Optional, List
from pydantic import BaseModel

class AuditLogEntry(BaseModel):
    audit_id: int
    source_table: str  # 'INVESTIGATION_AUDIT' or 'ALERT_AUDIT'
    record_id: int    # investigation_id or alert_id
    old_status: Optional[str] = None
    new_status: Optional[str] = None
    changed_by: str
    change_timestamp: str
    action_type: str
    remarks: Optional[str] = None
    table_name: Optional[str] = None
    operation: Optional[str] = None
    db_user: Optional[str] = None

class AuditListResponse(BaseModel):
    items: List[AuditLogEntry]
    total: int
    page: int
    page_size: int
    total_pages: int

class AuditFilter(BaseModel):
    source_table: Optional[str] = None
    action_type: Optional[str] = None
    search: Optional[str] = None
    page: int = 1
    page_size: int = 15
