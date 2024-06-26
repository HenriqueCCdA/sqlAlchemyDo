from dataclasses import dataclass, field
from sqlalchemy import ForeignKey, Column, Integer, MetaData, String, Table
from sqlalchemy.orm import registry, relationship

mapper_registry = registry()


@dataclass
class Address:
    id: int = field(init=False)
    user_id: int = field(init=False)
    email_address: str = None


@dataclass
class User:
    id: int = field(init=False)
    name: str = None
    fullname: str = None
    nickname: str = None
    addresses: list[Address] = field(default_factory=list)


metadata_obj = MetaData()

user = Table(
    "user",
    metadata_obj,
    Column("id", Integer,  primary_key=True),
    Column("name", String(50)),
    Column("fullname", String(50)),
    Column("nickname", String(12)),
)

address = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("email_address", String(50)),
)

mapper_registry.map_imperatively(
    User,
    user,
    properties={
        "addresses": relationship(Address, backref="user", order_by=address.c.id)
    },
)

mapper_registry.map_imperatively(Address, address)
