from io import BytesIO
from typing import Optional, BinaryIO

from src.application.common.interfaces.exporter import IExporter
from src.application.group.dto.group import GroupDTO
from src.infrastructure.exporters.excel.exporter import ExcelExporter
from src.infrastructure.exporters.excel.formater import Formatter


class GroupExcelExporter(ExcelExporter, IExporter):
    def __init__(self, template_path: str, formatter: Optional[Formatter] = None):
        super().__init__(template_path=template_path)
        self.formatter = formatter

    def save(self, groups: list[GroupDTO]) -> BinaryIO:
        buffer = BytesIO()
        self._write(groups)
        self._workbook.save(buffer)
        buffer.seek(0)
        return buffer

    def _write(self, groups: list[GroupDTO]) -> None:
        worksheet = self._workbook.active

        for row, group in enumerate(groups, 1):
            data = (
                row,
                str(group.id),
                group.creator.user.unique_code,
                group.name,
                group.description,
                group.teacher.user.unique_code if group.teacher else None,
                *[student.user.unique_code for student in group.students],
            )
            worksheet.append(data)

            # self.formatter.format_row(row + 1, max_col=16)
