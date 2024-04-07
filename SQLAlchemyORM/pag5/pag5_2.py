from typing import Optional
from sqlalchemy import ForeignKey, Integer, String, Text, create_engine, null, table
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, column_property, relationship

class Base(DeclarativeBase):
    pass


class Person(Base):
    __tablename__ = "person"

    person_id = mapped_column(Integer, primary_key=True)
    type = mapped_column(String, nullable=False)

    __mapper_args__ = dict(
        polymorphic_on=type,
        polymorphic_identity="person",
    )

class Employee(Person):
    __mapper_args__ = dict(
        polymorphic_identity="employee",
    )


engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5434/test", echo=True)
Base.metadata.create_all(engine)
