from alembic import context
from sqlalchemy import create_engine
from foodshareapp.settings import settings

DATABASE_URL = f"postgresql+psycopg2://{settings.db_user}:{settings.db_pass}@{settings.db_host}:{settings.db_port}/{settings.db_base}"
engine = create_engine(DATABASE_URL)


config = context.config
target_metadata = None


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode using SQLAlchemy sync engine."""
    connectable = engine
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
