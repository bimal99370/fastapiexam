from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


database = [
    {"title": "First Post", "content": "This is the content of the first post."},
    {"title": "Second Post", "content": "This is the content of the second post."}
]


@app.get("/postlists/", response_model=List[Post])
async def get_posts():
    return database


@app.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: int):
    if post_id < 0 or post_id >= len(database):
        raise HTTPException(status_code=404, detail="Post not found")
    return database[post_id]


@app.post("/posts/")
async def create_post(post: Post):
    database.append(post.dict())
    return post


@app.put("/posts/{post_id}")
async def update_post(post_id: int, post: Post):
    if post_id < 0 or post_id >= len(database):
        raise HTTPException(status_code=404, detail="Post not found")
    database[post_id] = post.dict()
    return {"message": "Post updated successfully"}


@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    if post_id < 0 or post_id >= len(database):
        raise HTTPException(status_code=404, detail="Post not found")
    del database[post_id]
    return {"message": "Post deleted successfully"}
