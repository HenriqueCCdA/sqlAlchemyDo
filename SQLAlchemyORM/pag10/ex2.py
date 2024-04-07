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

    id = mapped_column(Integer, primary_key=True)

    x1 = mapped_column(Integer)
    y1 = mapped_column(Integer)
    x2 = mapped_column(Integer)
    y2 = mapped_column(Integer)

    start = composite(Point, x1, y1)
    end = composite(Point, x2, y2)

engine = create_engine("sqlite:///../orm.db", echo=True)
Base.metadata.create_all(engine)
