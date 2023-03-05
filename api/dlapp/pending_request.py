from fastapi import HTTPException, status
from sqlalchemy import select, update

from ..schemas import Role
from .models import Permission as PermissionDB

# from .tasks import send_notification
from .schemas import Designation


def pending_requests(user, db):
    if Role.DEAN in user.roles:
        stmt = select(PermissionDB).where(PermissionDB.head_approved.__eq__(True))
        pending_requests = db.scalars(stmt).all()
        return pending_requests
    else:
        group = next(
            group for group in user.groups if Designation.HEADS.value in group.lower()
        )
        department = group.split("/")[2]
        stmt = select(PermissionDB).where(
            PermissionDB.c.user_group.icontains(department)
        )
        pending_requests = db.scalars(stmt).all()
        return pending_requests


def update_status(permission_id, permission_status, user, db):
    if Role.DEAN in user.roles:
        update(PermissionDB).where(
            PermissionDB.c.permission_id == permission_id
        ).values(dean_status=permission_status)
        return True

    for group in user.groups:
        if "Heads" in group:
            update(PermissionDB).where(
                PermissionDB.c.permission_id == permission_id
            ).values(hod_status=permission_status)
            return True
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return False
