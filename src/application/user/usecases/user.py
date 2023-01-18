from src.application.user.interfaces.uow import IUserUoW
from src.domain.user.models.user import UserRole


class UserUseCase:
    async def __init__(self, uow: IUserUoW):
        self.uow = uow
        

class GetUserRole(UserUseCase):
    async def __call__(self, user_id: int) -> UserRole:
        return await self.uow.user_reader.get_user_role(user_id)