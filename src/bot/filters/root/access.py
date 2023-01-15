from aiogram.types import User
from aiogram.filters import BaseFilter


class RootAccessFilter(BaseFilter):
    async def __call__(
        self,
        _,
        event_from_user: User,
        bot_admins: list[int],
    ) -> bool:
        return event_from_user.id in bot_admins
