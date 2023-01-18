from aiogram.filters import BaseFilter

from src.domain.user.models.user import UserRole


class StudentAccessFilter(BaseFilter):
    async def __call__(
        self,
        _,
        user_role: UserRole
    ) -> bool:
        return user_role == UserRole.STUDENT