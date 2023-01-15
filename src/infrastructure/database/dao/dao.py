from sqlalchemy.ext.asyncio import AsyncSession


class SQLAlchemyDAO:
    def __init__(self, session: AsyncSession):
        self.session = session
