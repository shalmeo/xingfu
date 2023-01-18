from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, types

from src.application.user.interfaces.uow import IUserUoW
from src.application.user.usecases.user import GetUserRole


class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[types.Update, dict[str, Any]], Awaitable[Any]],
        event: types.Update,
        data: dict[str, Any],
    ) -> Any:
        event_from_user = data["event_from_user"]
        if event_from_user:
            from_user_id = event_from_user.id
            uow: IUserUoW = data["uow"]
            user = await GetUserRole(uow=uow)(int(from_user_id))
            data["user_role"] = user

        return await handler(event, data)