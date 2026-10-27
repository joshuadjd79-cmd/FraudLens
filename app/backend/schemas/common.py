"""
FraudLens: Common API Schemas
"""

from typing import Generic, TypeVar, Optional, List, Any
from pydantic import BaseModel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: Optional[str] = None
    is_live_oracle: bool = True

    @classmethod
    def success_response(cls, data: Any = None, message: Optional[str] = None, is_live_oracle: bool = True):
        return cls(success=True, data=data, message=message, is_live_oracle=is_live_oracle)

    @classmethod
    def error_response(cls, message: str, is_live_oracle: bool = True):
        return cls(success=False, data=None, message=message, is_live_oracle=is_live_oracle)

class PaginatedData(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int

class SystemHealthResponse(BaseModel):
    status: str
    database_connected: bool
    database: Optional[dict] = None
    database_info: Optional[dict] = None
    timestamp: str
    version: str
    high_amount_threshold: Optional[float] = 50000.0
