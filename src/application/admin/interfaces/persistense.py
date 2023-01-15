from typing import Protocol
from uuid import UUID

from src.application.admin.dto.admin import AdminDTO
from src.domain.admin.models.admin import Admin


class IAdminReader(Protocol):
    async def get_admin(self, admin_id: UUID) -> AdminDTO:
        ...

    async def get_admins(self, offset: int, limit: int) -> list[AdminDTO]:
        ...

    async def get_all(self) -> list[AdminDTO]:
        ...

    async def get_admins_count(self):
        ...


class IAdminRepo(Protocol):
    async def get_admin(self, admin_id: UUID) -> Admin:
        ...

    async def delete_admin(self, admin_id: UUID) -> None:
        ...

    async def add_admin(self, admin: Admin) -> Admin:
        ...

    async def update_admin(self, admin: Admin) -> Admin:
        ...
