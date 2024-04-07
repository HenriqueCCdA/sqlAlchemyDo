import datetime

from typing import Optional
from sqlalchemy import BIGINT, NVARCHAR, TIMESTAMP, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    type_annotation_map = {
        int: BIGINT,
        datetime.datetime: TIMESTAMP(timezone=True),
        str: String().with_variant(NVARCHAR, "mssql")
    }


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[Optional[str]]
    nickname: Mapped[Optional[str]] = mapped_column(String(30))


class SomeClass(Base):
    __tablename__ = "some_table"

    id: Mapped[int] = mapped_column(primary_key=True)

    data: Mapped[str]

    additional_info: Mapped[Optional[str]]
