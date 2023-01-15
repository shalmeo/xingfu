from uuid import UUID

from src.domain.group.models.group import Group
from src.domain.group.models.stuent import Student
from src.domain.group.services.student import create_student


def create_group(name: str, description: str, teacher_id: UUID, students: list[UUID]) -> Group:
    return Group(
        name=name,
        description=description,
        teacher_id=teacher_id,
        students=[create_student(student_id) for student_id in students],
    )


def update_group(
    group: Group,
    name: str,
    description: str,
    teacher_id: UUID,
    students: list[UUID],
) -> Group:
    group.name = name
    group.description = description
    group.teacher_id = teacher_id
    group.students = [Student(id=s) for s in students]

    return group
