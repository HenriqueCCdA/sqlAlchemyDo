import dataclasses

from sqlalchemy import Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, composite, mapped_column, CompositeProperty
from sqlalchemy.sql import and_

@dataclasses.dataclass
class Point:
    x: int
    y: int

class Base(DeclarativeBase):
    pass

class PointComparator(CompositeProperty.Comparator):

    def __gt__(self, other):

        return and_(
            *[
                a > b
                for a, b in zip(
                    self.__clause_element__().clauses,
                    dataclasses.astuple(other),
                )
            ]
        )


class Vertex(Base):
    __tablename__ = "vertices"

    id: Mapped[int] = mapped_column(primary_key=True)

    start: Mapped[Point] = composite(mapped_column("x1"), mapped_column("y1"), comparator_factory=PointComparator)
    end: Mapped[Point] = composite(mapped_column("x2"), mapped_column("y2"), comparator_factory=PointComparator)


engine = create_engine("sqlite:///../orm.db", echo=True)
Base.metadata.create_all(engine)
