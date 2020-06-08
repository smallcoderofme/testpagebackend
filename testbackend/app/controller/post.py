from fastapi import APIRouter, Path, Response
from ..import database
from pydantic import BaseModel
from ..jwt import verify_token
import uuid

class Post(BaseModel):
    name: str
    preview: str
    content: str
    author: str
    public: bool
    user_id: str

    def verify(self):
        if not self.name or not self.preview or not self.content or not self.author or not self.user_id:
            return False
        else:
            return True

post_router = APIRouter()

@post_router.get("/posts/", tags=["posts"], responses={404: {"description": "Not found"}})
async def get_review():
    return [{ "name":"Post1" }, {"name": "Post2"}]

@post_router.post('/posts/{post_id}')
async def get_post_detail(post_id: str = Path(..., title="Get post detail of post id.")):
    query = "SELECT name, post_id, author, content, updated_on FROM posts WHERE post_id={}, public={};".format(post_id, True)
    result = await database.fetch_one(query=query)
    if result:
        res = dict(result)
        res["post_id"] = post_id
        return { res }
    else:
        return { "status":"404", "msg":"Not Found." }

@post_router.get("/admin_posts/", tags=["posts"], responses={404: {"description": "Not found"}})
async def get_admin_review(user_id: str, post_id:str, response: Response):
    token = response.headers["Authorization"]
    if token and verify_token(token):
        query = "SELECT name, post_id, author, public, created_on, updated_on FROM posts WHERE user_id={};".format(user_id)
        results = await database.fetch_all(query=query)
        res_lis = []
        for p in results:
            res_lis.append(p)
        return res_lis
    else:
        return { "status":"405", "msg":"Not Authotization." }

@post_router.post('/admin_post/{post_id}')
async def get_admin_post():
    return []

@post_router.post('/posts/create')
async def create_post(new_post: Post, response: Response):
    token = response.headers["Authorization"]
    if token and verify_token(token):
        if new_post.verify():
            query = "INSERT INTO posts (name, post_id, preview, content, public, author, user_id) VALUES ({} {} {} {} {} {} {})".format(new_post.name, uuid.uuid4(), new_post.preview, new_post.content, new_post.public, new_post.author, new_post.user_id)
            results = await database.execute(query)
            print(results)
            return { "status":"ok", "msg":"Created success." }
        else:
            return { "status":"403", "msg":"Param are not enough." } 
    else:
        return { "status":"405", "msg":"Not Authotization." }

@post_router.post('/posts/delete')
async def delete_post(post_id: str, response: Response):
    token = response.headers["Authorization"]
    if token and verify_token(token) and post_id and len(post_id) == 32:
        query = "DELETE FROM posts WHERE post_id={}".format(post_id)
        results = await database.execute(query)
        print(results)
        return { "status":"ok", "msg":"Delete success." }
    else:
        return { "status":"error", "msg":"Required params." }

@post_router.post('/posts/update')
async def update_post(update_post: Post, response: Response):
    token = response.headers["Authorization"]
    if token and verify_token(token):
        if update_post.verify():
            query = "UPDATE posts (name, post_id, preview, content, public, author, user_id) VALUES ({} {} {} {} {} {} {})".format(update_post.name, uuid.uuid4(), update_post.preview, update_post.content, update_post.public, update_post.author, update_post.user_id)
            results = await database.execute(query)
            print(results)
            return { "status":"ok", "msg":"Updated success." }
        else:
            return { "status":"403", "msg":"Param are not enough." } 
    else:
        return { "status":"405", "msg":"Not Authotization." }
