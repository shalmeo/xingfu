from uuid import UUID

from src.application.uncertain.dto.uncertain import UncertainDTO
from src.application.uncertain.interfaces.uow import IUncertainUoW
from src.domain.student.services.student import create_student
from src.domain.teacher.services.teacher import create_teacher
from src.domain.user.models.user import UserRole


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


class DetermineUncertain(UncertainUseCase):
    async def __call__(self, uncertain_id: UUID, user_role: UserRole):
        uncertain = await self.uow.uncertain_repo.get_uncertain(uncertain_id)
        user = await self.uow.user_repo.get_user(uncertain.user_id)

        if user_role == UserRole.STUDENT:
            await self.uow.student_repo.add_student(
                create_student(
                    user_id=user.id,
                    name=uncertain.name,
                    surname=uncertain.surname,
                    patronymic=uncertain.patronymic,
                    birthday=uncertain.birthday,
                )
            )
        elif user_role == UserRole.TEACHER:
            await self.uow.teacher_repo.add_teacher(
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
