import datetime
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from src.domain.user.models.user import UserRole
from src.infrastructure.database import models

logger = logging.getLogger(__name__)


async def add_initial_admins(session_maker: sessionmaker, bot_admins: list[int]):
    async with session_maker() as session:
        for i, admin_id in enumerate(bot_admins, 1):
            try:
                user = models.User(email=f"root{i}@email.com", role=UserRole.ROOT, telegram_id=admin_id)
                admin = models.Admin(
                    name=f"root{i}",
                    surname=f"admin{i}",
                    birthday=datetime.date.today(),
                )
                admin.user = user
                session.add_all((admin, user))
                await session.flush()
                logger.info("Admin with telegram_id=%s added to database", admin_id)
            except IntegrityError:
                logger.info("Admin with telegram_id=%s already added", admin_id)
                await session.rollback()

        await session.commit()
