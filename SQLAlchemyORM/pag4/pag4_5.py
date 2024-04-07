# from sqlalchemy.orm import DeclarativeBase, registry

# reg = registry()

# class Base(DeclarativeBase):
#     registry = reg
from datetime import datetime
from typing import Optional
from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    fullname: Mapped[Optional[str]]
    nickname: Mapped[Optional[str]] = mapped_column(String(64))
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")

class Address(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="addresses")
