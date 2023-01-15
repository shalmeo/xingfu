from typing import Protocol, Optional


class IUser(Protocol):
    name: str


class IUserWithPatronymic(Protocol):
    name: str
    patronymic: Optional[str]


class IStudentWithSchoolNickname(Protocol):
    user: IUser
    animal: str


class ITeacherWithSchoolNickname(Protocol):
    user: IUserWithPatronymic
    animal: str
