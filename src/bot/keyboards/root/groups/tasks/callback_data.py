from enum import Enum
from uuid import UUID

from aiogram.filters.callback_data import CallbackData


class TaskAction(Enum):
    INFO = "INFO"
    ATTACHED_FILES = "ATTACHED_FILES"


class TaskCallbackData(CallbackData, prefix="task"):
    task_id: UUID
    action: TaskAction


class TaskPageController(CallbackData, prefix="task_page"):
    offset: int
    limit: int


class GroupStudentCallbackData(CallbackData, prefix="group_stu"):
    student_id: UUID


class GroupStudentsPageController(CallbackData, prefix="group_stu_page"):
    offset: int
    limit: int
