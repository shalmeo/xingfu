from typing import Callable

from sqlalchemy.ext.asyncio import AsyncSession

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
from src.application.uncertain.interfaces.persistense import (
    IUncertainReader,
    IUncertainRepo,
)
from src.application.uncertain.interfaces.uow import IUncertainUoW
from src.application.user.interfaces.persistense import IUserRepo
from src.application.user.interfaces.uow import IUserUoW


class SQLAlchemyBaseUoW(IUoW):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()


class SQLAlchemyUoW(
    SQLAlchemyBaseUoW,
    IUserUoW,
    ITeacherUoW,
    IAdminUoW,
    IStudentUoW,
    IGroupUoW,
    ITaskUoW,
    IUncertainUoW,
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
