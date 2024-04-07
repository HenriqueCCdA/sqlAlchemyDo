from sqlalchemy import Index, Integer
from sqlalchemy.orm import declarative_mixin, declared_attr, DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    pass

class MyMixin:
    a = mapped_column(Integer)
    b = mapped_column(Integer)

    @declared_attr.directive
    def __table_args(cls):
        return (Index(f"test_idx_{cls.__tablename__}", "a", "b"),)


class MyModelA(MyMixin, Base):
    __tablename__ = "table_a"
    id = mapped_column(Integer, primary_key=True)


class MyModelB(MyMixin, Base):
    __tablename__ = "table_b"
    id = mapped_column(Integer, primary_key=True)
