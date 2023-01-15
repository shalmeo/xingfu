import sys
import asyncio
import random
from datetime import datetime

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from src.configure import configure_postgres
from src.domain.user.models.user import UserRole
from src.infrastructure.database import models
from src.settings import get_settings


async def main():
    entities = {
        "student": (models.Student, UserRole.STUDENT),
        "teacher": (models.Teacher, UserRole.TEACHER),
        "admin": (models.Admin, UserRole.ADMIN),
    }

    if len(sys.argv) != 2:
        print("The script must be executed with one argument!")
        return

    target = sys.argv[1]

    if target not in entities:
        print("The argument must be: student, teacher, admin")
        return

    model, enum = entities.get(target)

    settings = get_settings()
    session_factory = configure_postgres(settings.postgres.url)
    url = "https://637542cc08104a9c5f963b8f.mockapi.io/users"
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            users = await response.json()

    session: AsyncSession
    async with session_factory() as session:
        for data in users:
            user = models.User(
                telegram_username=f"username{random.randrange(1, 1000000)}",
                telegram_id=random.randrange(1, 799999999),
                phone=random.randrange(70000000000, 79999999999),
                email=f"email{random.randrange(1, 1000000)}@net{random.randrange(1, 1000000)}.com",
                role=enum,
            )
            session.add(user)
            await session.flush()
            u = model(
                user_id=user.id,
                name=data["name"],
                surname=data["surname"],
                patronymic=data["patronymic"],
                birthday=datetime.strptime(
                    data["birthday"].split("T")[0], r"%Y-%m-%d"
                ).date(),
            )
            session.add(u)
            await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
