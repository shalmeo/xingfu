from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.providers.session import session_provider
from src.application.common.interfaces.uow import IUoW
from src.infrastructure.database.dao.admin import AdminReader, AdminRepo
from src.infrastructure.database.dao.group import GroupReader, GroupRepo
from src.infrastructure.database.dao.student import StudentReader, StudentRepo
from src.infrastructure.database.dao.task import TaskReader
from src.infrastructure.database.dao.teacher import TeacherReader, TeacherRepo
from src.infrastructure.database.dao.uncertain import UncertainReader, UncertainRepo
from src.infrastructure.database.dao.user import UserReader, UserRepo
from src.infrastructure.uow import SQLAlchemyUoW


def uow_provider() -> IUoW:
    ...


def uow(session: AsyncSession = Depends(session_provider)) -> SQLAlchemyUoW:
    return SQLAlchemyUoW(
        session,
        user_reader=UserReader,
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
