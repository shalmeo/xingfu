from typing import Protocol
from uuid import UUID

from src.application.group.dto.group import GroupDTO
from src.domain.group.models.group import Group


class IGroupReader(Protocol):
    async def get_group(self, group_id: UUID) -> GroupDTO:
        ...

    async def get_groups(self, offset: int, limit: int) -> list[GroupDTO]:
        ...

    async def get_all(self) -> list[GroupDTO]:
        ...

    async def get_groups_count(self):
        ...


class IGroupRepo(Protocol):
    async def get_group(self, group_id: UUID) -> Group:
        ...

    async def delete_group(self, group_id: UUID) -> None:
        ...

    async def add_group(self, group: Group) -> Group:
        ...

    async def update_group(self, group: Group) -> Group:
        ...
