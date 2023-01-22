from typing import Protocol
from uuid import UUID

from src.application.undefined.dto.undefined import UndefinedDTO
from src.domain.undefined.models.undefined import Undefined


class IUndefinedReader(Protocol):
    async def get_undefined(self, undefined_id: UUID) -> UndefinedDTO:
        ...

    async def get_undefineds(self, offset: int, limit: int) -> list[UndefinedDTO]:
        ...

    async def get_undefineds_count(self) -> int:
        ...


class IUndefinedRepo(Protocol):
    async def add_undefined(self, undefined: Undefined) -> Undefined:
        ...

    async def get_undefined(self, undefined_id: UUID) -> Undefined:
        ...

    async def delete_undefined(self, undefined_id: UUID) -> None:
        ...
