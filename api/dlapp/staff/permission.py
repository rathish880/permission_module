from fastapi import HTTPException, status

from ...schemas import Role

from .schemas import Permission, Designation, HodStatus, DeanStatus
from .models import Permission as PermissionDB
from .tasks import send_notification

from datetime import datetime

departments = ["CSE", "EEE", "ECE", "MECH", "S&H", "MBA"]


def request_permission(permission_details, user, db, tasks):
    if Role.STAFF not in user.roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if len(user.groups) > 1:
        for grp in user.groups:
            department = grp.split("/")[2]
            if department in departments:
                group = grp
                break
    else:
        group = user.groups[0]

    designation = group.split("/")[3]

    permission = PermissionDB(
        user_id=user.user_id,
        user_group=group,
        permission_date=datetime.date(permission_details.permission_date),
        permission_time=permission_details.permission_time,
        hod_status=HodStatus.DIRECT
        if designation == Designation.HEADS
        else HodStatus.PENDING,
        dean_status=DeanStatus.PENDING,
        reason=permission_details.reason,
    )

    db.add(permission)
    db.commit()

    permission = Permission(
        permission_id=permission.permission_id,
        user_name=user.name,
        user_group=permission.user_group,
        permission_date=permission.permission_date,
        permission_time=permission.permission_time,
        requested_on=permission.requested_on,
        hod_status=permission.hod_status,
        dean_status=permission.hod_status,
        acted_on=permission.acted_on,
        reason=permission.reason,
    )

    tasks.add_task(send_notification, permission)

    return True
