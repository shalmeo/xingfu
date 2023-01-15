from sqlalchemy import select

from src.domain.user.models.user import UserRole
from src.infrastructure.database import models


def get_root_admin_id():
    return (
        select(models.Admin.id)
        .join(models.User)
        .where(models.User.role == UserRole.ROOT)
        .order_by(models.Admin.created_at.asc())
        .limit(1)
    )
