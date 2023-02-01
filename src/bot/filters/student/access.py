from aiogram.filters import BaseFilter
from src.application.user.dto.user import UserDTO

from src.domain.user.models.user import UserRole


class StudentAccessFilter(BaseFilter):
    async def __call__(self, _, user: UserDTO) -> bool:
        return user.role == UserRole.STUDENT
