import uuid

from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID

from src.domain.distribution.models.distribution import (
    DistributionStatus,
    DistributionRecordStatus,
)
from src.infrastructure.database.models.base import Base, TimeStampMixin


class Distribution(Base, TimeStampMixin):
    __tablename__ = "distributions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    title = Column(String, nullable=False)
    status = Column(Enum(DistributionStatus), default=DistributionStatus.DURING)


class DistributionRecord(Base, TimeStampMixin):
    __tablename__ = "distribution_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    distribution_id = Column(ForeignKey("distributions.id", ondelete="CASCADE"))
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    status = Column(
        Enum(DistributionRecordStatus), default=DistributionRecordStatus.DURING
    )
