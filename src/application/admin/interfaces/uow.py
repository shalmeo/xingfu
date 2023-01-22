from src.application.admin.interfaces.persistense import IAdminReader, IAdminRepo
from src.application.common.interfaces.uow import IUoW
from src.application.undefined.interfaces.persistense import IUndefinedRepo
from src.application.user.interfaces.persistense import IUserRepo


class IAdminUoW(IUoW):
    admin_reader: IAdminReader
    admin_repo: IAdminRepo

    user_repo: IUserRepo
    undefined_repo: IUndefinedRepo
