from dataclasses import InitVar
from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, registry

reg =  registry()


@reg.mapped_as_dataclass
class User:
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]

    password: InitVar[str]
    repeat_password: InitVar[str]

    password_hash: Mapped[str] = mapped_column(init=False, nullable=False)

    def __post_init__(self, password: str, repeat_password: str):
        if password != repeat_password:
            raise ValueError("passwords do not match")
