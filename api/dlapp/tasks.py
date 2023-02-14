"""Contains tasks to be executed for methods."""

import httpx

from ..settings import Settings
from .schemas import Permission


async def send_notification(permission: Permission):
    department = permission.user_group.split("/")[1]
    designation = permission.user_group.split("/")[2]
