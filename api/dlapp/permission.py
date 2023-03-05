from fastapi import HTTPException, status

from ..schemas import Role

from .schemas import Permission, Status
from .models import Permission as PermissionDB
from .tasks import send_notification

departments = ["CSE", "EEE", "ECE", "MECH", "S&H", "MBA"]


def request_permission(permission_details, user, db, tasks):
    if Role.STAFF not in user.roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if len(user.groups > 1):
        for grp in user.groups:
            department = grp.split("/")[2]
            if department in departments:
                group = grp
    else:
        group = user.groups[0]

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

    tasks.add_task(send_notification, permission)

    return True
