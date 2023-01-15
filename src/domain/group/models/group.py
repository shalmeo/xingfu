from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from src.domain.common.models.entity import Entity
from src.domain.group.models.stuent import Student


class Group(Entity):
    id: UUID = Field(default_factory=uuid4)
    teacher_id: Optional[UUID]
    students: list[Student]
    
    name: str
    description: Optional[str]
    
    def add_student(self, student: Student) -> None:
        if len(self.students) == 10:
            raise 
        
        self.students.append(student)
