from psycopg_pool import AsyncConnectionPool
from app.common.config import settings

_pool: AsyncConnectionPool | None = None

def init_pool():
    global _pool
    _pool = AsyncConnectionPool(conninfo=settings.DATABASE_URL, open=False)

def get_pool() -> AsyncConnectionPool:
    if _pool is None:
        raise RuntimeError("Connection pool is not initialized. Call init_pool() first.")
    return _pool
