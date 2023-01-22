import uuid

from sqlalchemy import Column, ForeignKey, Date, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.database.models.base import TimeStampMixin, Base


class Undefined(Base, TimeStampMixin):
    __tablename__ = "undefineds"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    birthday = Column(Date, nullable=False)

    user = relationship("User")
