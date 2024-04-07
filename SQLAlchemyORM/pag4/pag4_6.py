
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

engine = create_engine("postgresql+psycopg://postgres:postgres@localhost:5434/test", echo=True)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column("user_id", primary_key=True)
    name: Mapped[str] = mapped_column("user_name")


Base.metadata.create_all(engine)
