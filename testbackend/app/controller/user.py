from fastapi import APIRouter, Response
from pydantic import BaseModel
from ..security import generate_password_hash, check_password_hash
from ..models.model import users
from .. import database
import uuid
from datetime import datetime
from ..jwt import generate_token

class User(BaseModel):
    username: str
    password: str


user_router = APIRouter()

@user_router.post("/login/")
async def login(body_item: User, response: Response):
    print('----username:', body_item.username)
    query = "SELECT username, password_hash, user_id FROM users;"
    results = await database.fetch_all(query=query)
    print('------', dict(results[0]))
    for u in results:
        user = dict(u)
        if check_password_hash(user['password_hash'], body_item.password):
            token = generate_token()
            response.headers["x-xsrf-token"] = token
            return {"status":"ok","uname": body_item.username, "user_id": user['user_id']}
    return { "status":"error", "msg":"username or password error." }


@user_router.post("/register/", tags=["authorization"])
async def register(user: User):
    query = users.insert(None).values(
        username=user.username,
        password_hash=generate_password_hash(user.password),
        user_id=uuid.uuid4().hex,
        created_on=datetime.now(),
        updated_on=datetime.now())
    rp = await database.execute(query)
    print('result:', rp, user.username, user.password)
    return { "status":"ok", "redirect":"login" }