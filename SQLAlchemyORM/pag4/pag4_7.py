
from sqlalchemy import Column, String, create_engine, Table, Integer
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5434/test", echo=True)

class Base(DeclarativeBase):
    pass



user_table = Table(
    "user",
    Base.metadata,
    Column("user_id", Integer, primary_key=True),
    Column("user_name", String),
)

class User(Base):
    __table__ = user_table

    id = user_table.c.user_id
    name = user_table.c.user_name


Base.metadata.create_all(engine)
