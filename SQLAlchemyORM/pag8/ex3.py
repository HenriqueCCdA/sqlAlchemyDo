from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, mapped_column, Session, column_property
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.sql import case

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    firstname = mapped_column(String(50))
    lastname = mapped_column(String(50))
    fullname = column_property(firstname + " " + lastname)


engine = create_engine("sqlite:///orm.db", echo=True)
Base.metadata.create_all(engine)
