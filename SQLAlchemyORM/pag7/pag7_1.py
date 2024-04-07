from sqlalchemy.orm import Mapped, mapped_column, registry

reg =registry()

# class Base(MappedAsDataclass, DeclarativeBase):
#     ...

# class User(Base):
#     __tablename__ = "user_acount"

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     name: Mapped[str]


@reg.mapped_as_dataclass
class User:
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    fullname: Mapped[str] = mapped_column(default=None)


u1 = User("name")
