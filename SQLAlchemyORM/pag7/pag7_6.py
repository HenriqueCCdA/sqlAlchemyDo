from typing import Optional
from sqlalchemy.orm import registry, mapped_column, Mapped


reg = registry()

@reg.mapped_as_dataclass
class Data:
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    status: Mapped[str]

    ctrl_one: Optional[str] = None
    ctrl_two: Optional[str] = None
