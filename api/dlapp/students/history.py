from fastapi import HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy import and_

from ...schemas import Role

from .models import Permission as PermissionDB


def get_history(user, db):
    if Role.STUDENT not in user.roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    # groups=["/Hostel/Boys","/Students/CSE/B.E/First Year"]
    for grp in user.groups:
        if (grp.split("/")[1] == "Hostel"):
            break
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    stmt = select(PermissionDB).where(PermissionDB.user_id == user.user_id)
    user_history = db.scalars(stmt).all()
    return user_history


def delete_permission(permission_id, user, db):
    if Role.STUDENT not in user.roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    stmt = delete(PermissionDB).where(PermissionDB)
