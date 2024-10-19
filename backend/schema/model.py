from sqlalchemy import Integer, String, ForeignKey, select
from sqlalchemy.orm import mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = "contacts"
    id = mapped_column(Integer, primary_key=True)
    fullname = mapped_column(String(255), nullable=False)
    phone_number = mapped_column(String(255), nullable=False)
    user_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)


class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    fullname = mapped_column(String(255), nullable=False)
    email = mapped_column(String(100), nullable=False)
    hashed_password = mapped_column(String(255), nullable=False)
