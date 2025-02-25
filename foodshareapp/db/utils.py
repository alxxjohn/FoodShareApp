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
    f"{settings.db_host}:{settings.db_port}/{settings.db_base}",
    ssl=settings.db_ssl_enable,
)


redis_db = redis.Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    db=settings.rd_db,
    password=settings.redis_password,
)


async def commit_transaction(transaction: Transaction):
    if transaction._connection and getattr(
        transaction._connection, "_transaction_stack", None
    ):
        await transaction.commit()


async def rollback_transaction(transaction: Transaction):
    if transaction._connection and getattr(
        transaction._connection, "_transaction_stack", None
    ):
        await transaction.rollback()


async def db_transaction() -> AsyncIterator[Transaction]:
    transaction = db.transaction()
    await transaction.start()
    try:
        yield transaction
        await commit_transaction(transaction)
    except Exception as e:
        logger.error(f"Transaction error: {e}", exc_info=True)
        await rollback_transaction(transaction)
