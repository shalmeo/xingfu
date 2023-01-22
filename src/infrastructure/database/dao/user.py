from sqlalchemy import insert, literal_column, update, select, delete
from src.application.common.exceptions.common import NotFound

from src.application.user.dto.user import UserDTO
from src.application.user.interfaces.persistense import IUserRepo, IUserReader
from src.domain.user.models.user import User, UserRole
from src.infrastructure.database import models
from src.infrastructure.database.dao.dao import SQLAlchemyDAO

class UserReader(SQLAlchemyDAO, IUserReader):
    async def get_user_by_telegram_id(self, telegram_id: int) -> UserDTO:
        user = await self.session.scalar(select(models.User).where(models.User.telegram_id == telegram_id))
        
        if not user:
            raise NotFound
        
        return map_to_dto(user)
    
        
class UserRepo(SQLAlchemyDAO, IUserRepo):
    async def get_user(self, user_id: int) -> User:
        user = await self.session.scalar(
            select(models.User).where(models.User.id == user_id)
        )

        return User(
            id=user.id,
            email=user.email,
            phone=user.phone,
            timezone=user.timezone,
            role=user.role,
            telegram_id=user.telegram_id,
            telegram_username=user.telegram_username,
        )

    async def add_user(self, user: User) -> User:
        id = await self.session.execute(
            insert(models.User)
            .values(
                email=user.email,
                phone=user.phone,
                timezone=user.timezone,
                role=user.role,
                telegram_id=user.telegram_id,
                telegram_username=user.telegram_username,
            )
            .returning(literal_column("id"))
        )

        user.id = id.scalar()

        return user

    async def update_user(self, user: User) -> User:
        user_update = (
            update(models.User)
            .where(models.User.id == user.id)
            .values(
                email=user.email,
                phone=user.phone,
                timezone=user.timezone,
                telegram_id=user.telegram_id,
                telegram_username=user.telegram_username,
                role=user.role,
            )
        )

        await self.session.execute(user_update)

        return user

    async def delete_user(self, user_id: int) -> None:
        await self.session.execute(delete(models.User).where(models.User.id == user_id))


def map_to_dto(user: models.User) -> UserDTO:
    return UserDTO(
        created_at=user.created_at,
        id=user.id,
        email=user.email,
        timezone=user.timezone,
        phone=user.phone,
        role=user.role,
        telegram_id=user.telegram_id,
        telegram_username=user.telegram_username,
    )
