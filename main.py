from fastapi import FastAPI

from database import initialize_database
from routes.general import router as general_router
from routes.users import router as users_router

initialize_database()
app = FastAPI()

app.include_router(general_router)
app.include_router(users_router)
