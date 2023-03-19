from pydantic import BaseModel, Field
from lib.mongo import database
from datetime import datetime

post_collection = database.get_collection("posts")


class Post(BaseModel):
    title: str = Field(...)
    post_owner: str = None
    banner: str = None
    tags: list = Field(...)
    content: str = Field(...)
    files: list = []
    createdAt: datetime = datetime.now()

    class Config:
        schema_extra = {
            "example": {
                "title": "My first post",
                "post_owner": "username",
                "banner": "https://www.go ogle.com",
                "tags": ["tag1", "tag2"],
                "content": "This is my first post",
                "files": ["https://www.google.com"],
            }
        }


def post_helper(post) -> dict:
    return {
        "id": str(post["_id"]),
        "title": post["title"],
        "post_owner": post["post_owner"],
        "banner": post["banner"],
        "tags": post["tags"],
        "content": post["content"],
        "files": post["files"],
    }


class PostUpdated(BaseModel):
    title: str = None
    banner: str = None
    tags: list = None
    content: str = None
    files: list = None

    def get_update(self):
        return {k: v for k, v in self.dict().items() if v is not None}
