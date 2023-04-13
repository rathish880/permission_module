from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy import and_

from ...schemas import Role

from .models import Permission as PermissionDB
from .schemas import Designation, DeanStatus, HodStatus

departments = ("CSE", "EEE", "ECE", "MECH", "S&H", "MBA")


def get_history(designation, user, db):
    if Role.DEAN in user.roles or (Role.HR in user.roles and designation == "hr"):
        stmt = select(PermissionDB).where(
            PermissionDB.dean_status != DeanStatus.PENDING
        )
        admin_history = db.scalars(stmt).all()
        return admin_history

    groups = [group for group in user.groups if Designation.HEADS.value in group]

    if designation == "user":
        stmt = select(PermissionDB).where(PermissionDB.user_id == user.user_id)
        user_history = db.scalars(stmt).all()
        return user_history

    if designation == "hod":
        for grp in groups:
            dept = grp.split("/")[2]
            if dept in departments:
                department = dept
                break

    elif designation == "unit":
        for grp in groups:
            dept = grp.split("/")[2]
            if dept not in departments:
                department = dept
                break

    stmt = select(PermissionDB).where(
        and_(
            PermissionDB.user_group.like(f"%{department}%"),
            PermissionDB.hod_status.in_([HodStatus.FORWARD, HodStatus.DENIED]),
        )
    )
    admin_history = db.scalars(stmt).all()
    return admin_history


def hr_delete_permission(permission_id, user, db):
    if Role.HR not in user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    stmt = select(PermissionDB.dean_status).where(
        PermissionDB.permission_id == permission_id
    )
    dean_status = db.scalars(stmt).first()

    if dean_status != DeanStatus.PENDING:
        stmt = delete(PermissionDB).where(PermissionDB.permission_id == permission_id)
        db.execute(stmt)
        db.commit()
        return True

    return False


def user_delete_permission(permission_id, user, db):
    if Role.STAFF not in user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    # TODO: have to check whether this logic works as exepected

    # stmt = select(PermissionDB.dean_status).where(
    #     PermissionDB.permission_id == permission_id
    # )
    # dean_status = db.scalars(stmt).first()
    #
    stmt = delete(PermissionDB).where(
        PermissionDB.permission_id == permission_id
        and PermissionDB.dean_status == DeanStatus.PENDING
    )
    db.execute(stmt)
    db.commit()
    return True
