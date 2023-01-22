import logging
from uuid import UUID

from src.application.admin.dto.admin import AdminDTO, AdminCreateDTO, AdminUpdateDTO
from src.application.admin.interfaces.uow import IAdminUoW
from src.domain.admin.services.admin import create_admin, update_admin
from src.application.common.exceptions.common import NotFound, AlreadyExists
from src.application.user.dto.user import UserCreateDTO, UserUpdateDTO
from src.domain.undefined.services.undefined import create_undefined
from src.domain.user.models.user import UserRole
from src.domain.user.services.user import create_user, update_user

logger = logging.getLogger(__name__)


class AdminUseCase:
    def __init__(self, uow: IAdminUoW):
        self.uow = uow


class GetAdmin(AdminUseCase):
    async def __call__(self, admin_id: UUID) -> AdminDTO:
        try:
            return await self.uow.admin_reader.get_admin(admin_id)
        except NotFound as err:
            logger.info(str(err))
            raise err


class GetAdminsCount(AdminUseCase):
    async def __call__(self) -> int:
        return await self.uow.admin_reader.get_admins_count()


class GetAdmins(AdminUseCase):
    async def __call__(self, offset: int, limit: int) -> list[AdminDTO]:
        return await self.uow.admin_reader.get_admins(offset, limit)


class GetAllAdmins(AdminUseCase):
    async def __call__(self) -> list[AdminDTO]:
        return await self.uow.admin_reader.get_all()


class DeleteAdmin(AdminUseCase):
    async def __call__(self, admin_id: UUID) -> None:
        admin = await self.uow.admin_repo.get_admin(admin_id)
        user = await self.uow.user_repo.get_user(admin.user_id)
        undefined = create_undefined(
            user_id=user.id,
            name=admin.name,
            surname=admin.surname,
            patronymic=admin.patronymic,
            birthday=admin.birthday,
        )
        user.role = UserRole.UNCERTAIN
        await self.uow.undefined_repo.add_undefined(undefined)
        await self.uow.user_repo.update_user(user)
        await self.uow.admin_repo.delete_admin(admin_id)
        await self.uow.commit()


class AddAdmin(AdminUseCase):
    async def __call__(
        self,
        user: UserCreateDTO,
        admin: AdminCreateDTO,
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
            admin_created = create_admin(
                user_id=user_created.id,
                name=admin.name,
                surname=admin.surname,
                patronymic=admin.patronymic,
                birthday=admin.birthday,
                level=admin.level,
                description=admin.description,
            )
            await self.uow.admin_repo.add_admin(admin_created)
            await self.uow.commit()
            return admin_created.id
        except AlreadyExists as err:
            logger.info(f"Conflict fields %s", str(err))
            await self.uow.rollback()
            raise err


class UpdateAdmin(AdminUseCase):
    async def __call__(
        self,
        user: UserUpdateDTO,
        admin: AdminUpdateDTO,
    ):
        try:
            getadmin = await self.uow.admin_repo.get_admin(admin.id)
            getuser = await self.uow.user_repo.get_user(getadmin.user_id)
            updateadmin = update_admin(
                getadmin,
                name=admin.name,
                surname=admin.surname,
                patronymic=admin.patronymic,
                birthday=admin.birthday,
                level=admin.level,
                description=admin.description,
                access_start=admin.access_start,
                access_end=admin.access_end,
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

            await self.uow.admin_repo.update_admin(updateadmin)
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
