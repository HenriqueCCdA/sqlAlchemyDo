from uuid import uuid4
from typing import Optional
from sqlalchemy import String
from sqlalchemy.orm import MappedAsDataclass, Mapped, mapped_column, DeclarativeBase

class Mixin(MappedAsDataclass):
    create_user: Mapped[int] = mapped_column()
    update_user: Mapped[Optional[int]] = mapped_column(default=None, init=False)


class Base(DeclarativeBase, MappedAsDataclass):
    pass

class User(Base, Mixin):
    __tablename__ = "sys_user"

    uid: Mapped[str] = mapped_column(
        String(50), init=False, default_factory=uuid4, primary_key=True,
    )

    username: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
