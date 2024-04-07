import dataclasses

from sqlalchemy import create_engine
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

    start: Mapped[Point] = composite(mapped_column("x1"), mapped_column("y1"))
    end: Mapped[Point] = composite(mapped_column("x2"), mapped_column("y2"))

    def __repr__(self):
        return f"Vertex(start={self.start}, end={self.end})"

engine = create_engine("sqlite:///../orm.db", echo=True)
Base.metadata.create_all(engine)
