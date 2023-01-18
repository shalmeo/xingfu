import logging
from uuid import UUID

from src.application.common.exceptions.common import AlreadyExists
from src.application.uncertain.dto.uncertain import UncertainDTO, UncertainCreateDTO
from src.application.uncertain.interfaces.uow import IUncertainUoW
from src.application.user.dto.user import UserCreateDTO
from src.domain.student.services.student import create_student
from src.domain.teacher.services.teacher import create_teacher
from src.domain.uncertain.services.uncertain import create_uncertain
from src.domain.user.models.user import UserRole
from src.domain.user.services.user import create_user

logger = logging.getLogger(__name__)


class UncertainUseCase:
    def __init__(self, uow: IUncertainUoW):
        self.uow = uow


class GetUncertain(UncertainUseCase):
    async def __call__(self, uncertain_id: UUID) -> UncertainDTO:
        return await self.uow.uncertain_reader.get_uncertain(uncertain_id)


class GetUncertains(UncertainUseCase):
    async def __call__(self, offset: int, limit: int) -> list[UncertainDTO]:
        return await self.uow.uncertain_reader.get_uncertains(offset, limit)


class GetUncertainsCount(UncertainUseCase):
    async def __call__(self) -> int:
        return await self.uow.uncertain_reader.get_uncertains_count()


class DeleteUncertain(UncertainUseCase):
    async def __call__(self, uncertain_id: UUID) -> None:
        uncertain = await self.uow.uncertain_repo.get_uncertain(uncertain_id)
        await self.uow.uncertain_repo.delete_uncertain(uncertain_id)
        await self.uow.user_repo.delete_user(uncertain.user_id)
        await self.uow.commit()


class AddUncertain(UncertainUseCase):
    async def __call__(self, user: UserCreateDTO, uncertain: UncertainCreateDTO):
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
            uncertain_created = create_uncertain(
                user_id=user_created.id,
                name=uncertain.name,
                surname=uncertain.surname,
                patronymic=uncertain.patronymic,
                birthday=uncertain.birthday,
            )
            await self.uow.uncertain_repo.add_uncertain(uncertain_created)
            await self.uow.commit()
            return uncertain_created.id
        except AlreadyExists as err:
            logger.info(f"Conflict fields %s", str(err))
            await self.uow.rollback()
            raise err


class DetermineUncertain(UncertainUseCase):
    async def __call__(self, uncertain_id: UUID, user_role: UserRole) -> UUID:
        uncertain = await self.uow.uncertain_repo.get_uncertain(uncertain_id)
        user = await self.uow.user_repo.get_user(uncertain.user_id)
        target = None
        if user_role == UserRole.STUDENT:
            target = await self.uow.student_repo.add_student(
                create_student(
                    user_id=user.id,
                    name=uncertain.name,
                    surname=uncertain.surname,
                    patronymic=uncertain.patronymic,
                    birthday=uncertain.birthday,
                )
            )
        elif user_role == UserRole.TEACHER:
            target = await self.uow.teacher_repo.add_teacher(
                create_teacher(
                    user_id=user.id,
                    name=uncertain.name,
                    surname=uncertain.surname,
                    patronymic=uncertain.patronymic,
                    birthday=uncertain.birthday,
                )
            )

        user.change_own_role(user_role)
        await self.uow.user_repo.update_user(user)
        await self.uow.uncertain_repo.delete_uncertain(uncertain_id)
        await self.uow.commit()

        return target.id if target else None
