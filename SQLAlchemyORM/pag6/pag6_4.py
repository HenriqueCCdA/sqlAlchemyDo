from datetime import datetime
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime]


class MyModel(TimestampMixin, Base):
    __tablename__ = "test"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
