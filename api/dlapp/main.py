"""Contains routes for DLAPP"""
from datetime import date, datetime, timedelta, timezone
from os import getuid, stat
from ssl import ALERT_DESCRIPTION_PROTOCOL_VERSION

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import desc, select
from sqlalchemy.util import FastIntFlag

from ..database import SessionLocal
from ..dependencies import get_db, get_user
from ..schemas import Role, User
from .models import Permission as PermissionDB
from .schemas import Designation, Permission, PermissionDetails
from .tasks import send_notification

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
    tasks: BackgroundTasks = None,
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
        head_approved=False,
        dean_approved=False,
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
        head_approved=permission.head_approved,
        dean_approved=permission.dean_approved,
        approved_on=permission.approved_on,
        reason=permission.reason,
    )

    print(vars(permission))

    tasks.add_task(send_notification, permission)

    return True


@router.get(
    "/pending",
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is unauthorized"},
    },
    response_model=dict,
)
async def pending_requests(
    user: User = Depends(get_user),
    db: SessionLocal = Depends(get_db),
):
    if Role.DEAN in user.roles:
        stmt = select(PermissionDB).where(PermissionDB.head_approved.__eq__(True))
        pending_requests = db.scalars(stmt).all()
        return pending_requests
    else:
        group = next(
            group for group in user.groups if Designation.HEADS.value in group.lower()
        )
        department = group.split("/")[2]
        stmt = select(PermissionDB).where(PermissionDB.user_group.in_(department))
        pending_requests = db.scalars(stmt).all()
        return pending_requests


@router.get(
    "/history",
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is unauthorized"},
    },
    response_model=dict,
)
async def get_history(
    head: bool,  # head represents hod, unitOfficer, dean
    user: User = Depends(get_user),
    db: SessionLocal = Depends(get_db),
):
    if head and (Role.DEAN in user.roles or Role.HR in user.roles):
        stmt = select(PermissionDB).where(PermissionDB.head_approved.__eq__(True))
        admin_history = db.scalars(stmt).all()
        return admin_history

    elif head:
        group = next(
            group for group in user.groups if Designation.HEADS.value in group.lower()
        )
        department = group.split("/")[2]
        stmt = select(PermissionDB).where(PermissionDB.user_group.in_(department))
        admin_history = db.scalars(stmt).all()
        return admin_history

    else:
        stmt = select(PermissionDB).where(PermissionDB.user_name.__eq__(user.name))
        user_history = db.scalars(stmt).all()
        return user_history
