from fastapi import APIRouter, HTTPException, status

from database import get_connection
from models import User, UserResponse, UserUpdate

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
def register_user(user: User):    
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO users (name, age, password)
            VALUES (?, ?, ?)           
        """, (user.name, user.age, user.password)
        )
        
        user_id = cursor.lastrowid
        
        usr = {"name": user.name, "password": user.password, "age": user.age, "id": (user_id)}    
        
        return usr


@router.get(
    "",
    response_model=list[UserResponse],
    summary="list users",
    description="List all users",
    status_code=status.HTTP_200_OK,
)
def list_users():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users")
        
        rows = cursor.fetchall()
        
        users = []
        for user in rows:
            users.append({"id": user[0], "name": user[1], "age": user[3]})
        
        return users


@router.get(
    "/{id}",
    response_model=UserResponse,
    summary="get user",
    description="Get user data by id",
    status_code=status.HTTP_200_OK,
)
def get_user(id: int):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
        
        user = cursor.fetchone()
        
        if user is not None:
            return {"id": user[0], "name": user[1], "age": user[3]}
    
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"User {id} not found.")


@router.patch(
    "/{id}",
    response_model=UserResponse,
    summary="patch user",
    description="Change user data by id",
    status_code=status.HTTP_200_OK,
)
def patch_user(id: int, user: UserUpdate):
    name = user.name
    age = user.age
    password = user.password
    
    if name is None and age is None and password is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No field to update.")
    
    updates = []
    values = []
    
    if name is not None:
        updates.append("name = ?")
        values.append(name)

    if age is not None:
        updates.append("age = ?")
        values.append(age)

    if password is not None:
        updates.append("password = ?")
        values.append(password)
    
    set_clause = ", ".join(updates)
    
    with get_connection() as connection:
        cursor = connection.cursor()
        
        cursor.execute(f"""
            UPDATE users
            SET {set_clause}
            WHERE id = ?
        """, (*values, id)
        )

        
    return get_user(id)


@router.delete(
    "/{id}",
    response_model=UserResponse,
    summary="remove user",
    description="Delete user data by id",
    status_code=status.HTTP_200_OK,
)
def delete_user(id: int):
    usr = get_user(id)
    
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (id,))
        
        return usr
