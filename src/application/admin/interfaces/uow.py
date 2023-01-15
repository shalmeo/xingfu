from src.application.admin.interfaces.persistense import IAdminReader, IAdminRepo
from src.application.common.interfaces.uow import IUoW
from src.application.uncertain.interfaces.persistense import IUncertainRepo
from src.application.user.interfaces.persistense import IUserRepo


class IAdminUoW(IUoW):
    admin_reader: IAdminReader
    admin_repo: IAdminRepo

    user_repo: IUserRepo
    uncertain_repo: IUncertainRepo
