from uuid import UUID

from sqlalchemy import select, func, insert, delete
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import joinedload

from src.application.common.exceptions.common import OffsetNegative, NotFound
from src.application.uncertain.dto.uncertain import UncertainDTO
from src.application.uncertain.dto.user import UserDTO
from src.application.uncertain.interfaces.persistense import (
    IUncertainReader,
    IUncertainRepo,
)
from src.domain.uncertain.models.uncertain import Uncertain
from src.infrastructure.database import models
from src.infrastructure.database.dao.dao import SQLAlchemyDAO


class UncertainReader(SQLAlchemyDAO, IUncertainReader):
    async def get_uncertain(self, uncertain_id: UUID) -> UncertainDTO:
        uncertain = await self.session.scalar(
            select(models.Uncertain)
            .where(models.Uncertain.id == uncertain_id)
            .options(joinedload(models.Uncertain.user))
        )

        if not uncertain:
            raise NotFound

        return map_to_dto(uncertain)

    async def get_uncertains(self, offset: int, limit: int) -> list[UncertainDTO]:
        try:
            uncertains = await self.session.scalars(
                select(models.Uncertain)
                .order_by(models.Uncertain.created_at.desc(), models.Uncertain.name)
                .offset(offset)
                .limit(limit)
                .options(joinedload(models.Uncertain.user))
            )
        except DBAPIError as err:
            raise OffsetNegative from err

        return [map_to_dto(uncertain) for uncertain in uncertains]

    async def get_uncertains_count(self) -> int:
        return await self.session.scalar(select(func.count(models.Uncertain.id)))


class UncertainRepo(SQLAlchemyDAO, IUncertainRepo):
    async def add_uncertain(self, uncertain: Uncertain) -> Uncertain:
        await self.session.execute(
            insert(models.Uncertain).values(
                id=uncertain.id,
                user_id=uncertain.user_id,
                name=uncertain.name,
                surname=uncertain.surname,
                patronymic=uncertain.patronymic,
                birthday=uncertain.birthday,
            )
        )

        return uncertain

    async def get_uncertain(self, uncertain_id: UUID) -> Uncertain:
        uncertain = await self.session.scalar(select(models.Uncertain).where(models.Uncertain.id == uncertain_id))

        return Uncertain(
            id=uncertain.id,
            user_id=uncertain.user_id,
            name=uncertain.name,
            surname=uncertain.surname,
            patronymic=uncertain.patronymic,
            birthday=uncertain.birthday,
        )

    async def delete_uncertain(self, uncertain_id: UUID) -> None:
        await self.session.execute(delete(models.Uncertain).where(models.Uncertain.id == uncertain_id))


def map_to_dto(uncertain: models.Uncertain) -> UncertainDTO:
    return UncertainDTO(
        id=uncertain.id,
        name=uncertain.name,
        surname=uncertain.surname,
        patronymic=uncertain.patronymic,
        birthday=uncertain.birthday,
        user=UserDTO(
            id=uncertain.user.id,
            email=uncertain.user.email,
            timezone=uncertain.user.timezone,
            phone=uncertain.user.phone,
            telegram_id=uncertain.user.telegram_id,
            telegram_username=uncertain.user.telegram_username,
        ),
    )
