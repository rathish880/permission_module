"""Contains routes for DLAPP"""
from fastapi import APIRouter, BackgroundTasks, Depends, status

from . import history
from . import pending_request
from . import permission
from ..database import SessionLocal
from ..dependencies import get_db, get_user
from ..schemas import User
from .schemas import PermissionDetails

# from .tasks import send_notification

router = APIRouter(prefix="/dlapp", tags=["dlapp"])


# request permission
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

    result = permission.request_permission(permission_details, user, db, tasks)
    return result


# get pending request
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
    result = pending_request.pending_requests(user, db)
    return result


# update status by heads
@router.put(
    "/status",
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is unauthorized"},
    },
    response_model=bool,
)
async def update_status(
    permission_id: int,
    permission_status: str,
    user: User = Depends(get_user),
    db: SessionLocal = Depends(get_db),
):
    result = pending_request.update_status(permission_id, permission_status, user, db)
    return result


# get history
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
    result = history.get_history(head, user, db)
    return result


# delete permission by user before seen by Dean
@router.delete(
    "/user-permission",
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is unauthorized"},
    },
)
async def delete_user_permission(
    permission_id: int,
    user: User = Depends(get_user),
    db: SessionLocal = Depends(get_db),
):
    result = history.delete_user_permission(permission_id, user, db)
    return result


# delete permission by HR
@router.delete(
    "/delete-permission",
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is unauthorized"},
    },
)
async def delete_permission(
    permission_id: str,
    user: User = Depends(get_user),
    db: SessionLocal = Depends(get_db),
):
    result = history.delete_permission(permission_id, user, db)
    return result
