from pydantic import BaseModel, Field


class User(BaseModel):
    name: str
    password: str = Field(min_length=4)
    age: int

class UserResponse(BaseModel):
    name: str
    age: int
    id: int


class UserLogin(BaseModel):
    name: str
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    password: str | None = Field(None, min_length=4)
    age: int | None = None
