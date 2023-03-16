"""Main routes."""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import get_user
from .ausmart.main import router as reporter_router
from .dlapp.main import router as dlapp_router
from .schemas import User

app = FastAPI(title="AURCC API")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://172.17.2.228:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(reporter_router)
app.include_router(dlapp_router)


@app.get("/whoami")
def whoami(user: User = Depends(get_user)) -> User:
    """Return the user information of authenticated user."""
    return user
