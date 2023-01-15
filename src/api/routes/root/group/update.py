from uuid import UUID

from fastapi import APIRouter, Depends

from src.api import providers
from src.api.requests.root.group.update import GroupUpdateRequest
from src.application.group.dto.group import GroupUpdateDTO
from src.application.group.interfaces.uow import IGroupUoW
from src.application.group.usecases.group import UpdateGroup

router = APIRouter()


@router.put(
    "/group/{id}",
    status_code=204,
    responses={409: {"detail": "Conflict"}},
)
async def group_update(
    id: UUID,
    group: GroupUpdateRequest,
    uow: IGroupUoW = Depends(providers.uow_provider),
):
    await UpdateGroup(uow)(
        GroupUpdateDTO(
            id=id,
            name=group.name,
            description=group.description,
            teacher_id=group.teacher.id,
            students=[s.id for s in group.students],
        ),
    )
