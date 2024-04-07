from typing import Literal

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects import postgresql

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5434/test", echo=True)

Status = Literal["peding", "received", "completed"]

class Base(DeclarativeBase):
    type_annotation_map = {
        Status: sqlalchemy.Enum("pending", "received", "completed", name="status_enum"),
    }


# class Status(enum.Enum):
#     PENDING = "peding"
#     RECEIVED = "received"
#     COMPLETED = "completed"




class SomeClass(Base):
    __tablename__ = "some_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[Status]


print(CreateTable(SomeClass.__table__).compile(dialect=postgresql.dialect()))

Base.metadata.create_all(engine)
