from fastapi import APIRouter, HTTPException, status
from pwdlib import PasswordHash

from database import get_connection
from models import UserLogin, UserRegister, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

PASSWORD_HASHER = PasswordHash.recommended()


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
            users.append(
                {"id": user[0], "name": user[1], "username": user[2], "email": user[3]}
            )

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
            return {
                "id": user[0],
                "name": user[1],
                "username": user[2],
                "email": user[3],
            }

    raise HTTPException(status.HTTP_404_NOT_FOUND, f"User {id} not found.")


@router.post(
    "/register",
    response_model=UserResponse,
    summary="register user",
    description="Register a user, give name, username, email and password",
    status_code=status.HTTP_201_CREATED,
)
def register_user(user: UserRegister):
    with get_connection() as connection:
        name = user.name
        username = user.username
        email = user.email

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id FROM users
            WHERE username = ?
            """,
            (username,),
        )
        if cursor.fetchone() is not None:
            raise HTTPException(
                status.HTTP_409_CONFLICT, f"Username '{username}' already exists!"
            )

        cursor.execute(
            """
            SELECT id FROM users
            WHERE email = ?
            """,
            (email,),
        )
        if cursor.fetchone() is not None:
            raise HTTPException(
                status.HTTP_409_CONFLICT, f"Email '{email}' is already used!"
            )

        password = PASSWORD_HASHER.hash(user.password)

        cursor.execute(
            """
            INSERT INTO users (name, username, email, password)
            VALUES (?, ?, ?, ?)           
            """,
            (name, username, email, password),
        )

        user_id = cursor.lastrowid

    return get_user(user_id)


@router.post(
    "/login",
    response_model=UserResponse,
    summary="login",
    description="Login a user, username or email and password needed",
    status_code=status.HTTP_200_OK,
)
def login_user(user: UserLogin):
    with get_connection() as connection:
        login = user.login
        password = user.password

        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, password
            FROM users
            WHERE username = ? OR email = ?
            """,
            (login, login),
        )

        usr = cursor.fetchone()

        if usr is None or not PASSWORD_HASHER.verify(password, usr[1]):
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid credentials!")

        user_id = usr[0]

    return get_user(user_id)


@router.patch(
    "/{id}",
    response_model=UserResponse,
    summary="patch user",
    description="Change user data by id",
    status_code=status.HTTP_200_OK,
)
def patch_user(id: int, user: UserUpdate):
    name = user.name
    username = user.username
    email = user.email
    password = user.password

    if name is None and username is None and email is None and password is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No field to update.")

    updates = []
    values = []

    with get_connection() as connection:
        cursor = connection.cursor()

        if name is not None:
            updates.append("name = ?")
            values.append(name)

        if username is not None:
            cursor.execute(
                """
                SELECT id FROM users
                WHERE username = ? AND id != ?
                """,
                (username, id),
            )
            if cursor.fetchone() is not None:
                raise HTTPException(
                    status.HTTP_409_CONFLICT, f"Username '{username}' already exists!"
                )
            
            updates.append("username = ?")
            values.append(username)

        if email is not None:
            cursor.execute(
                """
                SELECT id FROM users
                WHERE email = ? AND id != ?
                """,
                (email, id),
            )
            if cursor.fetchone() is not None:
                raise HTTPException(
                    status.HTTP_409_CONFLICT, f"Email '{email}' is already used!"
                )
            
            updates.append("email = ?")
            values.append(email)

        if password is not None:
            updates.append("password = ?")
            values.append(PASSWORD_HASHER.hash(user.password))

        set_clause = ", ".join(updates)

        cursor.execute(
            f"""
            UPDATE users
            SET {set_clause}
            WHERE id = ?
            """,
            (*values, id),
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
        cursor.execute(
            """
            DELETE FROM users WHERE id = ?
            """,
            (id,),
        )

        return usr
