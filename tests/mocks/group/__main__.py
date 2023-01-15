import asyncio

import aiohttp
from sqlalchemy.ext.asyncio import AsyncSession

from src.configure import configure_postgres
from src.infrastructure.database import models
from src.settings import get_settings


async def main():
    settings = get_settings()
    session_factory = configure_postgres(settings.postgres.url)
    url = "https://637542cc08104a9c5f963b8f.mockapi.io/groups"
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            groups = await response.json()

    session: AsyncSession
    async with session_factory() as session:
        for i, data in enumerate(groups):
            group = models.Group(name=f"Group № {i}", description=data["description"])
            session.add(group)
            await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
