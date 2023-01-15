from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


def sm_provider() -> sessionmaker:
    ...


def sm(db_url: str):
    engine = create_async_engine(db_url)
    session_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    print("FACTORY")
    return session_factory


def session_provider():
    ...


def session(db_url):
    engine = create_async_engine(db_url)
    session_factory = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def db_session():
        async with session_factory() as database_session:
            yield database_session

    return db_session
