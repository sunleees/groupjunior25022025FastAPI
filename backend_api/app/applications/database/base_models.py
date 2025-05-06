from sqlalchemy.orm import DeclarativeBase, declarative_base

from applications.settings import settings


class Base(DeclarativeBase):
    pass
