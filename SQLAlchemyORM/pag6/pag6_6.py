from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, column_property, mapped_column


class Base(DeclarativeBase):
    pass

class SomethingMixin:
    x: Mapped[int]
    y: Mapped[int]

    @declared_attr
    def x_plus_y(cls) -> Mapped[int]:
        return column_property(cls.x + cls.y)

class Something(SomethingMixin, Base):
    __tablename__ = "something"

    id: Mapped[int] = mapped_column(primary_key=True)
