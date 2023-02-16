import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parent.parent.parent.parent))
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from plants_api.config.app_settings_global import app_settings
from plants_api.db import DeclarativeBase
from plants_api.db.entities import *  # noqa

config = context.config
section = config.config_ini_section

config.set_section_option(section, "POSTGRES_DB", app_settings.db_name)
config.set_section_option(section, "POSTGRES_HOST", app_settings.db_addr)
config.set_section_option(section, "POSTGRES_USER", app_settings.db_user)
config.set_section_option(section, "POSTGRES_PASSWORD", app_settings.db_pass)
config.set_section_option(section, "POSTGRES_PORT", str(app_settings.db_port))


fileConfig(config.config_file_name, disable_existing_loggers=False)
target_metadata = DeclarativeBase.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
