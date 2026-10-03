from fastapi import APIRouter, HTTPException, status

from models import User, UserResponse, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

users = []
current_user_id = 0

@router.post(
    "/register",
    response_model=UserResponse,
    summary="register user",
    description="Register a user, give name, password and age",
    status_code=status.HTTP_201_CREATED,
)
def register(user: User):
    global current_user_id
    current_user_id += 1
    
    usr = {"name": user.name, "password": user.password, "age": user.age, "id": (current_user_id)}
    
    users.append(usr)
    
    return usr


@router.get(
    "",
    response_model=list[UserResponse],
    summary="list users",
    description="List all users",
    status_code=status.HTTP_200_OK,
)
def list_users():
    return users


@router.get(
    "/{id}",
    response_model=UserResponse,
    summary="get user",
    description="Get user data by id",
    status_code=status.HTTP_200_OK,
)
def get_user(id: int):
    for user in users:
        if user["id"] == id:
            return user
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"User {id} not found.")


@router.patch(
    "/{id}",
    response_model=UserResponse,
    summary="patch user",
    description="Change user data by id",
    status_code=status.HTTP_200_OK,
)
def patch_user(id: int, user: UserUpdate):
    usr = get_user(id)
    
    if user.name is not None:
        usr["name"] = user.name
    
    if user.password is not None:
        usr["password"] = user.password
    
    if user.age is not None:
        usr["age"] = user.age
    
    return usr


@router.delete(
    "/{id}",
    response_model=UserResponse,
    summary="remove user",
    description="Delete user data by id",
    status_code=status.HTTP_200_OK,
)
def delete_user(id: int):
    usr = get_user(id)
    
    users.remove(usr)
    
    return usr