from sqlalchemy import Column, BigInteger, String, Enum

from src.domain.user.models.user import UserRole
from src.infrastructure.database.models.base import Base, TimeStampMixin


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True)

    email = Column(String, unique=True, nullable=False)
    phone = Column(BigInteger, unique=True, nullable=True)
    timezone = Column(String, nullable=False, default="UTC+3")
    telegram_id = Column(BigInteger, nullable=True)
    telegram_username = Column(String, nullable=True)
    role = Column(Enum(UserRole), nullable=False)
