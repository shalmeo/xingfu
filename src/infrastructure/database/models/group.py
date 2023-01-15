import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.database.defaults import get_root_admin_id
from src.infrastructure.database.models import Admin, Teacher
from src.infrastructure.database.models.base import TimeStampMixin, Base


class Group(Base, TimeStampMixin):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    admin_id = Column(
        ForeignKey(Admin.id, ondelete="SET DEFAULT"), default=get_root_admin_id()
    )
    teacher_id = Column(ForeignKey(Teacher.id, ondelete="SET NULL"), nullable=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)

    teacher = relationship("Teacher")
    admin_user = relationship(
        "User",
        secondary="admins",
        uselist=False,
        viewonly=True,
    )
    teacher_user = relationship(
        "User", secondary="teachers", uselist=False, viewonly=True
    )

    students = relationship(
        "Student",
        secondary="student_group_associations",
        uselist=True,
    )


class StudentGroupAssociation(Base, TimeStampMixin):
    __tablename__ = "student_group_associations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(ForeignKey("groups.id", ondelete="CASCADE"))
    student_id = Column(ForeignKey("students.id", ondelete="CASCADE"))
