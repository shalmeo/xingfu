import io
from abc import ABC

import openpyxl
from openpyxl import Workbook


class ExcelExporter(ABC):
    def __init__(self, template_path):
        self._workbook = openpyxl.load_workbook(template_path)

    def set_active(self, worksheet: str) -> None:
        self._workbook.active = self._workbook[worksheet]

    def set_title(self, title: str) -> None:
        self._workbook.active.title = title
