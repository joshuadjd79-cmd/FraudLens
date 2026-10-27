"""
FraudLens Repository Selector
Dispatches repository calls to live OracleRepository when connected,
or to DemoRepository when in standalone simulation mode.
"""

from app.backend.database.connection import is_oracle_connected
from app.backend.repositories.oracle_repo import OracleRepository
from app.backend.repositories.demo_repo import DemoRepository

def get_repo():
    """Returns the active repository implementation."""
    if is_oracle_connected():
        return OracleRepository
    return DemoRepository

# Alias for consistent naming
get_repository = get_repo

def is_live_mode() -> bool:
    """Returns True if live Oracle database is active."""
    return is_oracle_connected()
