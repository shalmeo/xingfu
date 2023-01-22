from src.application.user.dto.user import UserDTO
from src.application.user.interfaces.uow import IUserUoW
from src.domain.user.models.user import UserRole


class UserUseCase:
    def __init__(self, uow: IUserUoW):
        self.uow = uow
        

class GetUserByTelegramId(UserUseCase):
    async def __call__(self, telegram_id: int) -> UserDTO:
        return await self.uow.user_reader.get_user_by_telegram_id(telegram_id)