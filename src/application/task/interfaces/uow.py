from src.application.common.interfaces.uow import IUoW
from src.application.task.interfaces.persistense import ITaskReader


class ITaskUoW(IUoW):
    task_reader: ITaskReader
