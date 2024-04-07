from dataclasses import dataclass, field
from sqlalchemy import ForeignKey, Column, Integer, String
from sqlalchemy.orm import registry, declared_attr, relationship

mapper_registry = registry()

class RefTargetMixin:
    @declared_attr
    def target_id(cls):
        return Column("target_id", ForeignKey("target.id"))

    @declared_attr
    def target(cls):
        return relationship("Target")


@dataclass
class UserMixin:
    __tablename__ = "user"

    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    addresses: list[Address] = field(default_factory=list, metadata={"sa": lambda: relationship("Address")})


@dataclass
class AddrexMixin:
    __tablename__ = "address"
    __sa_dataclass_metadata_key__ = "sa"
    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})
    user_id: int = field(init=False, metadata={"sa": lambda: Column(ForeignKey("user.id"))})
    email_address: str = field(default=None, metadata={"sa": Column(String(50))})

@mapper_registry.mapped
class Use(UserMixin):
    pass

@mapper_registry.mapped
class Address(AddrexMixin):
    pass
