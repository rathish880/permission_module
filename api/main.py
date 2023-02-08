"""Main routes."""

from fastapi import Depends, FastAPI

from .dependencies import get_user
from .reporter.main import router as reporter_router
from .schemas import User

app = FastAPI(title="AURCC API")
app.include_router(reporter_router)


@app.get("/whoami")
def whoami(user: User = Depends(get_user)) -> User:
    """Return the user information of authenticated user."""
    return user
