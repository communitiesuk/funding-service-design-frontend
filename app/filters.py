from datetime import datetime


def date_format_short_month(value, format="%d %b %Y"):
    return value.strftime(format)


def datetime_format_short_month(value):
    date_format = "%d %b %Y at %H:%M"
    am_pm_format = "%p"
    formatted_time = value.strftime(date_format)
    formatted_time = formatted_time + value.strftime(am_pm_format).lower()
    return formatted_time


def datetime_format(value):
    date_format = "%d %B %Y at %H:%M"
    am_pm_format = "%p"
    formatted_time = datetime.strptime(value, "%Y-%m-%d %X").strftime(
        date_format
    )
    formatted_time = (
        formatted_time
        + datetime.strptime(value, "%Y-%m-%d %X")
        .strftime(am_pm_format)
        .lower()
    )
    return formatted_time


def snake_case_to_human(word):
    if word:
        return word.replace("_", " ").title()


def kebab_case_to_human(word):
    """Should NOT be used to unslugify as '-' are
    also used to replace other special characters"""
    if word:
        return word.replace("-", " ").title()
