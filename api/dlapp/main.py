"""Contains routes for DLAPP"""
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select

from ..database import SessionLocal
from ..dependencies import get_db, get_user
from ..schemas import Role, User
from .models import Permission as PermissionDB
from .schemas import Designation, Permission, PermissionDetails, Status
from .tasks import send_notification

router = APIRouter(prefix="/dlapp", tags=["dlapp"])
#  WARN: hello


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
    tasks: BackgroundTasks = None,
) -> bool:
    """User request a permission"""

    if Role.STAFF not in user.roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    #  NOTE: this is a note

    permission = PermissionDB(
        user_name=user.name,
        user_group=group,
        permission_date=permission_details.permission_date,
        permission_time=permission_details.permission_time,
        hod_status=Status.PENDING,
        dean_status=Status.PENDING,
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
        hod_status=permission.hod_status,
        dean_status=permission.hod_status,
        approved_on=permission.approved_on,
        reason=permission.reason,
    )

    print(vars(permission))

    tasks.add_task(send_notification, permission)

    return True
