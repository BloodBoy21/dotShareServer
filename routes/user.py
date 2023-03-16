from fastapi import APIRouter, HTTPException, Depends, Request, File, UploadFile
from middleware.auth import auth_user
from helpers.common import save_to_firestore
from helpers.user import update_profile_picture

profilePath = "pictures/profile/"
user = APIRouter(
    prefix="/user",
)

one_mb = 1024 * 1024
MAX_FILE_SIZE = one_mb * 5


@user.post("/upload_avatar")
async def update_avatar(
    user=Depends(auth_user),
    file: UploadFile = File(..., content_type=["image/jpeg", "image/png"]),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Not an image")
    ext = file.filename.split(".")[-1]
    filename = f"{user.username}.{ext}"
    path = profilePath + filename
    url = await save_to_firestore(file, path)
    update_profile_picture(user.username, url)
    return {"url": url}
