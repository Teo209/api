from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import initialize_database
from routes.general import router as general_router
from routes.users import router as users_router

initialize_database()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://site.piton.ddns.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(general_router)
app.include_router(users_router)

