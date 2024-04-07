from typing import Optional
from sqlalchemy import ForeignKey, String, Text, create_engine, table
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, column_property, relationship

class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    firstname: Mapped[str] = mapped_column(String(50))
    lastname: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str] = column_property(firstname + " " + lastname)

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str]
    address_statictics: Mapped[Optional[str]] = mapped_column(Text, deferred=True)

    user: Mapped["User"] = relationship(back_populates="addresses")


class GroupUsers(Base):
    __tablename__ = "group_users"

    user_id = mapped_column(String(40))
    group_id = mapped_column(String(40))

    __mapper_args__ = {"primary_key": [user_id, group_id]}


engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5434/test", echo=True)
Base.metadata.create_all(engine)
