from datetime import datetime

from app.models.statuses import get_formatted
from flask_babel import format_datetime
from flask_babel import gettext


def date_format_short_month(value: datetime, format="dd MMM yyyy"):
    return format_datetime(value, format)


def datetime_format_short_month(value: datetime) -> str:
    if value:
        formatted_date = format_datetime(value, format="dd MMM yyyy ")
        formatted_date += gettext("at")
        formatted_date += format_datetime(value, format=" HH:mm", rebase=False)
        formatted_date += format_datetime(value, "a").lower()
        return formatted_date
    else:
        return ""


def datetime_format(value: str) -> str:
    parsed = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
    formatted_date = format_datetime(parsed, format="dd MMMM yyyy ")
    formatted_date += gettext("at")
    formatted_date += format_datetime(parsed, format=" HH:mm")
    formatted_date += format_datetime(parsed, "a").lower()
    return formatted_date


def snake_case_to_human(word: str) -> str | None:
    if word:
        return word.replace("_", " ").strip().title()


def kebab_case_to_human(word: str) -> str | None:
    """Should NOT be used to unslugify as '-' are
    also used to replace other special characters"""
    if word:
        return word.replace("-", " ").strip().capitalize()


def status_translation(value: str):
    if value:
        return get_formatted(value)
