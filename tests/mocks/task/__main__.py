import asyncio
import datetime
import sys

from sqlalchemy.ext.asyncio import AsyncSession

from src.configure import configure_postgres
from src.infrastructure.database import models
from src.settings import get_settings


async def main():
    if len(sys.argv) != 2:
        print("The script must be executed with one argument - group id!")
        return

    group_id = sys.argv[1]

    settings = get_settings()
    session_factory = configure_postgres(settings.postgres.url)

    session: AsyncSession
    async with session_factory() as session:
        for i in range(1, 50):
            task = models.Task(
                group_id=group_id,
                title=f"Task №{i}",
                description=f"description {i}",
                deadline=datetime.datetime.now(),
            )
            session.add(task)
            await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
