import logging
from uuid import UUID

from src.application.common.exceptions.common import AlreadyExists
from src.application.undefined.dto.undefined import UndefinedDTO, UndefinedCreateDTO
from src.application.undefined.interfaces.uow import IUndefinedUoW
from src.application.user.dto.user import UserCreateDTO
from src.domain.student.services.student import create_student
from src.domain.teacher.services.teacher import create_teacher
from src.domain.undefined.services.undefined import create_undefined
from src.domain.user.models.user import UserRole
from src.domain.user.services.user import create_user

logger = logging.getLogger(__name__)


class UndefinedUseCase:
    def __init__(self, uow: IUndefinedUoW):
        self.uow = uow


class GetUndefined(UndefinedUseCase):
    async def __call__(self, undefined_id: UUID) -> UndefinedDTO:
        return await self.uow.undefined_reader.get_undefined(undefined_id)


class GetUndefineds(UndefinedUseCase):
    async def __call__(self, offset: int, limit: int) -> list[UndefinedDTO]:
        return await self.uow.undefined_reader.get_undefineds(offset, limit)


class GetUndefinedsCount(UndefinedUseCase):
    async def __call__(self) -> int:
        return await self.uow.undefined_reader.get_undefineds_count()


class DeleteUndefined(UndefinedUseCase):
    async def __call__(self, undefined_id: UUID) -> None:
        undefined = await self.uow.undefined_repo.get_undefined(undefined_id)
        await self.uow.undefined_repo.delete_undefined(undefined_id)
        await self.uow.user_repo.delete_user(undefined.user_id)
        await self.uow.commit()


class AddUndefined(UndefinedUseCase):
    async def __call__(self, user: UserCreateDTO, undefined: UndefinedCreateDTO):
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
            undefined_created = create_undefined(
                user_id=user_created.id,
                name=undefined.name,
                surname=undefined.surname,
                patronymic=undefined.patronymic,
                birthday=undefined.birthday,
            )
            await self.uow.undefined_repo.add_undefined(undefined_created)
            await self.uow.commit()
            return undefined_created.id
        except AlreadyExists as err:
            logger.info(f"Conflict fields %s", str(err))
            await self.uow.rollback()
            raise err


class DetermineUndefined(UndefinedUseCase):
    async def __call__(self, undefined_id: UUID, user_role: UserRole) -> UUID:
        undefined = await self.uow.undefined_repo.get_undefined(undefined_id)
        user = await self.uow.user_repo.get_user(undefined.user_id)
        target = None
        if user_role == UserRole.STUDENT:
            target = await self.uow.student_repo.add_student(
                create_student(
                    user_id=user.id,
                    name=undefined.name,
                    surname=undefined.surname,
                    patronymic=undefined.patronymic,
                    birthday=undefined.birthday,
                )
            )
        elif user_role == UserRole.TEACHER:
            target = await self.uow.teacher_repo.add_teacher(
                create_teacher(
                    user_id=user.id,
                    name=undefined.name,
                    surname=undefined.surname,
                    patronymic=undefined.patronymic,
                    birthday=undefined.birthday,
                )
            )

        user.change_own_role(user_role)
        await self.uow.user_repo.update_user(user)
        await self.uow.undefined_repo.delete_undefined(undefined_id)
        await self.uow.commit()

        return target.id if target else None
