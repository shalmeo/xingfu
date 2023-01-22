import logging
from typing import Optional
from uuid import UUID

from src.application.student.dto.student import (
    StudentDTO,
    StudentCreateDTO,
    StudentUpdateDTO,
)
from src.application.student.interfaces.uow import IStudentUoW
from src.domain.student.services.student import create_student, update_student
from src.application.common.exceptions.common import NotFound, AlreadyExists
from src.application.user.dto.user import UserCreateDTO, UserUpdateDTO
from src.domain.undefined.services.undefined import create_undefined
from src.domain.user.models.user import UserRole
from src.domain.user.services.user import create_user, update_user

logger = logging.getLogger(__name__)


class StudentUseCase:
    def __init__(self, uow: IStudentUoW):
        self.uow = uow


class GetStudent(StudentUseCase):
    async def __call__(self, student_id: UUID) -> StudentDTO:
        try:
            return await self.uow.student_reader.get_student(student_id)
        except NotFound as err:
            logger.info(str(err))
            raise err


class GetStudents(StudentUseCase):
    async def __call__(self, offset: int, limit: int) -> list[StudentDTO]:
        return await self.uow.student_reader.get_students(offset, limit)


class GetStudentsCount(StudentUseCase):
    async def __call__(self) -> int:
        return await self.uow.student_reader.get_students_count()


class GetAllStudents(StudentUseCase):
    async def __call__(self) -> list[StudentDTO]:
        return await self.uow.student_reader.get_all()


class GetGroupStudents(StudentUseCase):
    async def __call__(
        self,
        group_id: UUID,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[StudentDTO]:
        return await self.uow.student_reader.get_group_students(group_id, offset, limit)


class GetGroupStudentsCount(StudentUseCase):
    async def __call__(self, group_id) -> int:
        return await self.uow.student_reader.get_group_students_count(group_id)


class DeleteStudent(StudentUseCase):
    async def __call__(self, student_id: UUID) -> None:
        student = await self.uow.student_repo.get_student(student_id)
        user = await self.uow.user_repo.get_user(student.user_id)
        undefined = create_undefined(
            user_id=user.id,
            name=student.name,
            surname=student.surname,
            patronymic=student.patronymic,
            birthday=student.birthday,
        )
        user.change_own_role(UserRole.UNCERTAIN)
        await self.uow.undefined_repo.add_undefined(undefined)
        await self.uow.user_repo.update_user(user)
        await self.uow.student_repo.delete_student(student_id)
        await self.uow.commit()


class AddStudent(StudentUseCase):
    async def __call__(
        self,
        user: UserCreateDTO,
        student: StudentCreateDTO,
    ) -> UUID:
        try:
            user_created = create_user(
                email=user.email,
                phone=user.phone,
                timezone=user.timezone,
                role=user.role,
                telegram_id=user.telegram_id,
                telegram_username=user.telegram_username,
            )
            await self.uow.user_repo.add_user(user_created)
            student_created = create_student(
                user_id=user_created.id,
                name=student.name,
                surname=student.surname,
                patronymic=student.patronymic,
                birthday=student.birthday,
            )
            await self.uow.student_repo.add_student(student_created)
            await self.uow.commit()
            return student_created.id
        except AlreadyExists as err:
            logger.info(f"Conflict fields %s", str(err))
            await self.uow.rollback()
            raise err


class UpdateStudent(StudentUseCase):
    async def __call__(
        self,
        user: UserUpdateDTO,
        student: StudentUpdateDTO,
    ):
        try:
            getstudent = await self.uow.student_repo.get_student(student.id)
            getuser = await self.uow.user_repo.get_user(getstudent.user_id)
            updatestudent = update_student(
                getstudent,
                name=student.name,
                surname=student.surname,
                patronymic=student.patronymic,
                birthday=student.birthday,
                access_start=student.access_start,
                access_end=student.access_end,
            )
            updateuser = update_user(
                getuser,
                email=user.email,
                phone=user.phone,
                timezone=user.timezone,
                role=user.role,
                telegram_id=user.telegram_id,
                telegram_username=user.telegram_username,
            )

            await self.uow.student_repo.update_student(updatestudent)
            await self.uow.user_repo.update_user(updateuser)

            await self.uow.commit()
        except NotFound as err:
            logger.info(str(err))
            raise err
        except AlreadyExists as err:
            logger.info(f"Conflict fields %s", str(err))
            await self.uow.rollback()
            raise err


# class MapImportTeachers(RootUseCase):
#     def __call__(
#         self, teachers: list[dict]
#     ) -> list[tuple[dto.UserCreate, dto.TeacherCreate]]:
#         import_teachers = []
#         for teacher in teachers:
#             user = dto.UserCreate(
#                 name=teacher["name"],
#                 surname=teacher["surname"],
#                 patronymic=teacher["patronymic"],
#                 telegram_id=teacher["telegram_id"],
#                 telegram_username=teacher["telegram_username"],
#                 birthday=teacher["birthday"],
#                 email=teacher["email"],
#                 phone=teacher["phone"],
#                 timezone=teacher["timezone"],
#                 role=UserRole.STUDENT,
#             )
#             teacher = dto.TeacherCreate(
#                 level=teacher["level"],
#                 description=teacher["description"],
#             )
#             import_teachers.append((user, teacher))
#
#         return import_teachers
