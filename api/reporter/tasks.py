"""Contains tasks to be executed for methods."""

import httpx

from ..settings import Settings
from .schemas import Report


async def send_telegram_message(report: Report):
    """Send the report as a Telegram message."""
    group = report.reporter_group.replace("/", " ")[9:]
    text = (
        f"<b>{group}</b>\n{report.details}\n\n"
        "Check reporter.aurcc.in for more information."
    )
    response = httpx.post(
        f"https://api.telegram.org/bot{Settings.BOT_TOKEN}/sendMessage",
        data={"chat_id": Settings.REPORTER_CHAT_ID, "text": text, "parse_mode": "html"},
    )

    if response.is_error:
        raise Exception(f"Unable to report message on Telegram {response.content}")
