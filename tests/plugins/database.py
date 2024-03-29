from __future__ import annotations

import os
from collections.abc import AsyncGenerator, AsyncIterable
from typing import TYPE_CHECKING, cast

import pytest
from sqlalchemy import Connection, text
from sqlalchemy.ext import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker as AsyncSessionmaker  # noqa: N812

import core.impls.alchemy.deps

if TYPE_CHECKING:
    from alembic import config


@pytest.fixture(scope="session")
def database_url() -> str:
    return os.environ["DATABASE_TEST_URL"]


@pytest.fixture(scope="session")
def reuse_db(request: pytest.FixtureRequest) -> bool:
    return cast(bool, request.config.getvalue("reuse_db"))


@pytest.fixture(scope="session")
def sqlalchemy_pytest_database_url(database_url: str, worker_id: str) -> str:
    return f"{database_url}-{worker_id}"


@pytest.fixture(scope="session")
async def _sqlalchemy_create_database(
    database_url: str,
    sqlalchemy_pytest_database_url: str,
) -> AsyncIterable[None]:
    database_name = sqlalchemy_pytest_database_url.rsplit("/")[-1]
    engine = create_async_engine(
        database_url,
        execution_options={"isolation_level": "AUTOCOMMIT"},
    )
    async with engine.connect() as conn:
        exists = await conn.scalar(
            text(
                f"SELECT 1 FROM pg_database WHERE datname='{database_name}'",  # noqa: S608
            ),
        )
        if not exists:
            await conn.execute(text(f'create database "{database_name}";'))
    yield
    async with engine.connect() as conn:
        await conn.execute(
            text(
                f"""
                    select pg_terminate_backend(pg_stat_activity.pid)
                    from pg_stat_activity
                    where pg_stat_activity.datname = '{database_name}'
                    and pid <> pg_backend_pid();
                    """,  # noqa: S608
            ),
        )
        await conn.execute(text(f'drop database "{database_name}";'))


@pytest.fixture(scope="session")
def sqlalchemy_pytest_engine(sqlalchemy_pytest_database_url: str) -> AsyncEngine:
    return create_async_engine(sqlalchemy_pytest_database_url)


@pytest.fixture(scope="session")
def alembic_config() -> config.Config | None:
    from alembic import config

    return config.Config("alembic.ini")


@pytest.fixture(scope="session")
async def _sqlalchemy_run_migrations(
    _sqlalchemy_create_database: None,
    sqlalchemy_pytest_engine: AsyncEngine,
    alembic_config: config.Config | None,
    database_url: str,
) -> None:
    from alembic import command

    if alembic_config is None:
        return

    def run_upgrade(connection: Connection, cfg: config.Config) -> None:
        cfg.attributes["connection"] = connection
        command.upgrade(cfg, revision="head")

    async with sqlalchemy_pytest_engine.begin() as conn:
        alembic_config.set_main_option("sqlalchemy.url", database_url)
        await conn.run_sync(run_upgrade, alembic_config)
        await conn.commit()


@pytest.fixture(scope="session")
def async_sessionmaker() -> asyncio.async_sessionmaker[asyncio.AsyncSession]:
    return core.impls.alchemy.deps.async_session_factory


@pytest.fixture(autouse=True)
async def session(
    _sqlalchemy_run_migrations: None,
    sqlalchemy_pytest_engine: AsyncEngine,
    async_sessionmaker: AsyncSessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    async with sqlalchemy_pytest_engine.connect() as conn:
        transaction = await conn.begin()
        async_sessionmaker.configure(bind=conn)

        async with async_sessionmaker() as session:
            yield session

        if transaction.is_active:
            await transaction.rollback()
