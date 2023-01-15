from uuid import UUID

from sqlalchemy import select, delete, insert, update, func
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import joinedload

from src.application.admin.dto.user import UserDTO
from src.application.common.exceptions.common import NotFound, OffsetNegative
from src.application.admin.interfaces.persistense import IAdminReader, IAdminRepo
from src.domain.admin.models.admin import Admin
from src.domain.user.models.user import UserRole
from src.infrastructure.database import models
from src.infrastructure.database.dao.dao import SQLAlchemyDAO
from src.application.admin.dto.admin import AdminDTO


class AdminReader(SQLAlchemyDAO, IAdminReader):
    async def _admin(self, admin_id: UUID) -> models.Admin:
        return await self.session.get(
            models.Admin,
            admin_id,
            options=[
                joinedload(models.Admin.user),
                joinedload(models.Admin.animal),
            ],
        )

    async def get_admin(self, admin_id) -> AdminDTO:
        admin = await self._admin(admin_id)

        if not admin:
            raise NotFound

        return map_to_dto(admin)

    async def get_admins(self, offset: int, limit: int) -> list[AdminDTO]:
        try:
            admins = await self.session.scalars(
                select(models.Admin)
                .join(models.User)
                .where(models.User.role == UserRole.ADMIN)
                .offset(offset)
                .limit(limit)
                .order_by(models.Admin.created_at.desc(), models.Admin.name)
                .options(
                    joinedload(models.Admin.user),
                    joinedload(models.Admin.animal),
                )
            )
        except DBAPIError as err:
            raise OffsetNegative from err

        return [map_to_dto(admin) for admin in admins]

    async def get_all(self) -> list[AdminDTO]:
        admins = await self.session.scalars(
            select(models.Admin).options(
                joinedload(models.Admin.user),
                joinedload(models.Admin.animal),
            )
        )

        return [map_to_dto(admin) for admin in admins]

    async def get_admins_count(self):
        return await self.session.scalar(select(func.count(models.Admin.id)))


class AdminRepo(SQLAlchemyDAO, IAdminRepo):
    async def get_admin(self, admin_id: UUID) -> Admin:
        admin = await self.session.scalar(
            select(models.Admin).where(models.Admin.id == admin_id)
        )

        return Admin(
            id=admin.id,
            user_id=admin.user_id,
            name=admin.name,
            surname=admin.surname,
            patronymic=admin.patronymic,
            birthday=admin.birthday,
            level=admin.level,
            description=admin.description,
        )

    async def delete_admin(self, admin_id: UUID) -> None:
        await self.session.execute(
            delete(models.Admin).where(models.Admin.id == admin_id)
        )

    async def add_admin(self, admin: Admin) -> Admin:
        await self.session.execute(
            insert(models.Admin).values(
                id=admin.id,
                user_id=admin.user_id,
                name=admin.name,
                surname=admin.surname,
                patronymic=admin.patronymic,
                birthday=admin.birthday,
                level=admin.level,
                description=admin.description,
            )
        )

        return admin

    async def update_admin(self, admin: Admin) -> Admin:
        await self.session.execute(
            update(models.Admin)
            .where(models.Admin.id == admin.id)
            .values(
                name=admin.name,
                surname=admin.surname,
                patronymic=admin.patronymic,
                birthday=admin.birthday,
                level=admin.level,
                description=admin.description,
                access_start=admin.access_start,
                access_end=admin.access_end,
            )
        )

        return admin


def map_to_dto(admin: models.Admin):
    return AdminDTO(
        id=admin.id,
        name=admin.name,
        surname=admin.surname,
        patronymic=admin.patronymic,
        level=admin.level,
        description=admin.description,
        access_start=admin.access_start,
        access_end=admin.access_end,
        animal=admin.animal.name if admin.animal else None,
        birthday=admin.birthday,
        user=UserDTO(
            created_at=admin.user.created_at,
            id=admin.user.id,
            phone=admin.user.phone,
            telegram_id=admin.user.telegram_id,
            telegram_username=admin.user.telegram_username,
            timezone=admin.user.timezone,
            email=admin.user.email,
        ),
    )
