# API of AURCC Apps & Services

This repository is the source for the API server located at [api.aurcc.in](api.aurcc.in).
The server is written in Python using FastAPI framework with PostgreSQL for database and Keycloak for user accounts management.

## Install

Clone the repository and install the dependencies namely Keycloak and PostgreSQL. Then install the Python packages.

```bash
$ pip install -r requirements.txt
```

## Environment Variables

The server needs many environment variables to work well.
| Name | Description |
|--------------------------|--------------------------------------------------------------|
| `BOT_TOKEN` | Token of the Telegram bot which sends messages. |
| `DATABASE_URL` | PostgreSQL database URL in the SQLAlchemy compatible format. |
| `KEYCLOAK_CLIENT_ID` | Client ID of the server in Keycloak. |
| `KEYCLOAK_CLIENT_SECRET` | Secret of the server in Keycloak. |
| `KEYCLOAK_SERVER_URL` | URL of the Keycloak service. |
| `KEYCLOAK_REALM_NAME` | Name of the Keycloak realm. |
| `REPORTER_CHAT_ID` | ID of Telegram chat to which messages must be reported. |

## Running

Set the environment variables and start the server using `uvicorn`.

```bash
$ uvicorn api.main:app
```
