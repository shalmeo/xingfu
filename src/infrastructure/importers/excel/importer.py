import typing
from abc import ABC

import openpyxl


class ExcelImporter(ABC):
    def __init__(self, file: typing.Any):
        self._workbook = openpyxl.load_workbook(file)
