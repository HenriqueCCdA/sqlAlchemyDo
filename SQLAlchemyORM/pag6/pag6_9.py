from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, has_inherited_table


class Base(DeclarativeBase):
    pass

class HasIdMixin:

    @declared_attr.cascading
    def id(cls) -> Mapped[int]:
        if has_inherited_table(cls):
            return mapped_column(ForeignKey("person.id"), primary_key=True)
        else:
            return mapped_column(Integer, primary_key=True)

class Person(HasIdMixin, Base):
    __tablename__ = "person"

    discriminator: Mapped[str]
    __mapper_args__ = {"polymorphic_on": "discriminator"}

class Engineer(Person):
    __tablename__ = "engineer"

    primary_language: Mapped[str]
    __mapper_args__ = {"polymorphic_identity": "engineer"}
