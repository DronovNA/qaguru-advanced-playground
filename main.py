import json
import uvicorn
from fastapi import FastAPI
from app.routes import router
from fastapi_pagination import add_pagination

app = FastAPI()
app.include_router(router)
add_pagination(app)


if __name__ == "__main__":
    with open("users.json") as f:
        users = json.load(f)

    print("Users loaded")

    uvicorn.run(app, host="localhost", port=8000)
