from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from src.domain.common.models.entity import Entity


class Undefined(Entity):
    id: UUID = Field(default_factory=uuid4)
    user_id: Optional[int]
    name: str
    surname: str
    patronymic: Optional[str]
    birthday: date
