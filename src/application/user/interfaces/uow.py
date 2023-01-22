from src.application.common.interfaces.uow import IUoW
from src.application.user.interfaces.persistense import IUserReader, IUserRepo


class IUserUoW(IUoW):
    user_reader: IUserReader
    user_repo: IUserRepo
