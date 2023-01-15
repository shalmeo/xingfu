from src.application.common.interfaces.uow import IUoW
from src.application.teacher.interfaces.persistense import ITeacherReader, ITeacherRepo
from src.application.uncertain.interfaces.persistense import IUncertainRepo
from src.application.user.interfaces.persistense import IUserRepo


class ITeacherUoW(IUoW):
    teacher_reader: ITeacherReader
    teacher_repo: ITeacherRepo

    user_repo: IUserRepo
    uncertain_repo: IUncertainRepo
