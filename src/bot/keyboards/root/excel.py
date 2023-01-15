from enum import Enum

from aiogram.filters.callback_data import CallbackData

from src.bot.keyboards.registry import Registry


class ExcelAction(Enum):
    IMPORT = "IMPORT"
    EXPORT = "EXPORT"
    UPLOAD = "UPLOAD"


class ExcelCallbackData(CallbackData, prefix="excel"):
    action: ExcelAction
    registry: Registry
