from fastapi import APIRouter, Path, Response
from ..import database
from ..jwt import verify_token

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
        query = "SELECT name, post_id, author, created_on, updated_on FROM posts WHERE user_id={};".format(post_id)
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