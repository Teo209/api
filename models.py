from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    name: str = Field(min_length=1)
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=4)

class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr

class UserLogin(BaseModel):
    login: str | EmailStr
    password: str

class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1)
    username: str | None = Field(None, min_length=3)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=4)
