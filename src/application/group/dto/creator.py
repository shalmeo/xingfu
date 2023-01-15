from src.application.common.dto.common import DTO
from src.application.group.dto.user import UserDTO


class CreatorDTO(DTO):
    user: UserDTO
