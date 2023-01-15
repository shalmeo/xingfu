import datetime
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.user.models.user import UserRole
from src.infrastructure.database import models

logger = logging.getLogger(__name__)


async def add_initial_admins(session: AsyncSession, bot_admins: list[int]):
    for i, admin_telegram_id in enumerate(bot_admins, 1):
        try:
            user = models.User(
                name=f"Root{i}",
                surname=f"Administrator{i}",
                birthday=datetime.date.today(),
                telegram_id=admin_telegram_id,
                email=f"root{i}@email.com",
                role=UserRole.ROOT,
            )
            session.add(user)
            await session.flush()
            admin = models.Admin(user_id=user.id)
            session.add(admin)
            await session.flush()
            logger.info(
                "Admin with telegram_id=%s added to database", admin_telegram_id
            )
        except IntegrityError:
            logger.info("Admin with telegram_id=%s already added", admin_telegram_id)
            await session.rollback()

        await session.commit()
