from typing import Protocol
from src.application.user.dto.user import UserDTO
from src.domain.user.models.user import User, UserRole

class IUserReader(Protocol):
    async def get_user_by_telegram_id(self, telegram_id: int) -> UserDTO:
        ...
    
        
class IUserRepo(Protocol):
    async def get_user(self, user_id: int) -> User:
        ...

    async def add_user(self, user: User) -> User:
        ...

    async def update_user(self, user: User) -> User:
        ...

    async def delete_user(self, user_id: int) -> None:
        ...
