from io import BytesIO
from typing import Optional, BinaryIO

from src.application.admin.dto.admin import AdminDTO
from src.application.common.interfaces.exporter import IExporter
from src.infrastructure.exporters.excel.exporter import ExcelExporter
from src.infrastructure.exporters.excel.formater import Formatter


class AdminExcelExporter(ExcelExporter, IExporter):
    def __init__(self, template_path: str, formatter: Optional[Formatter] = None):
        super().__init__(template_path=template_path)
        self.formatter = formatter

    def save(self, admins: list[AdminDTO]) -> BinaryIO:
        buffer = BytesIO()
        self._write(admins)
        self._workbook.save(buffer)
        buffer.seek(0)
        return buffer

    def _write(self, admins: list[AdminDTO]) -> None:
        worksheet = self._workbook.active

        for row, admin in enumerate(admins, 1):
            data = (
                row,
                admin.user.unique_code,
                f"{admin.access_start}/{admin.access_end}",
                admin.user.timezone,
                f"{admin.surname} {admin.name} {admin.patronymic}",
                admin.user.email,
                admin.user.telegram_username,
                admin.user.telegram_id,
                admin.user.phone,
                admin.level,
                admin.description,
                admin.birthday,
            )
            worksheet.append(data)

            # self.formatter.format_row(row + 1, max_col=len(data))
