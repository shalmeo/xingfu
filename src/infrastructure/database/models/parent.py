import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.database.models.base import TimeStampMixin, Base


class Parent(Base, TimeStampMixin):
    __tablename__ = "parents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)


class StudentParentAssociation(Base, TimeStampMixin):
    __tablename__ = "student_parent_associations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    parent_id = Column(ForeignKey("parents.id", ondelete="CASCADE"), nullable=False)
