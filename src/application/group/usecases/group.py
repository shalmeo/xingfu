import logging
from uuid import UUID

from src.application.group.dto.group import GroupDTO, GroupCreateDTO, GroupUpdateDTO
from src.application.group.interfaces.uow import IGroupUoW
from src.domain.group.services.group import create_group, update_group
from src.application.common.exceptions.common import NotFound, AlreadyExists

logger = logging.getLogger(__name__)


class GroupUseCase:
    def __init__(self, uow: IGroupUoW):
        self.uow = uow


class GetGroup(GroupUseCase):
    async def __call__(self, group_id: UUID) -> GroupDTO:
        try:
            return await self.uow.group_reader.get_group(group_id)
        except NotFound as err:
            logger.info(str(err))
            raise err


class GetGroupsCount(GroupUseCase):
    async def __call__(self) -> int:
        return await self.uow.group_reader.get_groups_count()


class GetGroups(GroupUseCase):
    async def __call__(self, offset: int, limit: int) -> list[GroupDTO]:
        return await self.uow.group_reader.get_groups(offset, limit)


class GetAllGroups(GroupUseCase):
    async def __call__(self) -> list[GroupDTO]:
        return await self.uow.group_reader.get_all()


class DeleteGroup(GroupUseCase):
    async def __call__(self, group_id: UUID) -> None:
        await self.uow.group_repo.delete_group(group_id)
        await self.uow.commit()


class AddGroup(GroupUseCase):
    async def __call__(
        self,
        group: GroupCreateDTO,
    ) -> UUID:
        try:
            group_created = create_group(
                name=group.name, description=group.description, teacher_id=group.teacher_id, students=group.students
            )
            await self.uow.group_repo.add_group(group_created)
            await self.uow.commit()
            return group_created.id
        except AlreadyExists as err:
            logger.info(f"Conflict fields %s", str(err))
            await self.uow.rollback()
            raise err


class UpdateGroup(GroupUseCase):
    async def __call__(
        self,
        group: GroupUpdateDTO,
    ):
        try:
            getgroup = await self.uow.group_repo.get_group(group.id)
            updategroup = update_group(
                getgroup,
                name=group.name,
                description=group.description,
                teacher_id=group.teacher_id,
                students=group.students,
            )

            await self.uow.group_repo.update_group(updategroup)
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
