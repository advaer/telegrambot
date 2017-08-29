import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
)


class BaseMixin:
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    created = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        index=True
    )
    modified = Column(
        DateTime,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        index=True
    )
