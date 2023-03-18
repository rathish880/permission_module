from fastapi import HTTPException, status
from sqlalchemy import select, delete

from ..schemas import Role

from .models import Permission as PermissionDB
from .schemas import Designation, DeanStatus, HodStatus


def get_history(head, user, db):
    if head and (Role.DEAN in user.roles or Role.HR in user.roles):
        stmt = select(PermissionDB).where(
            PermissionDB.dean_status != DeanStatus.PENDING
        )
        admin_history = db.scalars(stmt).all()
        return admin_history

    elif head:
        group = next(group for group in user.groups if Designation.HEADS.value in group)
        department = group.split("/")[2]
        stmt = select(PermissionDB).where(
            PermissionDB.user_group.in_(department)
            and PermissionDB.hod_status != HodStatus.PENDING
        )
        admin_history = db.scalars(stmt).all()
        return admin_history

    else:
        stmt = select(PermissionDB).where(PermissionDB.user_name == user.name)
        user_history = db.scalars(stmt).all()
        return user_history


def delete_permission(permission_id, user, db):
    if Role.HR not in user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    stmt = select(PermissionDB.dean_status).where(
        PermissionDB.permission_id == permission_id
    )
    dean_status = db.scalars(stmt).first()

    if dean_status != DeanStatus.APPROVED:
        stmt = delete(PermissionDB).where(PermissionDB.permission_id == permission_id)
        db.execute(stmt)
        db.commit()
        return True

    return False


def delete_user_permission(permission_id, user, db):
    if Role.STAFF not in user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    stmt = select(PermissionDB.dean_status).where(
        PermissionDB.permission_id == permission_id
    )
    dean_status = db.scalars(stmt).first()

    if dean_status == DeanStatus.PENDING:
        stmt = delete(PermissionDB).where(PermissionDB.permission_id == permission_id)
        db.execute(stmt)
        db.commit()
        return True
    return False
