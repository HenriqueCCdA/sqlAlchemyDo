import datetime

from typing import Annotated, Optional

from sqlalchemy import func, String
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped


intpk = Annotated[int, mapped_column(primary_key=True)]
# timestamp = Annotated[
#     datetime.datetime,
#     mapped_column(nullable=False, server_default=func.CURRENT_TIMESTAMP()),
# ]
required_name = Annotated[str, mapped_column(String(30), nullable=False)]

# class Base(DeclarativeBase):
#     pass

# class SomeClass(Base):
#     __tablename__ = "some_table"

#     id: Mapped[intpk]
#     name: Mapped[required_name]
#     created_at: Mapped[timestamp]

timestamp = Annotated[
    datetime.datetime,
    mapped_column(nullable=False),
]

class Base(DeclarativeBase):
    pass

class SomeClass(Base):
    __tablename__ = "some_table"

    id: Mapped[intpk]
    name: Mapped[required_name]
    create_at: Mapped[Optional[timestamp]]


print(CreateTable(SomeClass.__table__))
