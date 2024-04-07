from sqlalchemy import MetaData, Integer
from sqlalchemy.orm import registry, mapped_column

reg = registry()

class BaseOne:
    metadata = MetaData()

class BaseTwo:
    metadata = MetaData()


@reg.mapped
class ClassOne:
    __tablename__ = "t1"

    id = mapped_column(Integer, primary_key=True)


@reg.mapped
class ClassTwo(BaseOne):
    __tablename__ = "t1"

    id = mapped_column(Integer, primary_key=True)


@reg.mapped
class ClassThree(BaseTwo):
    __tablename__ = "t1"

    id = mapped_column(Integer, primary_key=True)
