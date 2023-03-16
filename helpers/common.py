from fastapi import UploadFile
import shutil
from firebase_admin import storage


def save_file(file: UploadFile, path: str):
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return path


async def save_to_firestore(file: UploadFile, path: str):
    bucket = storage.bucket("dot-share-project.appspot.com")
    blob = bucket.blob(path)
    buffer = await file.read()
    blob.upload_from_string(buffer, content_type=file.content_type)
    blob.make_public()
    return blob.public_url
