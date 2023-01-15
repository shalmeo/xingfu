import uuid

from sqlalchemy import Column, ForeignKey, String, DateTime, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.database.models.base import Base, TimeStampMixin


class Task(Base, TimeStampMixin):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_id = Column(ForeignKey("groups.id", ondelete="CASCADE"))
    title = Column(String, nullable=False)
    lesson_date = Column(Date, nullable=True)
    deadline = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)

    group = relationship("Group")


class TaskFile(Base, TimeStampMixin):
    __tablename__ = "task_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(ForeignKey("tasks.id", ondelete="CASCADE"))
    file_id = Column(String, nullable=False)
    type = Column(String, nullable=False)


class TaskBlackList(Base, TimeStampMixin):
    __tablename__ = "task_blacklist"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(ForeignKey("students.id", ondelete="CASCADE"))
    task_id = Column(UUID, ForeignKey("tasks.id", ondelete="CASCADE"))
