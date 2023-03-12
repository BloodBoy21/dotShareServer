from lib.db import db
from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel


class User(db):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String())
    user_active = Column(Boolean, default=True)


class UserIn(BaseModel):
    username: str
    password: str
    email: str


class UserOut(BaseModel):
    username: str
    email: str
    is_active: bool
