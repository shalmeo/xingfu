from io import BytesIO
from typing import Optional, BinaryIO

from src.application.common.interfaces.exporter import IExporter
from src.application.student.dto.student import StudentDTO
from src.infrastructure.exporters.excel.exporter import ExcelExporter
from src.infrastructure.exporters.excel.formater import Formatter


class StudentExcelExporter(ExcelExporter, IExporter):
    def __init__(self, template_path: str, formatter: Optional[Formatter] = None):
        super().__init__(template_path=template_path)
        self.formatter = formatter

    def save(self, students: list[StudentDTO]) -> BinaryIO:
        buffer = BytesIO()
        self._write(students)
        self._workbook.save(buffer)
        buffer.seek(0)
        return buffer

    def _write(self, students: list[StudentDTO]) -> None:
        worksheet = self._workbook.active

        for row, student in enumerate(students, 1):
            data = (
                row,
                student.user.unique_code,
                f"{student.access_start}/{student.access_end}",
                student.creator.user.unique_code,
                student.user.timezone,
                f"{student.surname} {student.name} {student.patronymic}",
                student.school_nickname,
                student.user.email,
                student.user.telegram_username,
                student.user.telegram_id,
                student.user.phone,
                student.birthday,
            )
            worksheet.append(data)

            # self.formatter.format_row(row + 1, max_col=len(data))
