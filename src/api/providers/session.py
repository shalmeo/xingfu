from sqlalchemy.orm import sessionmaker


def sm_provider() -> sessionmaker:
    ...


def sm(session_factory: sessionmaker):
    return session_factory


def session_provider():
    ...


def session(session_factory: sessionmaker):
    async def wrapper():
        async with session_factory() as database_session:
            yield database_session

    return wrapper
