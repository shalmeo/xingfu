from typing import Any

from src.domain.root.interfaces.importer import IImporter
from src.infrastructure.importers.excel.importer import ExcelImporter
from src.infrastructure.importers.excel.serializers import serialize


class GroupExcelImporter(ExcelImporter, IImporter):
    def __init__(self, file: Any):
        super().__init__(file=file)

    def import_(self) -> list[dict]:
        worksheet = self._workbook.active
        groups = []
        for row in worksheet.iter_rows(min_row=2, min_col=2, max_col=16):
            group = []
            for cell in row:
                group.append(serialize(cell.value))

            try:
                serialized = parse_group(group)
            except ValueError:
                continue

            groups.append(serialized)

        return groups


def parse_group(group) -> dict:
    _, _, name, description, teacher_unique_code, *student_unique_codes = group

    return dict(
        name=name,
        description=description,
        teacher_unique_code=teacher_unique_code,
        student_unique_codes=student_unique_codes,
    )
