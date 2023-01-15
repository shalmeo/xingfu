import uuid

from sqlalchemy import Column, ForeignKey, String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.infrastructure.database.defaults import get_root_admin_id
from src.infrastructure.database.models import Base, Admin, User, Animal
from src.infrastructure.database.models.base import TimeStampMixin, AccessDatesMixin


class Teacher(Base, TimeStampMixin, AccessDatesMixin):
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    admin_id = Column(
        ForeignKey("admins.id", ondelete="SET DEFAULT"), default=get_root_admin_id()
    )
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    animal_id = Column(ForeignKey("animals.id", ondelete="SET NULL"), nullable=True)

    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String, nullable=True)
    birthday = Column(Date, nullable=False)
    level = Column(String, nullable=True)
    description = Column(String, nullable=True)

    user: User = relationship("User")
    admin: Admin = relationship("Admin")
    animal: Animal = relationship("Animal")
