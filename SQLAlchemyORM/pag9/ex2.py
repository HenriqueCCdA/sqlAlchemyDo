from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.ext.hybrid import hybrid_property



class Base(DeclarativeBase):
    pass


class EmailAddress(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)

    _email = mapped_column("email", String)

    @hybrid_property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email


engine = create_engine("sqlite:///orm.db", echo=True)
Base.metadata.create_all(engine)
