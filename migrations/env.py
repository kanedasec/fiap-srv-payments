from logging.config import fileConfig
import os
from sqlalchemy import engine_from_config, pool
from alembic import context

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

from src.adapters.db.base import Base
from src.adapters.db import models  # noqa: F401
target_metadata = Base.metadata

db_url = os.getenv("DATABASE_URL") or config.get_main_option("sqlalchemy.url")
if not db_url or db_url.startswith("${"):
    db_url = "postgresql+psycopg://postgres:postgres@localhost:5434/payments_db"
config.set_main_option("sqlalchemy.url", db_url)

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(config.get_section(config.config_ini_section, {}), prefix="sqlalchemy.", poolclass=pool.NullPool)
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
