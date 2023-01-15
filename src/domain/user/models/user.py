from enum import Enum
from typing import Optional

from src.domain.common.models.entity import Entity


class UserRole(Enum):
    ADMIN = "ADMIN"
    TEACHER = "TEACHER"
    STUDENT = "STUDENT"
    ROOT = "ROOT"
    UNCERTAIN = "UNCERTAIN"
    PARENT = "PARENT"


class User(Entity):
    id: Optional[int]
    email: str
    phone: Optional[int]
    timezone: str
    role: UserRole
    telegram_id: Optional[int]
    telegram_username: Optional[str]

    def change_own_role(self, user_role: UserRole):
        self.role = user_role
