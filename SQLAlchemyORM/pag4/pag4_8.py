
from sqlalchemy import Column, String, create_engine, Table, Integer
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5434/test", echo=True)

class Base(DeclarativeBase):
    pass



class MyClassr(Base):
    __table__ = Table(
        "some_table",
        Base.metadata,
        autoload_with=engine
    )
