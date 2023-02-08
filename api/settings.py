"""Contains Settings instance."""
from pydantic import BaseSettings


class _Settings(BaseSettings):
    """Settings for the application."""

    BOT_TOKEN: str
    DATABASE_URL: str
    KEYCLOAK_CLIENT_ID: str
    KEYCLOAK_CLIENT_SECRET: str
    KEYCLOAK_SERVER_URL: str
    KEYCLOAK_REALM_NAME: str
    REPORTER_CHAT_ID: int


Settings = _Settings()
