from uuid import UUID

from sqlalchemy import select, func, insert, delete
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import joinedload

from src.application.common.exceptions.common import OffsetNegative, NotFound
from src.application.undefined.dto.undefined import UndefinedDTO
from src.application.undefined.dto.user import UserDTO
from src.application.undefined.interfaces.persistense import (
    IUndefinedReader,
    IUndefinedRepo,
)
from src.domain.undefined.models.undefined import Undefined
from src.infrastructure.database import models
from src.infrastructure.database.dao.dao import SQLAlchemyDAO


class UndefinedReader(SQLAlchemyDAO, IUndefinedReader):
    async def get_undefined(self, undefined_id: UUID) -> UndefinedDTO:
        undefined = await self.session.scalar(
            select(models.Undefined)
            .where(models.Undefined.id == undefined_id)
            .options(joinedload(models.Undefined.user))
        )

        if not undefined:
            raise NotFound

        return map_to_dto(undefined)

    async def get_undefineds(self, offset: int, limit: int) -> list[UndefinedDTO]:
        try:
            undefineds = await self.session.scalars(
                select(models.Undefined)
                .order_by(models.Undefined.created_at.desc(), models.Undefined.name)
                .offset(offset)
                .limit(limit)
                .options(joinedload(models.Undefined.user))
            )
        except DBAPIError as err:
            raise OffsetNegative from err

        return [map_to_dto(undefined) for undefined in undefineds]

    async def get_undefineds_count(self) -> int:
        return await self.session.scalar(select(func.count(models.Undefined.id)))


class UndefinedRepo(SQLAlchemyDAO, IUndefinedRepo):
    async def add_undefined(self, undefined: Undefined) -> Undefined:
        await self.session.execute(
            insert(models.Undefined).values(
                id=undefined.id,
                user_id=undefined.user_id,
                name=undefined.name,
                surname=undefined.surname,
                patronymic=undefined.patronymic,
                birthday=undefined.birthday,
            )
        )

        return undefined

    async def get_undefined(self, undefined_id: UUID) -> Undefined:
        undefined = await self.session.scalar(select(models.Undefined).where(models.Undefined.id == undefined_id))

        return Undefined(
            id=undefined.id,
            user_id=undefined.user_id,
            name=undefined.name,
            surname=undefined.surname,
            patronymic=undefined.patronymic,
            birthday=undefined.birthday,
        )

    async def delete_undefined(self, undefined_id: UUID) -> None:
        await self.session.execute(delete(models.Undefined).where(models.Undefined.id == undefined_id))


def map_to_dto(undefined: models.Undefined) -> UndefinedDTO:
    return UndefinedDTO(
        id=undefined.id,
        name=undefined.name,
        surname=undefined.surname,
        patronymic=undefined.patronymic,
        birthday=undefined.birthday,
        user=UserDTO(
            id=undefined.user.id,
            email=undefined.user.email,
            timezone=undefined.user.timezone,
            phone=undefined.user.phone,
            telegram_id=undefined.user.telegram_id,
            telegram_username=undefined.user.telegram_username,
        ),
    )
