from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, column_property, mapped_column


class Base(DeclarativeBase):
    pass

class Tablename:

    @declared_attr.directive
    def __tablename__(cls) -> Optional[str]:
        return cls.__name__.lower()

class Person(Tablename, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    discriminator: Mapped[str]
    __mapper_args__ = {"polymorphic_on": "discriminator"}


class Engineer(Person):
    id: Mapped[int] = mapped_column(ForeignKey("person.id"), primary_key=True)

    primary_language: Mapped[str]

    __mapper_args__ = {"polymorphic_identity": "engineer"}

class Manager(Person):

    @declared_attr.directive
    def __tablename__(cls) -> Optional[str]:
        return None

    __mapper_args__ = {"polymorphic_identity": "manager"}
