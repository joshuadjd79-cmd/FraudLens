"""
FraudLens: Oracle Database Connection & Pool Management
Uses official python-oracledb driver in Thin Mode.
Provides connection pooling, health checks, and safe context management.
"""

import logging
from contextlib import contextmanager
from typing import Optional, Dict, Any
import oracledb
from app.backend.config import settings

logger = logging.getLogger("fraudlens.database")

_pool: Optional[oracledb.ConnectionPool] = None
_oracle_available: bool = False
_last_error: Optional[str] = None
_db_info: Dict[str, Any] = {}

def init_db_pool() -> bool:
    """Initializes the Oracle Connection Pool using thin mode."""
    global _pool, _oracle_available, _last_error, _db_info
    try:
        logger.info(f"Connecting to Oracle Database at {settings.ORACLE_DSN} as {settings.ORACLE_USER}...")
        _pool = oracledb.create_pool(
            user=settings.ORACLE_USER,
            password=settings.ORACLE_PASSWORD,
            dsn=settings.ORACLE_DSN,
            min=settings.ORACLE_POOL_MIN,
            max=settings.ORACLE_POOL_MAX,
            increment=1
        )
        
        # Test connection & retrieve metadata
        with _pool.acquire() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT banner FROM v$version WHERE ROWNUM = 1")
                banner_row = cur.fetchone()
                banner = banner_row[0] if banner_row else "Oracle Database"
                
                cur.execute("""
                    SELECT SYS_CONTEXT('USERENV', 'CON_NAME') AS con_name,
                           SYS_CONTEXT('USERENV', 'SESSION_USER') AS session_user,
                           SYS_CONTEXT('USERENV', 'DB_NAME') AS db_name
                    FROM DUAL
                """)
                ctx = cur.fetchone()
                
                _db_info = {
                    "version": banner,
                    "container": ctx[0] if ctx else "FREEPDB1",
                    "user": ctx[1] if ctx else settings.ORACLE_USER,
                    "db_name": ctx[2] if ctx else "FREE",
                    "dsn": settings.ORACLE_DSN,
                    "mode": "Oracle Thin Driver (Native)"
                }
                
        _oracle_available = True
        _last_error = None
        logger.info(f"Oracle Connection Pool successfully initialized: {_db_info['container']} / {_db_info['user']}")
        return True
    except Exception as e:
        _oracle_available = False
        _last_error = str(e)
        logger.warning(f"Oracle connection failed ({e}). Application will run in Demo/Fallback Mode.")
        return False

def close_db_pool():
    """Closes the connection pool on application shutdown."""
    global _pool, _oracle_available
    if _pool:
        try:
            _pool.close()
            logger.info("Oracle Connection Pool closed.")
        except Exception as e:
            logger.error(f"Error closing Oracle pool: {e}")
        finally:
            _pool = None
            _oracle_available = False

def is_oracle_connected() -> bool:
    """Returns True if live Oracle pool is active."""
    return _oracle_available

def check_oracle_health() -> Dict[str, Any]:
    """Returns a health summary dictionary indicating if Oracle is reachable."""
    return {
        "healthy": _oracle_available,
        "details": _db_info if _oracle_available else None,
        "error": _last_error
    }

def get_db_info() -> Dict[str, Any]:
    """Returns safe database diagnostic information."""
    return {
        "connected": _oracle_available,
        "info": _db_info if _oracle_available else {
            "version": "In-Memory Demonstration Engine",
            "container": "STANDALONE_DEMO",
            "user": "DEMO_USER",
            "db_name": "DEMODB",
            "dsn": "simulated://in-memory",
            "mode": "Simulation / Fallback"
        },
        "last_error": _last_error
    }

@contextmanager
def get_db_connection():
    """Context manager for acquiring and releasing Oracle connections safely."""
    global _pool, _oracle_available, _last_error
    if not _oracle_available or not _pool:
        raise ConnectionError("Oracle database is not connected.")
    
    conn = None
    try:
        conn = _pool.acquire()
        yield conn
    except Exception as e:
        if conn:
            try:
                conn.rollback()
            except Exception:
                pass
        raise e
    finally:
        if conn and _pool:
            try:
                _pool.release(conn)
            except Exception:
                pass
