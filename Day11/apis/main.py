from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Fake database
users = []

# Schema (data shape)
class User(BaseModel):
    id: int
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str


@app.post("/users", status_code=201)
def create_user(user: UserCreate):
    user_id = len(users) + 1
    new_user = User(id=user_id, name=user.name, email=user.email)
    users.append(new_user)
    return new_user

@app.get("/users")
def get_users():
    return users


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: UserCreate):
    for user in users:
        if user.id == user_id:
            user.name = updated_user.name
            user.email = updated_user.email
            return user
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")
