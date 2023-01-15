from src.application.common.exceptions.base import AppException


class AlreadyExists(AppException):
    """Already exists"""


class NotFound(AppException):
    """Not found"""


class OffsetNegative(AppException):
    """Offset negative"""
