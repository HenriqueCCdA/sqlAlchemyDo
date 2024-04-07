from sqlalchemy import Integer, String, create_engine, func, select
from sqlalchemy.orm import DeclarativeBase, mapped_column, Session, synonym
from sqlalchemy.ext.hybrid import hybrid_property



class Base(DeclarativeBase):
    pass


class MyClass(Base):
    __tablename__ = "my_table"

    id = mapped_column(Integer, primary_key=True)
    status = mapped_column(String(50))

    @property
    def job_status(self):
        return "Status: " + self.status

    job_status = synonym("status", descriptor=job_status)


engine = create_engine("sqlite:///orm.db", echo=True)
Base.metadata.create_all(engine)
session = Session(engine)
