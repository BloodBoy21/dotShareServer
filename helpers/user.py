from fastapi import HTTPException
from lib.db import get_db
from models.user import User

db = get_db()


def get_user_by_id(user_id: str):
    user = db.query(User).filter(User.user_id == user_id).first()
    if user is None:
        raise Exception("User not found")
    return user


def get_user(username: str):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise Exception("User not found")
    return user


def update_profile_picture(username: str, url: str):
    user = get_user(username)
    user.profile_picture = url
    return upadte_user(user)


def upadte_user(user):
    try:
        db.add(user)
        db.commit()
        return user
    except Exception as error:
        print(error)
        raise HTTPException(status_code=400, detail=str(error))
