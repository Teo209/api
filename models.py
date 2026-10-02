from pydantic import BaseModel


class User(BaseModel):
    name: str
    password: str
    age: int

class UserResponse(BaseModel):
    name: str
    age: int