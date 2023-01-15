import asyncio
import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.configure import configure_postgres
from src.infrastructure.database import models
from src.settings import get_settings


async def main():
    settings = get_settings()
    session_factory = configure_postgres(settings.postgres.url)

    session: AsyncSession
    async with session_factory() as session:
        groups = (
            await session.scalars(
                select(models.Group).options(selectinload(models.Group.students))
            )
        ).all()

        for group in groups:
            students = (await session.scalars(select(models.Student))).all()
            for i in range(10):
                student = random.choice(students)
                if student not in group.students:
                    group.students.append(student)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
