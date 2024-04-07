from sqlalchemy import Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, mapped_column, Session
from sqlalchemy.ext.hybrid import hybrid_property



class Base(DeclarativeBase):
    pass


class EmailAddress(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)

    _email = mapped_column("email", String)

    @hybrid_property
    def email(self):
        return self._email[:-12]

    @email.setter
    def email(self, email):
        self._email = email + "@example.com"

    @email.expression
    def email(cls):
        return func.substr(cls._email, 0, func.length(cls._email) - 12)


engine = create_engine("sqlite:///orm.db", echo=True)
Base.metadata.create_all(engine)
session = Session(engine)
