from typing import Optional
from sqlalchemy import ForeignKey, literal_column, select, create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import Session, Mapped, mapped_column, DeclarativeBase, relationship

engine = create_engine('sqlite:///test.db', echo=False)

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

stmt = select(user_table).where(user_table.c.name == "spongebob")
print(stmt)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)



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

stmt = select(User).where(User.name == "spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)

print(select(user_table))

print(select(user_table.c.name, user_table.c.fullname))

print(select(user_table.c["name", "fullname"]))

row = session.execute(select(User)).first()
print(row)

user = session.scalars(select(User)).first()
print(user)

row = session.execute(select(User.name, User.fullname)).first()
print(row)

r = session.execute(
    select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
).all()

print(r)

stmt = select(
    ("Username: " + user_table.c.name).label("username"),
).order_by(user_table.c.name)
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(f"{row.username}")

stmt = select(literal_column("'some phrase'").label("p"), user_table.c.name).order_by(user_table.c.name)

with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(f"{row.p}, {row.name}")

from sqlalchemy import func, desc

stmt = (
    select(Address.user_id, func.count(Address.id).label("num_addresses"))
    .group_by("user_id")
    .order_by("user_id", desc("num_addresses"))
)
print(stmt)

user_alias_1 = user_table.alias()
user_alias_2 = user_table.alias()

print(
    select(user_alias_1.c.name, user_alias_2.c.name).join_from(
        user_alias_1, user_alias_2, user_alias_1.c.id > user_alias_2.c.id
    )
)

from sqlalchemy.orm import aliased
address_alias_1 = aliased(Address)
address_alias_2 = aliased(Address)

print(
    select(User)
    .join_from(User, address_alias_1)
    .where(address_alias_1.email_address == "patrick@aol.com")
    .join_from(User, address_alias_2)
    .where(address_alias_2.email_address == "patrick@gmail.com")
)


subq = (
    select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
    .group_by(address_table.c.user_id)
    .subquery()
)
print(subq)

print(select(subq.c.user_id, subq.c.count))

print("----")

stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(user_table, subq)
print(stmt)

print("----")

subq = (
    select(func.count(address_table.c.id).label("count"), address_table.c.user_id)
    .group_by(address_table.c.user_id)
    .cte()
)

stmt = select(user_table.c.name, user_table.c.fullname, subq.c.count).join_from(user_table, subq)

print(stmt)

print("----")
subq = select(Address).where(~Address.email_address.like("%@aol.com")).subquery()
address_subq = aliased(Address,  subq)
stmt = (
    select(User, address_subq)
    .join_from(User, address_subq)
    .order_by(User.id, address_subq.id)
)

with Session(engine) as session:
    for user, address in session.execute(stmt):
        print(f"{user} {address}")
print("----")

subq = (
    select(func.count(address_table.c.id))
    .where(user_table.c.id == address_table.c.user_id)
    .scalar_subquery()
)

print(subq)

print(subq == 5)

stmt = select(user_table.c.name, subq.label("address_count"))
print(stmt)

print("----")
subq = (
    select(
        func.count(address_table.c.id).label("address_count"),
        address_table.c.email_address,
        address_table.c.user_id,
    )
    .where(user_table.c.id == address_table.c.user_id)
    .lateral()
)

stmt = (
    select(user_table.c.name, subq.c.address_count, subq.c.email_address)
    .join_from(user_table, subq)
    .order_by(user_table.c.id, subq.c.email_address)
)
print(stmt)

print("----")

from sqlalchemy import union_all
stmt1 = select(user_table).where(user_table.c.name == "sandy")
stmt2 = select(user_table).where(user_table.c.name == "spongebob")

u = union_all(stmt1, stmt2)

with engine.connect() as conn:
    result = conn.execute(u)
    print(result.all())

print("----")

u_subq = u.subquery()

stmt = (
    select(u_subq.c.name, address_table.c.email_address)
    .join_from(address_table, u_subq)
    .order_by(u_subq.c.name, address_table.c.email_address)
)

with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())

print("----")
stmt1 = select(User).where(user.name == "sandy")
stmt2 = select(User).where(user.name == "spongebob")

u = union_all(stmt1, stmt2)

orm_stmt = select(User).from_statement(u)
with Session(engine) as session:
    for obj in session.execute(orm_stmt).scalars():
        print(obj)
print("----")

user_alias = aliased(User, u.subquery())
orm_stmt = select(user_alias).order_by(user_alias.id)
with Session(engine) as session:
    for obj in session.execute(orm_stmt).scalars():
        print(obj)

print("----")

subq = (
    select(func.count(address_table.c.id))
    .where(user_table.c.id == address_table.c.user_id)
    .group_by(address_table.c.user_id)
    .having(func.count(address_table.c.id) > 1)
).exists()

with engine.connect() as conn:
    result = conn.execute(select(user_table.c.name).where(subq))
    print(result.all())

print("-----")

subq = (
    select(address_table.c.id).where(user_table.c.id == address_table.c.user_id)
).exists()

with engine.connect() as conn:
    result = conn.execute(select(user_table.c.name).where(~subq))
    print(result.all())

print("-----")

print(select(func.count()).select_from(user_table))

print(select(func.lower("A String With Much UPPERCASE")))

stmt = select(func.now())
with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())

print("-----")


stmt = (
    select(
        func.row_number().over(partition_by=user_table.c.name),
        user_table.c.name,
        address_table.c.email_address,
    )
    .select_from(user_table)
    .join(address_table)
)

with engine.connect() as conn:
    result = conn.execute(stmt)
    print(result.all())
