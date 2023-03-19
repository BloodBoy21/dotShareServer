from fastapi import APIRouter, HTTPException, Depends, Request, File, UploadFile, Query
from middleware.auth import auth_user
from helpers.common import save_to_firestore
from models.mongo.post import Post, post_helper, post_collection, PostUpdated
from pydantic import BaseModel
import bson

post = APIRouter(
    prefix="/post",
)


class PostCreated(BaseModel):
    id: str


class PostFilters(BaseModel):
    post_owner: str = None
    tags: str = None
    startDate: str = None
    endDate: str = None
    _query: dict = {}

    def get_query(self):
        return self.__by_owner().__by_tags().__by_date()._query

    def __by_owner(self):
        if self.post_owner is None:
            return self
        self._query.update({"post_owner": self.post_owner})
        return self

    def __by_tags(self):
        if self.tags is None:
            return self
        self._query.update({"tags": {"$in": self.tags.split(",")}})
        return self

    def __by_date(self):
        hasDates = self.startDate is not None and self.endDate is not None
        if not hasDates:
            return self
        self._query.update(
            {"createdAt": {"$gte": self.startDate, "$lte": self.endDate}}
        )
        return self

    def __doc__(self):
        return "Filters posts by owner, tags and date"


@post.post("/", response_model=PostCreated, description="Create a new post")
async def create_post(user=Depends(auth_user), post: Post = None):
    post_owner = user.user_id
    post.post_owner = post_owner
    post_saved = await post_collection.insert_one(post.dict())
    post_id = str(post_saved.inserted_id)
    return PostCreated(id=post_id)


@post.get("/", description="Get all posts and filter by owner, tags and date")
async def get_all_posts(request: Request):
    filters = PostFilters(**request.query_params)
    query = filters.get_query() if filters else {}
    print(query)
    post = post_collection.find(query)
    return [post_helper(post) for post in await post.to_list(length=100)]


@post.patch("/{post_id}", description="Update a post")
async def update_post(post_id: str, post: PostUpdated = None, user=Depends(auth_user)):
    get_old_post = await post_collection.find_one({"_id": bson.ObjectId(post_id)})
    get_old_post = post_helper(get_old_post)
    if get_old_post.get("post_owner") != user.user_id:
        raise HTTPException(status_code=401, detail="Not allowed to update this post")
    res = await post_collection.update_one(
        {"_id": bson.ObjectId(post_id)}, {"$set": post.get_update()}
    )
    return {"updated": res.modified_count}


@post.delete("/{post_id}", description="Delete a post")
async def delete_post(post_id: str, user=Depends(auth_user)):
    get_post = await post_collection.find_one({"_id": bson.ObjectId(post_id)})
    get_post = post_helper(get_post)
    if get_post.get("post_owner") != user.user_id:
        raise HTTPException(status_code=401, detail="Not allowed to delete this post")
    await post_collection.delete_one({"_id": bson.ObjectId(post_id)})
    return {"deleted": True}
