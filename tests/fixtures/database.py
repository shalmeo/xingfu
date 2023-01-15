import asyncio
import os
from typing import Callable

import pytest
import alembic.config
from alembic import command
from alembic.script import ScriptDirectory

from sqlalchemy import event
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from src.application.admin.interfaces.persistense import IAdminReader, IAdminRepo
from src.application.admin.interfaces.uow import IAdminUoW
from src.application.common.interfaces.uow import IUoW
from src.application.group.interfaces.persistense import IGroupReader, IGroupRepo
from src.application.group.interfaces.uow import IGroupUoW
from src.application.student.interfaces.persistense import IStudentReader, IStudentRepo
from src.application.student.interfaces.uow import IStudentUoW
from src.application.task.interfaces.persistense import ITaskReader
from src.application.teacher.interfaces.persistense import ITeacherReader, ITeacherRepo
from src.application.teacher.interfaces.uow import ITeacherUoW
from src.application.uncertain.interfaces.persistense import IUncertainReader, IUncertainRepo
from src.application.user.interfaces.persistense import IUserRepo
from src.application.user.interfaces.uow import IUserUoW
from src.infrastructure.database.dao.admin import AdminReader, AdminRepo
from src.infrastructure.database.dao.group import GroupReader, GroupRepo
from src.infrastructure.database.dao.student import StudentReader, StudentRepo
from src.infrastructure.database.dao.task import TaskReader
from src.infrastructure.database.dao.teacher import TeacherRepo, TeacherReader
from src.infrastructure.database.dao.uncertain import UncertainReader, UncertainRepo
from src.infrastructure.database.dao.user import UserRepo


@pytest.fixture(scope="session")
def container_postgres_url() -> str:
    postgres_container = PostgresContainer("postgres:11")

    if os.name == "nt":
        postgres_container.get_container_host_ip = lambda: "localhost"

    with postgres_container as postgres:
        pg_url = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        yield pg_url


@pytest.fixture()
def uow(db_session) -> "FakeSQLAlchemyUoW":
    return FakeSQLAlchemyUoW(
        db_session,
        user_repo=UserRepo,
        teacher_reader=TeacherReader,
        teacher_repo=TeacherRepo,
        admin_reader=AdminReader,
        admin_repo=AdminRepo,
        student_reader=StudentReader,
        student_repo=StudentRepo,
        group_reader=GroupReader,
        group_repo=GroupRepo,
        task_reader=TaskReader,
        uncertain_reader=UncertainReader,
        uncertain_repo=UncertainRepo,
    )


@pytest.fixture(scope="session")
def session_factory(container_postgres_url):
    engine = create_async_engine(container_postgres_url, echo=True)
    sm = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
        future=True,
        autoflush=False,
    )
    return sm


@pytest.fixture(scope="session")
def db_wipe(session_factory):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    loop.run_until_complete(wipe_db(session_factory))
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def test_db(session_factory, container_postgres_url, db_wipe) -> None:
    cfg = alembic.config.Config()
    cfg.set_main_option("script_location", "src/infrastructure/database/migrations")
    cfg.set_main_option("sqlalchemy.url", container_postgres_url)

    revisions_dir = ScriptDirectory.from_config(cfg)

    # Get & sort migrations, from first to last
    revisions = list(revisions_dir.walk_revisions())
    revisions.reverse()
    for revision in revisions:
        command.upgrade(cfg, revision.revision)
        command.downgrade(cfg, revision.down_revision or "-1")
        command.upgrade(cfg, revision.revision)


@pytest.fixture(scope="function")
async def db_session(session_factory, container_postgres_url) -> AsyncSession:
    async with create_async_engine(container_postgres_url).connect() as connect:
        transaction = await connect.begin()
        async_session: AsyncSession = session_factory(bind=connect)
        await async_session.begin_nested()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def reopen_nested_transaction(*_):
            if connect.closed:
                return

            if not connect.in_nested_transaction():
                connect.sync_connection.begin_nested()

        yield async_session
        await async_session.close()
        if transaction.is_active:
            await transaction.rollback()


async def wipe_db(session_factory, schema: str = "public") -> None:
    async with session_factory() as session:
        await session.execute(f"DROP SCHEMA IF EXISTS {schema} CASCADE;")
        await session.commit()
        await session.execute(f"CREATE SCHEMA {schema};")
        await session.commit()


class FakeSQLAlchemyBaseUoW(IUoW):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.flush()

    async def rollback(self) -> None:
        await self._session.rollback()


class FakeSQLAlchemyUoW(FakeSQLAlchemyBaseUoW, IUserUoW, ITeacherUoW, IAdminUoW, IStudentUoW, IGroupUoW):
    def __init__(
        self,
        session: AsyncSession,
        user_repo: Callable[..., IUserRepo],
        teacher_reader: Callable[..., ITeacherReader],
        teacher_repo: Callable[..., ITeacherRepo],
        admin_reader: Callable[..., IAdminReader],
        admin_repo: Callable[..., IAdminRepo],
        student_reader: Callable[..., IStudentReader],
        student_repo: Callable[..., IStudentRepo],
        group_reader: Callable[..., IGroupReader],
        group_repo: Callable[..., IGroupRepo],
        task_reader: Callable[..., ITaskReader],
        uncertain_reader: Callable[..., IUncertainReader],
        uncertain_repo: Callable[..., IUncertainRepo],
    ):
        self.user_repo = user_repo(session)
        self.teacher_reader = teacher_reader(session)
        self.teacher_repo = teacher_repo(session)
        self.admin_reader = admin_reader(session)
        self.admin_repo = admin_repo(session)
        self.student_reader = student_reader(session)
        self.student_repo = student_repo(session)
        self.group_reader = group_reader(session)
        self.group_repo = group_repo(session)
        self.task_reader = task_reader(session)
        self.uncertain_reader = uncertain_reader(session)
        self.uncertain_repo = uncertain_repo(session)

        super().__init__(session)
