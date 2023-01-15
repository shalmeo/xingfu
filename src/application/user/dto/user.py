from datetime import datetime
from typing import Optional

from src.application.common.dto.common import DTO
from src.domain.user.models.user import UserRole


class UserDTO(DTO):
    created_at: datetime

    id: int
    email: str
    timezone: str
    phone: Optional[int]
    role: UserRole

    telegram_id: Optional[int]
    telegram_username: Optional[str]

    @property
    def unique_code(self):
        telegram_id = str(self.telegram_id)[-4:] if self.telegram_id else "0000"
        phone = str(self.phone)[-4:] if self.phone else "0000"
        return (
            f"{self.created_at.year}-{self.created_at.month}-{self.created_at.day}-"
            f"{self.created_at.time().hour}{self.created_at.time().minute}-"
            f"{telegram_id}-{phone}-{self.id}"
        )


class UserCreateDTO(DTO):
    email: str
    timezone: str
    phone: Optional[int]
    role: UserRole

    telegram_id: Optional[int]
    telegram_username: Optional[str]


class UserUpdateDTO(DTO):
    email: str
    timezone: str
    phone: Optional[int]
    role: UserRole

    telegram_id: Optional[int]
    telegram_username: Optional[str]
