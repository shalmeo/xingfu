import logging
from uuid import UUID

from src.application.common.exceptions.common import NotFound, AlreadyExists
from src.application.teacher.interfaces.uow import ITeacherUoW
from src.domain.teacher.services.teacher import create_teacher, update_teacher
from src.application.user.dto.user import UserCreateDTO, UserUpdateDTO
from src.domain.uncertain.services.uncertain import create_uncertain
from src.domain.user.models.user import UserRole
from src.domain.user.services.user import create_user, update_user
from src.application.teacher.dto.teacher import (
    TeacherDTO,
    TeacherCreateDTO,
    TeacherUpdateDTO,
)

logger = logging.getLogger(__name__)


class TeacherUseCase:
    def __init__(self, uow: ITeacherUoW):
        self.uow = uow


class GetTeacher(TeacherUseCase):
    async def __call__(self, teacher_id: UUID) -> TeacherDTO:
        try:
            return await self.uow.teacher_reader.get_teacher(teacher_id)
        except NotFound as err:
            logger.info(str(err))
            raise err


class GetTeachers(TeacherUseCase):
    async def __call__(self, offset: int, limit: int) -> list[TeacherDTO]:
        return await self.uow.teacher_reader.get_teachers(offset, limit)


class GetTeachersCount(TeacherUseCase):
    async def __call__(self) -> int:
        return await self.uow.teacher_reader.get_teachers_count()


class GetAllTeachers(TeacherUseCase):
    async def __call__(self) -> list[TeacherDTO]:
        return await self.uow.teacher_reader.get_all()


class DeleteTeacher(TeacherUseCase):
    async def __call__(self, teacher_id: UUID) -> None:
        teacher = await self.uow.teacher_repo.get_teacher(teacher_id)
        user = await self.uow.user_repo.get_user(teacher.user_id)
        uncertain = create_uncertain(
            user_id=user.id,
            name=teacher.name,
            surname=teacher.surname,
            patronymic=teacher.patronymic,
            birthday=teacher.birthday,
        )
        user.change_own_role(UserRole.UNCERTAIN)
        await self.uow.uncertain_repo.add_uncertain(uncertain)
        await self.uow.user_repo.update_user(user)
        await self.uow.teacher_repo.delete_teacher(teacher_id)
        await self.uow.commit()


class AddTeacher(TeacherUseCase):
    async def __call__(
        self,
        user: UserCreateDTO,
        teacher: TeacherCreateDTO,
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
            teacher_created = create_teacher(
                user_id=user_created.id,
                name=teacher.name,
                surname=teacher.surname,
                patronymic=teacher.patronymic,
                birthday=teacher.birthday,
                level=teacher.level,
                description=teacher.description,
            )
            await self.uow.teacher_repo.add_teacher(teacher_created)
            await self.uow.commit()
            return teacher_created.id
        except AlreadyExists as err:
            logger.info(f"Conflict fields %s", str(err))
            await self.uow.rollback()
            raise err


class UpdateTeacher(TeacherUseCase):
    async def __call__(
        self,
        user: UserUpdateDTO,
        teacher: TeacherUpdateDTO,
    ):
        try:
            getteacher = await self.uow.teacher_repo.get_teacher(teacher.id)
            getuser = await self.uow.user_repo.get_user(getteacher.user_id)
            updateteacher = update_teacher(
                getteacher,
                name=teacher.name,
                surname=teacher.surname,
                patronymic=teacher.patronymic,
                birthday=teacher.birthday,
                level=teacher.level,
                description=teacher.description,
                access_start=teacher.access_start,
                access_end=teacher.access_end,
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

            await self.uow.teacher_repo.update_teacher(updateteacher)
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
