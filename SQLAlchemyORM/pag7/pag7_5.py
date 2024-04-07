from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship


reg = registry()


@reg.mapped_as_dataclass
class Parent:
    __tablename__ = "parent"
    id: Mapped[int] = mapped_column(primary_key=True)
    children: Mapped[list["Child"]] = relationship(
        default_factory=list, back_populates="parent"
    )


@reg.mapped_as_dataclass
class Child:
    __tablename__ = "child"
    id: Mapped[int] = mapped_column(primary_key=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
    parent: Mapped["Parent"] = relationship(default=None)
