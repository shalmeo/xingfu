from fastapi import APIRouter, Depends

from src.api import providers
from src.api.requests.root.group.create import GroupCreateRequest
from src.application.group.dto.group import GroupCreateDTO
from src.application.group.interfaces.uow import IGroupUoW
from src.application.group.usecases.group import AddGroup

router = APIRouter()


@router.post(
    "/group",
    status_code=201,
    responses={409: {"detail": "..."}},
)
async def group_create(
    group: GroupCreateRequest, uow: IGroupUoW = Depends(providers.uow_provider)
):
    await AddGroup(uow)(
        GroupCreateDTO(
            name=group.name,
            description=group.description,
            teacher_id=group.teacher.id,
            students=[student.id for student in group.students],
        ),
    )
