from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


def session_provider():
    ...


def session(db_url: str):
    engine = create_async_engine(db_url)
    session_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def get_db_session() -> AsyncSession:
        db_session: AsyncSession = session_factory()
        try:
            yield db_session
        finally:
            await db_session.close()

    return get_db_session
