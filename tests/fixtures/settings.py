import pytest


@pytest.fixture
def admins_excel_path() -> str:
    return "tests/excel/admins.xlsx"


@pytest.fixture
def teachers_excel_path() -> str:
    return "tests/excel/teachers.xlsx"


@pytest.fixture
def students_excel_path() -> str:
    return "tests/excel/students.xlsx"
