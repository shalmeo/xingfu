from typing import Protocol
from uuid import UUID

from src.application.uncertain.dto.uncertain import UncertainDTO
from src.domain.uncertain.models.uncertain import Uncertain


class IUncertainReader(Protocol):
    async def get_uncertain(self, uncertain_id: UUID) -> UncertainDTO:
        ...

    async def get_uncertains(self, offset: int, limit: int) -> list[UncertainDTO]:
        ...

    async def get_uncertains_count(self) -> int:
        ...


class IUncertainRepo(Protocol):
    async def add_uncertain(self, uncertain: Uncertain) -> Uncertain:
        ...

    async def get_uncertain(self, uncertain_id: UUID) -> Uncertain:
        ...

    async def delete_uncertain(self, uncertain_id: UUID) -> None:
        ...
