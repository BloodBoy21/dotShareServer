from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
import jwt
import os
from helpers.user import get_user_by_id

JWT_SECRET = os.environ.get("JWT_SECRET")

oauth2_scheme = HTTPBearer()


async def auth_user(token: str = Depends(oauth2_scheme)):
    token = token.credentials
    if token is None:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = get_user_by_id(payload.get("sub"))
        return user
    except Exception as error:
        print(error)
        raise HTTPException(status_code=401, detail="Unauthorized")
