from datetime import datetime

from sqlalchemy import create_engine, func
from sqlalchemy.orm import Mapped, mapped_column, registry, Session

reg = registry()

@reg.mapped_as_dataclass
class User:
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.utc_timestamp(), default=None
    )


engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5434/test", echo=True)

reg.metadata.create_all(engine)

with Session(engine) as session:
    session.add(User())
    session.commit()
