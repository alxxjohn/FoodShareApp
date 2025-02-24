import logging
from typing import Any, AsyncIterator, Mapping

import redis
from databases import Database
from databases.core import Transaction as Transaction


from foodshareapp.settings import settings

logger = logging.getLogger(__name__)


Record = Mapping[Any, Any]

db = Database(
    f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@"
    f":{settings.db_port}/{settings.db_base}?host={settings.db_host}",
    ssl=settings.db_ssl_enable,
)

redis_db = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.rd_db,
    password=settings.redis_password,
)


async def db_transaction() -> AsyncIterator[Transaction]:
    """Dependency which starts and yields a new DB `transaction`.
    In order to persist any queries executed with the transaction,
    the route handler must call `transaction.commit()` before returning a response.
    Any unhandled exceptions raised before calling `db.commit()` will cause the
    transaction to roll back.
    """

    transaction = db.transaction()
    await transaction.start()
    try:
        yield transaction
    finally:
        try:
            await transaction.rollback()
        except IndexError as e:
            logger.warn("--- DB Transaction ERROR ---")
            logger.warn(e)
            logger.warn("--- DB Transaction ERROR ---")
            # Unfortunately, Databases.core.Transaction fails in a very messy way
            # if the transaction was already committed/rolled back.
            pass
