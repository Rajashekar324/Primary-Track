from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import status
from fastapi import HTTPException
from fastapi import Depends
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/users")
def get_users():
    return ["Alice", "Bob"]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get("/search")
def search(q: str, limit: int = 10):
    return {"query": q, "limit": limit}

class User(BaseModel):
    name: str
    age: int

# @app.post("/users")
# def create_user(user: User):
#     return user

@app.post("/test")
def test(data: dict):
    return data

class UserOut(BaseModel):
    name: str

@app.post("/users", response_model=UserOut)
def create_user(user: User):
    return user



@app.post("/login", status_code=status.HTTP_201_CREATED)
def login():
    return {"message": "Created"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id != 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item": "Book"}

def common_params():
    return {"q": "search"}

@app.get("/items")
def read_items(params=Depends(common_params)):
    return params

@app.get("/async")
async def async_example():
    return {"message": "Async works!"}