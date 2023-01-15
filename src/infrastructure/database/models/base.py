from sqlalchemy import TIMESTAMP, Column, Date, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.decl_api import declarative_mixin
from sqlalchemy.sql import expression
from sqlalchemy.ext.compiler import compiles
from sqlalchemy import types


meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
Base = declarative_base(metadata=meta)


class utcnow(expression.FunctionElement):
    type = types.DateTime()
    inherit_cache = True


class defaultaccess(expression.FunctionElement):
    type = types.Date()
    inherit_cache = True


@compiles(defaultaccess, "postgresql")
def pg_defaultaccess(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP) + interval '10 year'"


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


@declarative_mixin
class TimeStampMixin:
    __abstract__ = True

    created_at = Column(TIMESTAMP(timezone=True), server_default=utcnow())


@declarative_mixin
class AccessDatesMixin:
    __abstract__ = True

    access_start = Column(Date, server_default=utcnow())
    access_end = Column(Date, server_default=defaultaccess())
