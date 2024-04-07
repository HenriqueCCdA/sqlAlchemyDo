from typing import Optional
from sqlalchemy import ForeignKey, create_engine, String, select
from sqlalchemy.orm import Session, Mapped, mapped_column, DeclarativeBase, relationship, joinedload, contains_eager

engine = create_engine('sqlite:///test.db', echo=True)

class Base(DeclarativeBase):
    ...


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]

    addresses: Mapped[list["Address"]] = relationship(back_populates="user", lazy="raise_on_sql")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))

    user: Mapped[User] = relationship(back_populates="addresses", lazy="raise_on_sql")

    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

squidward = User(name="squidward", fullname="Squidward Tentacles")
krabs = User(name="ehkrabs", fullname="Eugene H. Krabs")

u1 = User(name="pkrabs", fullname="Pearl Krabs")
a1 = Address(email_address="pearl.krabs@gmail.com")
u1.addresses.append(a1)

a2 = Address(email_address="pearl@aol.com", user=u1)

print(select(Address.email_address).select_from(User).join(User.addresses))

print(select(Address.email_address).join_from(User, Address))

session = Session(engine)

from sqlalchemy.orm import selectinload

for user_obj in session.execute(select(User).options(selectinload(User.addresses))).scalars():
    user_obj.addresses

stmt = select(User).options(selectinload(User.addresses)).order_by(User.id)

for row in session.execute(stmt):
    print(f"{row.User.name} ({', '.join(a.email_address for a in row.User.addresses)})")

stmt = select(Address).options(joinedload(Address.user, innerjoin=True)).order_by(Address.id)

for row in session.execute(stmt):
    print(f"{row.Address.email_address} {row.Address.user.name}")
