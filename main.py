#Python
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid

#Pydantic
from pydantic import BaseModel
from pydantic import Field

#FastAPI
from fastapi import FastAPI
from fastapi import Body,Query,Path,HTTPException



app = FastAPI()

posts = []


#Models

class Post(BaseModel):
    id: str = Field(
        title= "Id",
        description="Post ID",
    )

    title: str = Field(
        ...,
        min_length= 1,
        max_length= 200,
        title= "Title",
        description="This is the title of the post",
    )

    author: str = Field(
        ...,
        min_length= 1,
        max_length= 100,
        title= "Author",
        description= "This is the Author of the Post",
    )

    content: Text = Field(
        ...,
        min_length= 1,  
        title= "Content",
        description= "This is the content of the Post"
    )

    created_at: datetime = datetime.now()
    published_at : Optional[datetime]
    publisehd: bool = Field(default=None)



@app.get("/")
def home():
    """ This is the Home """
    return {"welcome": "Welcome to my API"}

@app.get("/post")
def get_post():
    return posts 


@app.post("/posts")
def save_post(
    post:Post = Body(
    ...,
    title= "New Post",
    description="This is the body of the new post",
    )
):
    post.id = str(uuid())
    posts.append(post.dict())
    return post


@app.get("/post/{post_id}")
def get_post(
    post_id: str = Path(
    ...,
    title= "Post ID",
    description="This is the id of the Post",
    min_length= 1,
    max_length= 40,
    )
):

    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code= 404, detail="Post not Found")



@app.delete("/post/{post_id}")
def delete_post(
    post_id: str = Path(
        ...,
        title= "Post ID",
        description= "This is the ID of the post to delete",
        min_length= 1,
        max_length=40,
        )
):

    for index,post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Post has been deleted successfully"}

    raise HTTPException(status_code= 404, detail="Post not Found")

@app.put("/post/{post_id}")
def update_post(
    post_id: str = Path(
    ...,
    title= "Post Id",
    description="Id of the publication to update",
    ),

    updated_post: Post = Body(
        ...,
        title= "Updated Post",
        description= "This is the body of the post updated",
    )
):
    for index,post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = updated_post.title
            posts[index]["author"] = updated_post.author
            posts[index]["content"] = updated_post.content
            return {"message": "Post has been updated successfully"}
    raise HTTPException(status_code= 404, detail="Post not Found")