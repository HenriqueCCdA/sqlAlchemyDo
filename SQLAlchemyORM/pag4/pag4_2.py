from decimal import Decimal

from typing import Annotated
from sqlalchemy import Numeric, String
from sqlalchemy.schema import CreateTable
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

str_30 = Annotated[str, 30]
str_50 = Annotated[str, 50]
num_12_4 = Annotated[Decimal, 12]
num_6_2 = Annotated[Decimal, 6]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_30: String(30),
        str_50: String(50),
        num_12_4: Numeric(12, 4),
        num_6_2: Numeric(6, 2),
    }

class SomeClass(Base):
    __tablename__ = "some_table"

    short_name: Mapped[str_30] = mapped_column(primary_key=True)
    long_name: Mapped[str_50]
    num_value: Mapped[num_12_4]
    short_num_value: Mapped[num_6_2]

print(CreateTable(SomeClass.__table__))
