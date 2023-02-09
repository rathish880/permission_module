"""Contains routes for Reporter."""
from datetime import date, datetime, timedelta, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy import select

from ..database import SessionLocal
from ..dependencies import get_db, get_user
from ..schemas import Role, User
from .models import Report as ReportDB
from .schemas import Report, ReportDetails
from .tasks import send_telegram_message

router = APIRouter(prefix="/reporter", tags=["reporter"])


@router.get(
    "/reports",
    responses={
        status.HTTP_200_OK: {"description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is unauthorized"},
        status.HTTP_403_FORBIDDEN: {
            "description": "User is not allowed to access reports"
        },
    },
    #    response_model=Report,
)
async def get_reports(
    from_date: date | None = None,
    to_date: date | None = None,
    user: User = Depends(get_user),
    db: SessionLocal = Depends(get_db),
) -> list[Report]:
    """Get reports submitted between `from_date` and `to_date`.

    If `from_date` is not provided, the current day will be choosen.
    Similarly, if `to_date` is not provided, the next date of `from_date` will be used.
    """
    if Role.DEAN not in user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not from_date:
        from_date = datetime.now(timezone.utc).date()

    if not to_date:
        to_date = from_date + timedelta(days=1)

    stmt = select(ReportDB).where(ReportDB.reported_on.between(from_date, to_date))
    reports = db.scalars(stmt).all()
    return reports


@router.post(
    "/reports",
    responses={
        status.HTTP_200_OK: {"description": "Report created"},
        status.HTTP_401_UNAUTHORIZED: {"description": "User is unauthorized"},
        status.HTTP_403_FORBIDDEN: {"description": "User is not allowed to report"},
    },
    response_model=bool,
)
async def post_report(
    report_details: ReportDetails,
    user: User = Depends(get_user),
    db: SessionLocal = Depends(get_db),
    tasks: BackgroundTasks = None,
) -> bool:
    """Create a new report with the current date time and details."""
    if Role.STUDENT not in user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if report_details.period <= 0:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY, "Period should be a positive integer"
        )
    group = next(group for group in user.groups if Role.STUDENT.value in group.lower())
    report = ReportDB(
        period=report_details.period,
        details=report_details.details,
        reporter_group=group,
    )
    db.add(report)
    db.commit()
    report = Report(
        report_id=report.report_id,
        reported_on=report.reported_on,
        reporter_group=report.reporter_group,
        period=report.period,
        details=report.details,
    )
    tasks.add_task(send_telegram_message, report)
    return True
