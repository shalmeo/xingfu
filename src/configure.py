import logging
from pathlib import Path

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.infrastructure.localization.fluent import TranslationLoader, FluentAdapter


def configure_postgres(postgres_url: str) -> sessionmaker:
    engine = create_async_engine(postgres_url, future=True)

    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


def configure_logging() -> None:
    logging.getLogger("aiohttp.access").setLevel(logging.WARNING)
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )


def configure_fluent() -> FluentAdapter:
    locales_map = {"ru": ("ru",)}
    loader = TranslationLoader(Path("resources/locales"))
    return FluentAdapter(loader, locales_map)
