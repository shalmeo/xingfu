from uuid import UUID

from sqlalchemy import select, delete, insert, update, func
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import joinedload, selectinload

from src.application.common.exceptions.common import NotFound, OffsetNegative
from src.application.group.dto.creator import CreatorDTO
from src.application.group.dto.student import StudentDTO
from src.application.group.dto.teacher import TeacherDTO
from src.application.group.dto.user import UserDTO
from src.application.group.interfaces.persistense import IGroupReader, IGroupRepo
from src.domain.group.models.group import Group
from src.domain.group.models.stuent import Student
from src.infrastructure.database import models
from src.infrastructure.database.dao.dao import SQLAlchemyDAO
from src.application.group.dto.group import GroupDTO


class GroupReader(SQLAlchemyDAO, IGroupReader):
    async def _group(self, group_id: UUID) -> models.Group:
        return await self.session.get(
            models.Group,
            group_id,
            options=[
                joinedload(models.Group.teacher),
                joinedload(models.Group.teacher_user),
                joinedload(models.Group.admin_user),
                selectinload(models.Group.students).joinedload(models.Student.user),
            ],
        )

    async def get_group(self, group_id) -> GroupDTO:
        group = await self._group(group_id)

        if not group:
            raise NotFound

        return map_to_dto(group)

    async def get_groups(self, offset: int, limit: int) -> list[GroupDTO]:
        try:
            groups = await self.session.scalars(
                select(models.Group)
                .offset(offset)
                .limit(limit)
                .order_by(models.Group.created_at.desc(), models.Group.name)
                .options(
                    joinedload(models.Group.teacher),
                    joinedload(models.Group.teacher_user),
                    joinedload(models.Group.admin_user),
                    selectinload(models.Group.students).joinedload(models.Student.user),
                )
            )
        except DBAPIError as err:
            raise OffsetNegative from err

        return [map_to_dto(group) for group in groups]

    async def get_all(self) -> list[GroupDTO]:
        groups = await self.session.scalars(
            select(models.Group).options(
                joinedload(models.Group.teacher),
                joinedload(models.Group.teacher_user),
                joinedload(models.Group.admin_user),
                selectinload(models.Group.students).joinedload(models.Student.user),
            )
        )

        return [map_to_dto(group) for group in groups]

    async def get_groups_count(self):
        return await self.session.scalar(select(func.count(models.Group.id)))


class GroupRepo(SQLAlchemyDAO, IGroupRepo):
    async def get_group(self, group_id: UUID) -> Group:
        group: models.Group = await self.session.scalar(
            select(models.Group).where(models.Group.id == group_id).options(selectinload(models.Group.students))
        )

        return Group(
            id=group.id,
            name=group.name,
            description=group.description,
            teacher_id=group.teacher_id,
            students=[Student(id=s.id) for s in group.students],
        )

    async def delete_group(self, group_id: UUID) -> None:
        await self.session.execute(delete(models.Group).where(models.Group.id == group_id))

    async def add_group(self, group: Group) -> Group:
        await self.session.execute(
            insert(models.Group).values(
                id=group.id,
                name=group.name,
                description=group.description,
                teacher_id=group.teacher_id,
            )
        )
        for student in group.students:
            await self.session.execute(
                insert(models.StudentGroupAssociation).values(group_id=group.id, student_id=student.id)
            )

        return group

    async def update_group(self, group: Group) -> Group:
        await self.session.execute(
            update(models.Group)
            .where(models.Group.id == group.id)
            .values(
                name=group.name,
                description=group.description,
                teacher_id=group.teacher_id,
            )
        )
        await self.session.execute(
            delete(models.StudentGroupAssociation).where(models.StudentGroupAssociation.group_id == group.id)
        )
        for student in group.students:
            await self.session.execute(
                insert(models.StudentGroupAssociation).values(group_id=group.id, student_id=student.id)
            )

        return group


def map_to_dto(group: models.Group):
    teacher = None

    if group.teacher_user:
        teacher = TeacherDTO(
            id=group.teacher.id,
            name=group.teacher.name,
            surname=group.teacher.surname,
            patronymic=group.teacher.patronymic,
            user=UserDTO(
                created_at=group.teacher_user.created_at,
                id=group.teacher_user.id,
                phone=group.teacher_user.phone,
                telegram_id=group.teacher_user.telegram_id,
            ),
        )

    return GroupDTO(
        id=group.id,
        name=group.name,
        description=group.description,
        teacher=teacher,
        creator=CreatorDTO(
            user=UserDTO(
                created_at=group.admin_user.created_at,
                id=group.admin_user.id,
                phone=group.admin_user.phone,
                telegram_id=group.admin_user.telegram_id,
            )
        ),
        students=[
            StudentDTO(
                id=student.id,
                name=student.name,
                surname=student.surname,
                patronymic=student.patronymic,
                user=UserDTO(
                    created_at=student.user.created_at,
                    id=student.user.id,
                    phone=student.user.phone,
                    telegram_id=student.user.telegram_id,
                ),
            )
            for student in group.students
        ],
    )
