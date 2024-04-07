# from sqlalchemy.orm import DeclarativeBase, registry

# reg = registry()

# class Base(DeclarativeBase):
#     registry = reg
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship, registry

mapper_registry = registry()


class Base(DeclarativeBase):
    pass


@mapper_registry.mapped
class User:
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    nickname: Mapped[Optional[str]] = mapped_column(String(64))
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")

@mapper_registry.mapped
class Address:
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="addresses")

@mapper_registry.mapped
class Person:
    __tablename__ = "person"

    person_id = mapped_column(Integer, primary_key=True)
    type = mapped_column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "person",
    }


@mapper_registry.mapped
class Employee(Person):
    __tablename__ = "employee"

    person_id = mapped_column(ForeignKey("person.person_id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "employee",
    }
