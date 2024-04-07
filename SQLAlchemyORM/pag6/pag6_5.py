from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

class Target(Base):
    __tablename__ = "target"
    id: Mapped[int] = mapped_column(primary_key=True)

class RefTargetMixin:
    target_id: Mapped[int] = mapped_column(ForeignKey("target.id"))

    @declared_attr
    def target(cls) -> Mapped["Target"]:
        return relationship("Target", primaryjoin=Target.id == cls.target_id)

class Foo(RefTargetMixin, Base):
    __tablename__ = "foo"
    id: Mapped[int] = mapped_column(primary_key=True)

class Bar(RefTargetMixin, Base):
    __tablename__ = "bar"
    id: Mapped[int] = mapped_column(primary_key=True)
