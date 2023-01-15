from datetime import date, datetime
from typing import Optional
from uuid import UUID

from src.application.common.dto.common import DTO


class TaskDTO(DTO):
    id: UUID
    group_id: UUID

    title: str
    lesson_date: Optional[date]
    deadline: datetime
    description: str
