from uuid import UUID

from src.application.task.dto.task import TaskDTO
from src.application.task.interfaces.uow import ITaskUoW


class TaskUseCase:
    def __init__(self, uow: ITaskUoW):
        self.uow = uow


class GetTask(TaskUseCase):
    async def __call__(self, task_id: UUID) -> TaskDTO:
        return await self.uow.task_reader.get_task(task_id)


class GetGroupTasks(TaskUseCase):
    async def __call__(self, group_id: UUID, offset: int, limit: int) -> list[TaskDTO]:
        return await self.uow.task_reader.get_group_tasks(group_id, offset, limit)


class GetGroupTasksCount(TaskUseCase):
    async def __call__(self, group_id: UUID) -> int:
        return await self.uow.task_reader.get_group_tasks_count(group_id)
