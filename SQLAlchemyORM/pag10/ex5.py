import dataclasses
from typing import Any

from sqlalchemy import Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, composite, mapped_column, CompositeProperty
from sqlalchemy.sql import and_

@dataclasses.dataclass
class Point:
    x: int
    y: int


@dataclasses.dataclass
class Vertex:
    start: Point
    end: Point

    def _generate(cls, x1:int, y1: int, x2: int, y2: int):
        return Vertex(Point(x1, y1), Point(x2, y2))

    def __composite_values__(self) -> tuple[Any, ...]:
        return dataclasses.astuple(self.start) + dataclasses.astuple(self.end)

class Base(DeclarativeBase):
    pass


class HasVertex(Base):
    __tablename__ = "has_vertex"
    id: Mapped[int] = mapped_column(primary_key=True)

    x1: Mapped[int]
    y1: Mapped[int]
    x2: Mapped[int]
    y2: Mapped[int]

    vertex: Mapped[Vertex] = composite(Vertex._generate, "x1", "y1", "x2", "y2")

engine = create_engine("sqlite:///../orm.db", echo=True)
Base.metadata.create_all(engine)
