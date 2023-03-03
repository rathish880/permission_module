from fastapi import Depends, status
from sqlalchemy import select

from ..main import get_user
from ..database import SessionLocal
from ..dependencies import get_db
from ..schemas import User, Role

from .main import router
from .models import Permission as PermissionDB
from .schemas import Designation


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
        stmt = select(PermissionDB).where(PermissionDB.head_approved)
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
        stmt = select(PermissionDB).where(PermissionDB.user_name == user.name)
        user_history = db.scalars(stmt).all()
        return user_history
