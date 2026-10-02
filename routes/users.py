from fastapi import APIRouter, status

from models import User, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post(
    "/register",
    response_model=UserResponse,
    summary="register user",
    description="Register a user, give name, password and age",
    status_code=status.HTTP_201_CREATED,
)
def register(user: User):
    return {"name": user.name, "password": user.password, "age": user.age}
