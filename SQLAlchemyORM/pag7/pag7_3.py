from typing import Annotated

from sqlalchemy.orm import Mapped, mapped_column, registry

inptk = Annotated[int, mapped_column(init=False, primary_key=True)]

reg = registry()


@reg.mapped_as_dataclass
class User:
    __tablename__ = "user_account"
    id: Mapped[inptk] = mapped_column(init=False)

u1 = User()
