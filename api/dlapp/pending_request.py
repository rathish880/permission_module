from fastapi import HTTPException, status
from sqlalchemy import select, update

from ..schemas import Role
from .schemas import HodStatus
from .models import Permission as PermissionDB

# from .tasks import send_notification
from .schemas import Designation

departments = ["CSE", "EEE", "ECE", "MECH", "S&H", "MBA"]


def pending_requests(user, db):
    if Role.DEAN in user.roles:
        stmt = select(PermissionDB).where(
            PermissionDB.head_status == HodStatus.FORWARD
            or PermissionDB.hod_status == HodStatus.DIRECT
        )
        pending_requests = db.execute(stmt).scalars().all()
        return pending_requests

    # TODO: find group according to the parameter 'user'
    groups = [group for group in user.groups if Designation.HEADS.value in group]

    if len(groups) > 0:
        for grp in groups:
            dept = grp.split("/")[2]
            if dept in departments:
                department = dept
                break

        stmt = select(PermissionDB).where(
            PermissionDB.user_group.like(f"%{department}%")
        )
        pending_requests = db.execute(stmt).scalars().all()
        return pending_requests
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


def update_status(permission_id, permission_status, user, db):
    if Role.DEAN in user.roles:
        stmt = (
            update(PermissionDB)
            .where(PermissionDB.permission_id == permission_id)
            .values(dean_status=permission_status)
        )
        db.execute(stmt)
        db.commit()
    return True

    groups = [group for group in user.groups if Designation.HEADS.value in group]

    if len(groups) > 0:
        stmt = (
            update(PermissionDB)
            .where(PermissionDB.permission_id == permission_id)
            .values(hod_status=permission_status)
        )
        db.execute(stmt)
        db.commit()
        return True
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
