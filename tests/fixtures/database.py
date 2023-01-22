import asyncio
import os
from typing import Callable

import pytest

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
from src.application.task.interfaces.uow import ITaskUoW
from src.application.teacher.interfaces.persistense import ITeacherReader, ITeacherRepo
from src.application.teacher.interfaces.uow import ITeacherUoW
from src.application.undefined.interfaces.persistense import IUndefinedReader, IUndefinedRepo
from src.application.undefined.interfaces.uow import IUndefinedUoW
from src.application.user.interfaces.persistense import IUserRepo
from src.application.user.interfaces.uow import IUserUoW
from src.infrastructure.database.dao.admin import AdminReader, AdminRepo
from src.infrastructure.database.dao.group import GroupReader, GroupRepo
from src.infrastructure.database.dao.student import StudentReader, StudentRepo
from src.infrastructure.database.dao.task import TaskReader
from src.infrastructure.database.dao.teacher import TeacherRepo, TeacherReader
from src.infrastructure.database.dao.undefined import UndefinedReader, UndefinedRepo
from src.infrastructure.database.dao.user import UserRepo
from src.infrastructure.database.init import add_initial_admins
from src.infrastructure.database.models import Base
from src.settings import get_settings


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def container_postgres_url() -> str:
    postgres_container = PostgresContainer("postgres:11")

    if os.name == "nt":
        postgres_container.get_container_host_ip = lambda: "localhost"

    with postgres_container as postgres:
        pg_url = postgres.get_connection_url().replace("psycopg2", "asyncpg")
        yield pg_url


@pytest.fixture(scope="session")
def local_postgres_url() -> str:
    return get_settings().postgres.url


@pytest.fixture(scope="session")
def postgres_url(container_postgres_url) -> str:
    return container_postgres_url


@pytest.fixture(scope="session")
async def session_factory(postgres_url) -> sessionmaker:
    async_engine = create_async_engine(postgres_url)
    sm = sessionmaker(
        async_engine,
        expire_on_commit=False,
        class_=AsyncSession,
        future=True,
        autoflush=False,
    )

    try:
        async with async_engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
            await connection.run_sync(Base.metadata.create_all)

        await add_initial_admins(sm, [123])
        yield sm
    finally:
        await async_engine.dispose()


@pytest.fixture(scope="function")
async def db_session(session_factory) -> AsyncSession:
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()


class FakeSQLAlchemyBaseUoW(IUoW):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.flush()

    async def rollback(self) -> None:
        await self._session.rollback()


class FakeSQLAlchemyUoW(
    FakeSQLAlchemyBaseUoW, IUserUoW, ITeacherUoW, IAdminUoW, IStudentUoW, IGroupUoW, ITaskUoW, IUndefinedUoW
):
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
        undefined_reader: Callable[..., IUndefinedReader],
        undefined_repo: Callable[..., IUndefinedRepo],
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
        self.undefined_reader = undefined_reader(session)
        self.undefined_repo = undefined_repo(session)

        super().__init__(session)


@pytest.fixture()
def uow(db_session) -> FakeSQLAlchemyUoW:
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
        undefined_reader=UndefinedReader,
        undefined_repo=UndefinedRepo,
    )
