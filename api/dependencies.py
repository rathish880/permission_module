"""Contains the dependencies."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from keycloak import KeycloakOpenID

from .database import Base, engine
from sqlalchemy.orm import Session

from .schemas import User
from .settings import Settings

Base.metadata.create_all(bind=engine)

keycloak = KeycloakOpenID(
    server_url=Settings.KEYCLOAK_SERVER_URL,
    realm_name=Settings.KEYCLOAK_REALM_NAME,
    client_id=Settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=Settings.KEYCLOAK_CLIENT_SECRET,
)
scheme = HTTPBearer()


def get_db():
    """Get a database session."""
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


async def get_user(token: HTTPAuthorizationCredentials = Depends(scheme)) -> User:
    """Get the user of the given token."""

    info = keycloak.introspect(token.credentials)
    if not info["active"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    userinfo = keycloak.userinfo(token.credentials)
    user = User(
        user_id=info["sub"],
        name=info["name"],
        roles=info["realm_access"]["roles"],
        groups=userinfo["groups"],
    )
    return user
