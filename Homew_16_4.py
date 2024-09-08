from fastapi import FastAPI, Body, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="temolat")

users_db = []


class User(BaseModel):
    user_id: int
    username: str
    age: int


@app.get("/")
async def new_zapros(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "users": users_db})


@app.get(path="/users/{user_id}")
async def users_list(request: Request, user_id: int) -> HTMLResponse:
    return templates.TemplateResponse("users.html", {"request": request, "user": users_db[user_id]})


@app.post("/user")
async def user_add(user: User):
    # user_id = len(users_db)
    if users_db:
        user_id = max(users_db, key=lambda x: x.user_id).user_id + 1
    else:
        user_id = 0
    users_db.append(user)
    return user


@app.put("/user/{user_id}")
async def user_update(user_id: int, username: str = Body(...), age: int = Body(...)):
    if user_id >= len(users_db) or user_id < 0:
        raise HTTPException(status_code=404, detail="User not found")
    update_user = users_db[user_id]
    update_user.username = username
    update_user.age = age
    return update_user


@app.delete("/user/{user_id}")
async def user_delete(user_id: int):
    if user_id >= len(users_db) or user_id < 0:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = users_db.pop(user_id)
    return deleted_user


# python -m uvicorn Homew_16_4:app