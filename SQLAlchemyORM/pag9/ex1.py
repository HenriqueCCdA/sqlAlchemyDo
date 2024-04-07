from sqlalchemy import Integer, String
from sqlalchemy.orm import validates, DeclarativeBase, mapped_column



class Base(DeclarativeBase):
    pass


class EmailAddress(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    email = mapped_column(String)

    @validates("email")
    def validdate_email(self, key, address):
        if "@" not in address:
            raise ValueError("failed simple email validation")
        return address
