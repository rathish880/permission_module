from fastapi import HTTPException, status

from ...schemas import Role

from .schemas import Permission, HodStatus, WardenStatus
from .models import Permission as PermissionDB
from .tasks import send_notification

from datetime import datetime

departments = ["CSE", "EEE", "ECE", "MECH", "S&H", "MBA"]


def request_permission(permission_details, user, db, tasks):
    if Role.STUDENT not in user.roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    declared_holiday = False

    for grp in user.groups:
        department = grp.split("/")[2]
        if department in departments:
            group = grp
            break

    permission = PermissionDB(
        user_id=user.user_id,
        user_group=group,
        from_date=datetime.date(permission_details.from_date),
        to_date=datetime.date(permission_details.to_date),
        hod_status=HodStatus.DIRECT if declared_holiday else HodStatus.PENDING,
        warden_status=WardenStatus.PENDING,
        reason="Declared Holiday" if declared_holiday else permission_details.reason,
    )

    db.add(permission)
    db.commit()

    permission = Permission(
        permission_id=permission.permission_id,
        user_name=user.name,
        user_group=permission.user_group,
        from_date=permission.from_date,
        to_date=permission.to_date,
        reason=permission.reason,
    )

    tasks.add_task(send_notification, permission)

    return True
