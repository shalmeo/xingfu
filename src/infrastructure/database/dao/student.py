from uuid import UUID

from sqlalchemy import select, delete, insert, update, func
from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import joinedload

from src.application.common.exceptions.common import NotFound, OffsetNegative
from src.application.student.dto.creator import CreatorDTO, CreatorUserDTO
from src.application.student.dto.user import UserDTO
from src.application.student.interfaces.persistense import IStudentReader, IStudentRepo
from src.domain.student.models.student import Student
from src.infrastructure.database import models
from src.infrastructure.database.dao.dao import SQLAlchemyDAO
from src.application.student.dto.student import StudentDTO


class StudentReader(SQLAlchemyDAO, IStudentReader):
    async def _student(self, student_id: UUID) -> models.Student:
        return await self.session.get(
            models.Student,
            student_id,
            options=[
                joinedload(models.Student.user),
                joinedload(models.Student.animal),
                joinedload(models.Student.admin_user),
            ],
        )

    async def get_student(self, student_id) -> StudentDTO:
        student = await self._student(student_id)

        if not student:
            raise NotFound

        return map_to_dto(student)

    async def get_students(self, offset: int, limit: int) -> list[StudentDTO]:
        try:
            students = await self.session.scalars(
                select(models.Student)
                .offset(offset)
                .limit(limit)
                .order_by(models.Student.created_at.desc(), models.Student.name)
                .options(
                    joinedload(models.Student.user),
                    joinedload(models.Student.animal),
                    joinedload(models.Student.admin_user),
                )
            )
        except DBAPIError as err:
            raise OffsetNegative from err

        return [map_to_dto(student) for student in students]

    async def get_all(self) -> list[StudentDTO]:
        students = await self.session.scalars(
            select(models.Student).options(
                joinedload(models.Student.user),
                joinedload(models.Student.animal),
                joinedload(models.Student.admin_user),
            )
        )

        return [map_to_dto(student) for student in students]

    async def get_students_count(self) -> int:
        return await self.session.scalar(select(func.count(models.Student.id)))

    async def get_group_students(
        self, group_id: UUID, offset: int, limit: int
    ) -> list[StudentDTO]:
        try:
            students = await self.session.scalars(
                select(models.Student)
                .join(models.StudentGroupAssociation)
                .where(models.StudentGroupAssociation.group_id == group_id)
                .order_by(models.Student.created_at.desc(), models.Student.name)
                .offset(offset)
                .limit(limit)
                .options(
                    joinedload(models.Student.user),
                    joinedload(models.Student.animal),
                    joinedload(models.Student.admin_user),
                )
            )
        except DBAPIError as err:
            raise OffsetNegative from err

        return [map_to_dto(student) for student in students]

    async def get_group_students_count(self, group_id: UUID) -> int:
        return await self.session.scalar(
            select(func.count(models.Student.id))
            .join(models.StudentGroupAssociation)
            .where(models.StudentGroupAssociation.group_id == group_id)
        )


class StudentRepo(SQLAlchemyDAO, IStudentRepo):
    async def get_student(self, student_id: UUID) -> Student:
        student = await self.session.scalar(
            select(models.Student).where(models.Student.id == student_id)
        )

        return Student(
            id=student.id,
            user_id=student.user_id,
            name=student.name,
            surname=student.surname,
            patronymic=student.patronymic,
            birthday=student.birthday,
        )

    async def delete_student(self, student_id: UUID) -> None:
        await self.session.execute(
            delete(models.Student).where(models.Student.id == student_id)
        )

    async def add_student(self, student: Student) -> Student:
        await self.session.execute(
            insert(models.Student).values(
                id=student.id,
                user_id=student.user_id,
                name=student.name,
                surname=student.surname,
                patronymic=student.patronymic,
                birthday=student.birthday,
            )
        )

        return student

    async def update_student(self, student: Student) -> Student:
        await self.session.execute(
            update(models.Student)
            .where(models.Student.id == student.id)
            .values(
                name=student.name,
                surname=student.surname,
                patronymic=student.patronymic,
                birthday=student.birthday,
                access_start=student.access_start,
                access_end=student.access_end,
            )
        )

        return student


def map_to_dto(student: models.Student):
    return StudentDTO(
        id=student.id,
        name=student.name,
        surname=student.surname,
        patronymic=student.patronymic,
        access_start=student.access_start,
        access_end=student.access_end,
        animal=student.animal.name if student.animal else None,
        birthday=student.birthday,
        user=UserDTO(
            created_at=student.user.created_at,
            id=student.user.id,
            phone=student.user.phone,
            telegram_id=student.user.telegram_id,
            telegram_username=student.user.telegram_username,
            email=student.user.email,
            timezone=student.user.timezone,
        ),
        creator=CreatorDTO(
            user=CreatorUserDTO(
                created_at=student.admin_user.created_at,
                id=student.admin_user.id,
                phone=student.admin_user.phone,
                telegram_id=student.admin_user.telegram_id,
            )
        ),
    )
