from io import BytesIO
from typing import Optional, BinaryIO

from src.application.common.interfaces.exporter import IExporter
from src.application.teacher.dto.teacher import TeacherDTO
from src.infrastructure.exporters.excel.exporter import ExcelExporter
from src.infrastructure.exporters.excel.formater import Formatter


class TeacherExcelExporter(ExcelExporter, IExporter):
    def __init__(self, template_path: str, formatter: Optional[Formatter] = None):
        super().__init__(template_path=template_path)
        self.formatter = formatter

    def save(self, teachers: list[TeacherDTO]) -> BinaryIO:
        buffer = BytesIO()
        self._write(teachers)
        self._workbook.save(buffer)
        buffer.seek(0)
        return buffer

    def _write(self, teachers: list[TeacherDTO]) -> None:
        worksheet = self._workbook.active

        for row, teacher in enumerate(teachers, 1):
            data = (
                row,
                teacher.user.unique_code,
                f"{teacher.access_start}/{teacher.access_end}",
                teacher.creator.user.unique_code,
                teacher.user.timezone,
                f"{teacher.surname} {teacher.name} {teacher.patronymic}",
                teacher.school_nickname,
                teacher.user.email,
                teacher.user.telegram_username,
                teacher.user.telegram_id,
                teacher.user.phone,
                teacher.level,
                teacher.description,
                teacher.birthday,
            )
            worksheet.append(data)

            # self.formatter.format_row(row + 1, max_col=len(data))
