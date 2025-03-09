from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Структуры данных
class User(BaseModel):
    name: str
    job: str

class UserResponse(BaseModel):
    id: int
    name: str
    job: str

users_db = {
    1: {"id": 1, "name": "morpheus", "job": "leader"},
    2: {"id": 2, "name": "neo", "job": "the one"},
}

# Эндпоинты
@app.get("/api/users")
async def get_users():
    return {"data": list(users_db.values())}

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    user = users_db.get(user_id)
    if user:
        return user
    return {"message": "User not found"}, 404

@app.post("/api/users")
async def create_user(user: User):
    user_id = len(users_db) + 1
    users_db[user_id] = user.dict()
    return {"id": user_id, "name": user.name, "job": user.job}

@app.put("/api/users/{user_id}")
async def update_user(user_id: int, user_data: User):
    if user_id in users_db:
        users_db[user_id] = {"id": user_id, "name": user_data.name, "job": user_data.job}
        return {"id": user_id, "name": user_data.name, "job": user_data.job}
    return {"message": "User not found"}, 404

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: int):
    if user_id in users_db:
        del users_db[user_id]
        return {"message": "User deleted"}
    return {"message": "User not found"}, 404

