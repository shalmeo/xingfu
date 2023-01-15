from typing import Any

from src.domain.root.interfaces.importer import IImporter
from src.infrastructure.importers.excel.importer import ExcelImporter
from src.infrastructure.importers.excel.serializers import serialize


class TeacherExcelImporter(ExcelImporter, IImporter):
    def __init__(self, file: Any):
        super().__init__(file=file)

    def import_(self) -> list[dict]:
        worksheet = self._workbook.active
        teachers = []
        for row in worksheet.iter_rows(min_row=2, min_col=2, max_col=14):
            teacher = []
            for cell in row:
                teacher.append(serialize(cell.value))

            try:
                serialized = parse_teacher(teacher)
            except ValueError:
                continue

            teachers.append(serialized)

        return teachers


def parse_teacher(teacher: list[Any]) -> dict:
    (
        *_,
        timezone,
        full_name,
        _,
        email,
        username,
        telegram_id,
        phone,
        level,
        description,
        birthday,
    ) = teacher

    if not timezone:
        raise ValueError

    if not full_name:
        raise ValueError
    else:
        surname, name, patronymic = full_name.split()

    if not email:
        raise ValueError

    return dict(
        timezone=timezone,
        name=name,
        surname=surname,
        patronymic=patronymic,
        email=email,
        username=username,
        telegram_id=telegram_id,
        phone=phone,
        level=level,
        description=description,
        birthday=birthday,
    )
