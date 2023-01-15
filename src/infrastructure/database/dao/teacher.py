from uuid import UUID

from sqlalchemy import select, delete, insert, update, func
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import joinedload

from src.application.common.exceptions.common import NotFound, OffsetNegative
from src.application.teacher.dto.creator import CreatorDTO, CreatorUserDTO
from src.application.teacher.dto.user import UserDTO
from src.application.teacher.interfaces.persistense import ITeacherReader, ITeacherRepo
from src.domain.teacher.models.teacher import Teacher
from src.infrastructure.database import models
from src.infrastructure.database.dao.dao import SQLAlchemyDAO
from src.application.teacher.dto.teacher import TeacherDTO


class TeacherReader(SQLAlchemyDAO, ITeacherReader):
    async def _teacher(self, teacher_id: UUID) -> models.Teacher:
        return await self.session.get(
            models.Teacher,
            teacher_id,
            options=[
                joinedload(models.Teacher.user),
                joinedload(models.Teacher.admin).joinedload(models.Admin.user),
                joinedload(models.Teacher.animal),
            ],
        )

    async def get_teacher(self, teacher_id) -> TeacherDTO:
        teacher = await self._teacher(teacher_id)

        if not teacher:
            raise NotFound

        return map_to_dto(teacher)

    async def get_teachers(self, offset: int, limit: int) -> list[TeacherDTO]:
        try:
            teachers = await self.session.scalars(
                select(models.Teacher)
                .offset(offset)
                .limit(limit)
                .order_by(models.Teacher.created_at.desc(), models.Teacher.name)
                .options(
                    joinedload(models.Teacher.user),
                    joinedload(models.Teacher.admin).joinedload(models.Admin.user),
                    joinedload(models.Teacher.animal),
                )
            )
        except DBAPIError as err:
            raise OffsetNegative from err

        return [map_to_dto(teacher) for teacher in teachers]

    async def get_all(self) -> list[TeacherDTO]:
        teachers = await self.session.scalars(
            select(models.Teacher).options(
                joinedload(models.Teacher.user),
                joinedload(models.Teacher.admin).joinedload(models.Admin.user),
                joinedload(models.Teacher.animal),
            )
        )

        return [map_to_dto(teacher) for teacher in teachers]

    async def get_teachers_count(self) -> int:
        return await self.session.scalar(select(func.count(models.Teacher.id)))


class TeacherRepo(SQLAlchemyDAO, ITeacherRepo):
    async def get_teacher(self, teacher_id: UUID) -> Teacher:
        teacher = await self.session.scalar(
            select(models.Teacher).where(models.Teacher.id == teacher_id)
        )

        return Teacher(
            id=teacher.id,
            user_id=teacher.user_id,
            name=teacher.name,
            surname=teacher.surname,
            patronymic=teacher.patronymic,
            birthday=teacher.birthday,
            level=teacher.level,
            description=teacher.description,
        )

    async def delete_teacher(self, teacher_id: UUID) -> None:
        await self.session.execute(
            delete(models.Teacher).where(models.Teacher.id == teacher_id)
        )

    async def add_teacher(self, teacher: Teacher) -> Teacher:
        await self.session.execute(
            insert(models.Teacher).values(
                id=teacher.id,
                user_id=teacher.user_id,
                name=teacher.name,
                surname=teacher.surname,
                patronymic=teacher.patronymic,
                birthday=teacher.birthday,
                level=teacher.level,
                description=teacher.description,
            )
        )

        return teacher

    async def update_teacher(self, teacher: Teacher) -> Teacher:
        await self.session.execute(
            update(models.Teacher)
            .where(models.Teacher.id == teacher.id)
            .values(
                name=teacher.name,
                surname=teacher.surname,
                patronymic=teacher.patronymic,
                birthday=teacher.birthday,
                level=teacher.level,
                description=teacher.description,
                access_start=teacher.access_start,
                access_end=teacher.access_end,
            )
        )

        return teacher


def map_to_dto(teacher: models.Teacher):
    return TeacherDTO(
        id=teacher.id,
        name=teacher.name,
        surname=teacher.surname,
        patronymic=teacher.patronymic,
        level=teacher.level,
        description=teacher.description,
        access_start=teacher.access_start,
        access_end=teacher.access_end,
        animal=teacher.animal.name if teacher.animal else None,
        birthday=teacher.birthday,
        user=UserDTO(
            created_at=teacher.user.created_at,
            id=teacher.user.id,
            email=teacher.user.email,
            phone=teacher.user.phone,
            timezone=teacher.user.timezone,
            telegram_id=teacher.user.telegram_id,
            telegram_username=teacher.user.telegram_username,
        ),
        creator=CreatorDTO(
            user=CreatorUserDTO(
                created_at=teacher.admin.user.created_at,
                id=teacher.admin.user.id,
                phone=teacher.admin.user.phone,
                telegram_id=teacher.admin.user.telegram_id,
            )
        ),
    )
