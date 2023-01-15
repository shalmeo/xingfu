from src.application.common.interfaces.uow import IUoW
from src.application.group.interfaces.persistense import IGroupReader, IGroupRepo


class IGroupUoW(IUoW):
    group_reader: IGroupReader
    group_repo: IGroupRepo
