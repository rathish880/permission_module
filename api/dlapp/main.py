"""Contains routes for DLAPP"""
from datetime import date, datetime, timedelta, timezone
from os import getuid

from fastapi import APIRouter, Depends, HTTPException, status
from starlette.background import BackgroundTask

from ..database import SessionLocal
from ..dependencies import get_db, get_user
from ..schemas import Role, User
from .models import Permission as PermissionDB
from .schemas import Permission, PermissionDetails

router = APIRouter(prefix="/dlapp", tags=["dlapp"])


@router.post(
    "/request",
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is unauthorized"},
    },
    response_model=bool,
)
async def request_permission(
    permission_details: PermissionDetails,
    user: User = Depends(get_user),
    db: SessionLocal = Depends(get_db),
    tasks: BackgroundTask = None,
) -> bool:
    """User request a permission"""

    if Role.STAFF not in user.roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    group = next(group for group in user.groups if Role.STAFF.value in group.lower())

    permission = PermissionDB(
        user_name=user.name,
        user_group=group,
        permission_date=permission_details.permission_date,
        permission_time=permission_details.permission_time,
        reason=permission_details.reason,
    )

    db.add(permission)
    db.commit()

    permission = Permission(
        permission_id=permission.permission_id,
        user_name=permission.user_name,
        user_group=permission.user_group,
        permission_date=permission.permission_date,
        permission_time=permission.permission_time,
        requested_on=permission.requested_on,
        approved_on=permission.approved_on,
        reason=permission.reason,
    )

    tasks.add_task(send_notification, permission)

    return True
