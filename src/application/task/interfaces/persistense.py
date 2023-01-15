from typing import Protocol
from uuid import UUID

from src.application.task.dto.task import TaskDTO


class ITaskReader(Protocol):
    async def get_task(self, task_id: UUID) -> TaskDTO:
        ...

    async def get_group_tasks(
        self, group_id: UUID, offset: int, limit: int
    ) -> list[TaskDTO]:
        ...

    async def get_group_tasks_count(self, group_id: UUID) -> int:
        ...
