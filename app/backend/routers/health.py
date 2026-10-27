"""
FraudLens: Health & Diagnostics Router
Provides endpoint: /api/health (and /health alias)
"""

from datetime import datetime
from typing import Any, Dict
from fastapi import APIRouter
from app.backend.database.connection import get_db_info
from app.backend.config import settings
from app.backend.schemas.common import ApiResponse

router = APIRouter(tags=["Health & Diagnostics"])


@router.get("/api/health")
@router.get("/health")
def get_health() -> ApiResponse[Dict[str, Any]]:
    """Returns application health, Oracle connectivity, and system metadata."""
    db_status = get_db_info()
    data = {
        "status": "HEALTHY" if db_status["connected"] else "DEGRADED_DEMO_MODE",
        "database_connected": db_status["connected"],
        "database": {
            "connected": db_status["connected"],
            "info": db_status["info"],
            "last_error": db_status["last_error"],
            "active_tables": [
                "CUSTOMERS",
                "ACCOUNTS",
                "TRANSACTIONS",
                "FRAUD_ALERTS",
                "INVESTIGATORS",
                "INVESTIGATIONS",
                "INVESTIGATION_AUDIT",
                "ALERT_AUDIT",
            ],
        },
        "high_amount_threshold": settings.HIGH_AMOUNT_THRESHOLD,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": settings.VERSION,
        "mode": "Live Oracle AI Database 26ai" if db_status["connected"] else "In-Memory Simulation / Demo Mode",
    }
    return ApiResponse.success_response(data=data)
