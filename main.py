from fastapi import FastAPI

from routes.general import router as general_router
from routes.users import router as users_router

app = FastAPI()

app.include_router(general_router)
app.include_router(users_router)
