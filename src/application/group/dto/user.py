from datetime import datetime
from typing import Optional

from src.application.common.dto.common import DTO


class UserDTO(DTO):
    created_at: datetime
    id: int
    phone: Optional[int]
    telegram_id: Optional[int]

    @property
    def unique_code(self):
        telegram_id = str(self.telegram_id)[-4:] if self.telegram_id else "0000"
        phone = str(self.phone)[-4:] if self.phone else "0000"
        return (
            f"{self.created_at.year}-{self.created_at.month}-{self.created_at.day}-"
            f"{self.created_at.time().hour}{self.created_at.time().minute}-"
            f"{telegram_id}-{phone}-{self.id}"
        )
