from typing import Optional

from src.application.common.dto.common import DTO


class UserDTO(DTO):
    id: int
    email: str
    timezone: str
    phone: Optional[int]

    telegram_id: Optional[int]
    telegram_username: Optional[str]
