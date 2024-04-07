from uuid import UUID

from sqlalchemy import CheckConstraint, MetaData, UniqueConstraint
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import declared_attr, DeclarativeBase, mapped_column, Mapped

constraint_naming_conventions = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=constraint_naming_conventions)


class MyAbstracBase(Base):
    __abstract__ = True

    @declared_attr.directive
    def __table_args__(cls):
        return (
            UniqueConstraint("uuid"),
            CheckConstraint("x > 0 OR y < 100", name="xy_chk")
        )

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[UUID]
    x: Mapped[int]
    y: Mapped[int]


class ModelAlpha(MyAbstracBase):
    __tablename__ = "alpha"


class ModelBeta(MyAbstracBase):
    __tablename__ = "beta"

print(CreateTable(ModelAlpha.__table__))
print(CreateTable(ModelBeta.__table__))
