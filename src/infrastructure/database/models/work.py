import uuid

from sqlalchemy import Column, ForeignKey, DateTime, String, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID

from src.domain.work.models.work import WorkStatus
from src.infrastructure.database.models.base import Base, TimeStampMixin


class Work(Base, TimeStampMixin):
    __tablename__ = "works"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(ForeignKey("tasks.id", ondelete="CASCADE"))
    student_id = Column(ForeignKey("students.id", ondelete="CASCADE"))
    dispatch_datetime = Column(DateTime, nullable=False)
    status = Column(Enum(WorkStatus), default=WorkStatus.CHECKING)
    is_viewed = Column(Boolean, default=False)
    message = Column(String, nullable=True)


class WorkFile(Base, TimeStampMixin):
    __tablename__ = "work_files"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_id = Column(ForeignKey("works.id", ondelete="CASCADE"))
    file_id = Column(String, nullable=False)
    type = Column(String, nullable=False)


class Wom(Base, TimeStampMixin):
    __tablename__ = "woms"  # work on mistakes

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    work_id = Column(ForeignKey("works.id", ondelete="CASCADE"))
