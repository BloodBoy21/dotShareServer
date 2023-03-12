from fastapi import APIRouter, HTTPException
from models.user import UserOut, UserIn, User
from lib.db import get_db
from pydantic import BaseModel
import bcrypt
import jwt
import os
import datetime
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_DAYS = 30

jwt_secret = os.environ.get("JWT_SECRET")
db = get_db()
api = APIRouter(
    prefix="/api/v1",
)


class UserLogin(BaseModel):
    username: str
    password: str


def create_token(user):
    payload = {
        "sub": user.username,
        "exp": datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    }
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}


@api.post("/signup")
async def signup(user: UserIn):
    try:
        user_password = bcrypt.hashpw(
            user.password.encode("utf-8"),
            bcrypt.gensalt())
        new_user = User(
            username=user.username,
            password=user_password.decode("utf-8"),
            email=user.email,
        )
        db.add(new_user)
        db.commit()
        user = UserOut(
            username=user.username, email=user.email,
            is_active=True
        )
        return create_token(user)
    except Exception as error:
        print(error)
        raise HTTPException(status_code=400, detail=str(error))


@api.post("/login", response_model=UserOut)
async def login(user: UserLogin):
    login_user = db.query(User).filter(User.username == user.username).first()
    if login_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    shoud_login = bcrypt.checkpw(
        user.password.encode("utf-8"), login_user.password.encode("utf-8")
    )
    if shoud_login:
        user_out = UserOut(
            username=login_user.username, email=login_user.email,
            is_active=True
        )
        return create_token(user_out)
