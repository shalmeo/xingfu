from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.orm import sessionmaker

from src.infrastructure.database.dao.admin import AdminReader, AdminRepo
from src.infrastructure.database.dao.group import GroupReader, GroupRepo
from src.infrastructure.database.dao.student import StudentReader, StudentRepo
from src.infrastructure.database.dao.task import TaskReader
from src.infrastructure.database.dao.teacher import TeacherReader, TeacherRepo
from src.infrastructure.database.dao.uncertain import UncertainReader, UncertainRepo
from src.infrastructure.database.dao.user import UserRepo
from src.infrastructure.uow import SQLAlchemyUoW


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_maker: sessionmaker) -> None:
        self.session_maker = session_maker

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:
        async with self.session_maker() as session:
            data["session"] = session
            data["uow"] = SQLAlchemyUoW(
                session,
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
            await handler(event, data)
            data.pop("session")
            data.pop("uow")
