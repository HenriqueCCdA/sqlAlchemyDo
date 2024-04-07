import dataclasses

from sqlalchemy import Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, composite, mapped_column

@dataclasses.dataclass
class Point:
    x: int
    y: int

class Base(DeclarativeBase):
    pass


class Vertex(Base):
    __tablename__ = "vertices"

    id: Mapped[int] = mapped_column(primary_key=True)

    x1: Mapped[int]
    y1: Mapped[int]
    x2: Mapped[int]
    y2: Mapped[int]

    start = composite(Point, x1, y1)
    end = composite(Point, x2, y2)

engine = create_engine("sqlite:///../orm.db", echo=True)
Base.metadata.create_all(engine)
