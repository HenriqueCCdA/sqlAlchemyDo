from sqlalchemy import Integer
from sqlalchemy.orm import declarative_mixin, declared_attr, DeclarativeBase, mapped_column

class Base(DeclarativeBase):
    pass

class MySQLSettings:
    __table_args__ = {"mysql_engine": "InnoDB"}

class MyOtherMixin:
    __table_args__ = {"info": "foo"}

class MyModel(MySQLSettings, MyOtherMixin, Base):
    __tablename__ = "my_model"

    @declared_attr.directive
    def __table_args__(cls):
        args = dict()
        args.update(MySQLSettings.__table_args__)
        args.update(MyOtherMixin.__table_args__)
        return args

    id = mapped_column(Integer, primary_key=True)
