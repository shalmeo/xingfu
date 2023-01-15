from src.application.common.interfaces.uow import IUoW
from src.application.user.interfaces.persistense import IUserRepo


class IUserUoW(IUoW):
    user_repo: IUserRepo
