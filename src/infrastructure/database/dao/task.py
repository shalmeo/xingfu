from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.exc import DBAPIError

from src.application.common.exceptions.common import OffsetNegative
from src.application.task.dto.task import TaskDTO
from src.application.task.interfaces.persistense import ITaskReader
from src.infrastructure.database import models
from src.infrastructure.database.dao.dao import SQLAlchemyDAO


class TaskReader(SQLAlchemyDAO, ITaskReader):
    async def get_task(self, task_id: UUID) -> TaskDTO:
        task = await self.session.scalar(
            select(models.Task).where(models.Task.id == task_id)
        )

        return map_to_dto(task)

    async def get_group_tasks(
        self, group_id: UUID, offset: int, limit: int
    ) -> list[TaskDTO]:
        try:
            tasks = await self.session.scalars(
                select(models.Task)
                .where(models.Task.group_id == group_id)
                .order_by(models.Task.created_at.desc(), models.Task.title)
                .offset(offset)
                .limit(limit)
            )
        except DBAPIError as err:
            raise OffsetNegative from err

        return [map_to_dto(task) for task in tasks]

    async def get_group_tasks_count(self, group_id: UUID) -> int:
        return await self.session.scalar(
            select(func.count(models.Task.id)).where(models.Task.group_id == group_id)
        )


def map_to_dto(task: models.Task) -> TaskDTO:
    return TaskDTO(
        id=task.id,
        group_id=task.group_id,
        title=task.title,
        lesson_date=task.lesson_date,
        deadline=task.deadline,
        description=task.description,
    )
