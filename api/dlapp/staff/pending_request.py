from fastapi import HTTPException, status
from sqlalchemy import select, update
from sqlalchemy import or_, and_
from datetime import datetime

from ...schemas import Role
from .schemas import HodStatus, DeanStatus
from .models import Permission as PermissionDB
from .models import UserInfo

# from .tasks import send_notification
from .schemas import Designation

departments = ("CSE", "EEE", "ECE", "MECH", "S&H", "MBA")


def pending_requests(user, db):
    if Role.DEAN in user.roles:
        stmt = select(PermissionDB).where(
            and_(
                or_(
                    PermissionDB.hod_status == HodStatus.FORWARD,
                    PermissionDB.hod_status == HodStatus.DIRECT,
                ),
                PermissionDB.dean_status == DeanStatus.PENDING,
            )
        )
        pending_requests = db.execute(stmt).scalars().all()
        return pending_requests

    groups = [group for group in user.groups if Designation.HEADS.value in group]
    pending_requests = []

    if len(groups) == 0:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    for grp in groups:
        department = grp.split("/")[2]
        stmt = select(PermissionDB).where(
            and_(
                PermissionDB.user_group.like(f"%{department}%"),
                PermissionDB.hod_status == HodStatus.PENDING,
            )
        )
        pending_requests.extend(db.execute(stmt).scalars().all())
    return pending_requests


def update_status(permission_id, permission_status, user, db):
    if Role.DEAN in user.roles:
        stmt = (
            update(PermissionDB)
            .where(PermissionDB.permission_id == permission_id)
            .values(dean_status=permission_status, acted_on=datetime.now())
        )
        db.execute(stmt)
        db.commit()
        return True

    groups = [group for group in user.groups if Designation.HEADS.value in group]

    if len(groups) > 0:
        stmt = (
            update(PermissionDB)
            .where(PermissionDB.permission_id == permission_id)
            .values(hod_status=permission_status, acted_on=datetime.now())
        )
        db.execute(stmt)
        db.commit()
        return True
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
