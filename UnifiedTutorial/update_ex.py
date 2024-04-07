from typing import Optional
from sqlalchemy import ForeignKey, literal_column, select, create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import Session, Mapped, mapped_column, DeclarativeBase, relationship

engine = create_engine('sqlite:///test.db', echo=True)

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)

address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)


class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[list["Address"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))

    user: Mapped[User] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

from sqlalchemy import update

stmt = (
    update(user_table)
    .where(user_table.c.name == "patrick")
    .values(fullname="Patrick the Star")
)

print(stmt)

stmt = update(user_table).values(fullname="Username: " + user_table.c.name)
print(stmt)

from sqlalchemy import bindparam

stmt = (
    update(user_table)
    .where(user_table.c.name == bindparam("oldname"))
    .values(name=bindparam("newname"))
)

with engine.begin() as conn:
    conn.execute(
        stmt,
        [
            {"oldname": "jack", "newname": "ed"},
            {"oldname": "sandy", "newname": "mary"},
            {"oldname": "jim", "newname": "jake"},
        ]
    )

scalar_subq = (
    select(address_table.c.email_address)
    .where(address_table.c.user_id == user_table.c.id)
    .order_by(address_table.c.id)
    .limit(1)
    .scalar_subquery()
)

update_stmt = update(user_table).values(fullname=scalar_subq)
print(update_stmt)

from sqlalchemy import delete

stmt =  delete(user_table).where(user_table.c.name == "patrick")
print(stmt)

delete_stmt = (
    delete(user_table)
    .where(user_table.c.id == address_table.c.user_id)
    .where(address_table.c.email_address == "patrick@aol.com")
)

from sqlalchemy.dialects import mysql

print(delete_stmt.compile(dialect=mysql.dialect()))

with engine.begin() as conn:
    result = conn.execute(
        update(user_table)
        .values(fullname="Patrick McStar")
        .where(user_table.c.name == "patrick")
    )
    print(result.rowcount)
