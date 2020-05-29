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
        if !self.name or !self.preview or !self.content or !self.author or !self.user_id:
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
async def create_post(new_post: Postr, esponse: Response):
    if token and verify_token(token):
        if new_post.verify():
            query = "INSERT INTO posts (name, post_id, preview, content, public, author, user_id) VALUES ({} {} {} {} {} {} {})"
            .format(new_post.name, uuid.uuid4(), new_post.preview, new_post.content, new_post.public, new_post.author, new_post.user_id)
            results = await database.execute(query)
            return { "status":"ok", "msg":"Created success." }
        else:
            return { "status":"403", "msg":"Param are not enough." } 
    else:
        return { "status":"405", "msg":"Not Authotization." }