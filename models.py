from pydantic import BaseModel


class User(BaseModel):
    name: str
    password: str
    age: int

class UserResponse(BaseModel):
    name: str
    age: int
    id: int

class UserUpdate(BaseModel):
    name: str | None = None
    password: str | None = None
    age: int | None = None
