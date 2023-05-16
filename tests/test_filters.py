import datetime

import app.filters as filters
import pytest
from app import app


def test_date_format_short_month():
    a_datetime = datetime.datetime(2020, 1, 1, 12, 0, 0)
    with app.test_request_context():
        assert filters.date_format_short_month(a_datetime) == "01 Jan 2020"


def test_datetime_format_short_month():
    a_datetime = datetime.datetime(2020, 1, 1, 12, 0, 0)
    with app.test_request_context():
        assert (
            filters.datetime_format_short_month(a_datetime)
            == "01 Jan 2020 at 12:00pm"
        )


@pytest.mark.parametrize(
    "input_date, expected",
    [
        ("2020-01-01T00:00:00", "01 January 2020 at 00:00am"),
        ("2020-01-01T12:00:00", "01 January 2020 at 12:00pm"),
        ("2020-12-01T23:59:59", "01 December 2020 at 23:59pm"),
    ],
)
def test_datetime_format(input_date, expected):
    with app.test_request_context():
        assert filters.datetime_format(input_date) == expected


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("Testing_snake_case", "Testing Snake Case"),
        ("_Testing_snake_case", "Testing Snake Case"),
    ],
)
def test_snake_case_to_human(input_string, expected):
    assert filters.snake_case_to_human(input_string) == expected


@pytest.mark.parametrize(
    "input_string, expected",
    [
        ("testing-kebab-case", "Testing kebab case"),
        ("-testing-kebab-case", "Testing kebab case"),
    ],
)
def test_kebab_case_to_human(input_string, expected):
    assert filters.kebab_case_to_human(input_string) == expected


def test_status_translation():
    assert filters.status_translation("NOT_STARTED") == "Not Started"
