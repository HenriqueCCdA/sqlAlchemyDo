from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Table, event
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import registry, relationship, Session

class Base(DeclarativeBase):
    pass


# class User(Base):
#     __tablename__ = "user"

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str]
#     fullname: Mapped[str] = mapped_column(String(30))
#     nickname: Mapped[Optional[str]]


mapper_registry = registry()

user = Table(
    "user",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)

address = Table(
    "address",
    mapper_registry.metadata,
    Column("id", Integer, ForeignKey("user.id")),
    Column("email_address", String(50)),
)

class User:
    pass

class Address:
    pass

mapper_registry.map_imperatively(
    User,
    user,
    properties={
        "addresses": relationship(Address, backref="user", order_by=address.c.id)
    },
)

# mapper_registry.map_imperatively(Address, address)


class Point(Base):
    __tablename__ = "point"

    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[int]
    y: Mapped[int]

    @property
    def x_plus_y(self):
        return self.x + self.y


class Point2(Base):
    __tablename__ = "point2"

    id: Mapped[int] = mapped_column(primary_key=True)
    x: Mapped[int]
    y: Mapped[int]

    def __init__(self, x, y, **kw):
        super().__init__(x=x, y=y, **kw)
        self.x_plus_y = x + y


@event.listens_for(Point2, "load")
def receive_load(target, context):
    print("oi")
    target.x_plus_y = target.x + target.y
