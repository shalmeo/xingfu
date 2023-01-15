from typing import Any

from src.domain.root.interfaces.importer import IImporter
from src.infrastructure.importers.excel.importer import ExcelImporter
from src.infrastructure.importers.excel.serializers import serialize


class StudentExcelImporter(ExcelImporter, IImporter):
    def __init__(self, file: Any):
        super().__init__(file=file)

    def import_(self) -> list[dict]:
        worksheet = self._workbook.active
        students = []
        parent_columns = range(15, 26)
        for row in worksheet.iter_rows(min_row=2, min_col=2, max_col=14):
            student = []
            parents = []
            for cell in row:
                if cell.column in parent_columns:
                    parents.append(serialize(cell.value))
                    continue

                student.append(serialize(cell.value))

            serialized_parents = parse_parents(parents)

            try:
                serialized_student = parse_student(student)
                serialized_student.update(parents=serialized_parents)
            except (ValueError, AttributeError):
                continue

            students.append(serialized_student)

        return students


def parse_student(student: list[Any]) -> dict:
    (
        *_,
        timezone,
        full_name,
        _,
        email,
        username,
        telegram_id,
        phone,
        birthday,
    ) = student

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
        birthday=birthday,
    )


def parse_parents(parents: list[Any]) -> list:
    serialized_parents = []
    (
        parent1_fullname,
        parent1_telegram_id,
        parent1_phone,
        parent2_fullname,
        parent2_telegram_id,
        parent2_phone,
    ) = parents
    if parent1_fullname:
        try:
            serialized_parent = parse_parent(
                [parent1_fullname, parent1_telegram_id, parent1_phone]
            )
            serialized_parents.append(serialized_parent)
        except (ValueError, AttributeError):
            pass

    if parent2_fullname:
        try:
            serialized_parent = parse_parent(
                [parent2_fullname, parent2_telegram_id, parent2_phone]
            )
            serialized_parents.append(serialized_parent)
        except (ValueError, AttributeError):
            pass

    return serialized_parents


def parse_parent(parent: list[Any]) -> dict:
    fullname, phone, telegram_id = parent
    surname, name, patronymic = fullname.split()
    return dict(
        name=name,
        surname=surname,
        patronymic=patronymic,
        phone=phone,
        telegram_id=telegram_id,
    )
