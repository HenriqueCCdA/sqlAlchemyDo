from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column, relationship

class Base(DeclarativeBase):

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    __table_args__ = {"mysql_engine": "InnoDB"}
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True)


class HasLogRecord:

    log_record_id: Mapped[int] = mapped_column(ForeignKey("logrecord.id"))

    @declared_attr
    def log_record(self) -> Mapped["LogRecord"]:
        return relationship("LogRecord")

class LogRecord(Base):
    log_info: Mapped[str]

class MyModel(HasLogRecord, Base):
    name: Mapped[str]
