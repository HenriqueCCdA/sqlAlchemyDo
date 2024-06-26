from __future__ import annotations

from dataclasses import dataclass, field
import email
from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import registry, relationship

from pag1.pag1 import Address

mapper_registry = registry()


@mapper_registry.mapped
@dataclass
class User:
    __table__ = Table(
        "user",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String(50)),
        Column("fullname", String(50)),
        Column("nickname", String(12)),
    )
    id: int = field(init=False)
    name: Optional[str]  = None
    fullname: Optional[str] = None
    nickname: Optional[str] = None
    addresses: list[Address] = field(default_factory=list)

    __mapper_args__ = {
        "properties": {
            "addresses": relationship("Address"),
        }
    }


@mapper_registry.mapped
@dataclass
class Address:
    __table__ = Table(
        "'address",
        mapper_registry.metadata,
        Column("id", Integer, primary_key=True),
        Column("user_id", Integer, String(50))
    )
    id: int = field(init=False)
    user_id: int = field(init=False)
    email_address: Optional[str] = None
