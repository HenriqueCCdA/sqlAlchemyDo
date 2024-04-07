from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, mapped_column, Session
from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.sql import case

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id = mapped_column(Integer, primary_key=True)
    firstname = mapped_column(String(50))
    lastname = mapped_column(String(50))

    @hybrid_property
    def fullname(self):
        return self.firstname + " " + self.lastname

    @fullname.expression
    def fullname(cls):
        return case(
            (cls.firstname != None, cls.firstname + " " + cls.lastname),
            else_=cls.lastname,
        )

engine = create_engine("sqlite:///orm.db", echo=True)
Base.metadata.create_all(engine)
