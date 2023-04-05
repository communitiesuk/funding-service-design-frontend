import json
from datetime import datetime

import pytest
from app.default.account_routes import build_application_data_for_display
from app.default.account_routes import get_visible_funds
from app.default.account_routes import update_applications_statuses_for_display
from app.default.data import RoundStatus
from app.models.application_summary import ApplicationSummary
from app.models.round import Round
from bs4 import BeautifulSoup

file = open("tests/api_data/endpoint_data.json")
data = json.loads(file.read())
TEST_APPLICATION_STORE_JSON = data[
    "application_store/applications?account_id="
    + "test-user&order_by=last_edited&order_rev=1"
]
common_application_data = {
    "account_id": "test-user",
    "reference": "TEST-REF-B",
    "project_name": "Test project",
    "date_submitted": None,
    "started_at": "2022-05-20 14:47:12",
    "last_edited": "2022-05-24 11:03:59",
    "language": "en",
    "id": "xxxx",
    "status": "IN_PROGRESS",
    "fund_id": "xxx",
    "round_id": "xxx",
}
TEST_APP_STORE_DATA = [
    ApplicationSummary.from_dict(
        {
            **common_application_data,
            "id": "1111",
            "status": "IN_PROGRESS",
            "fund_id": "111",
            "round_id": "fsd-r2w2",
        }
    ),
    ApplicationSummary.from_dict(
        {
            **common_application_data,
            "id": "2222",
            "status": "NOT_STARTED",
            "fund_id": "111",
            "round_id": "fsd-r2w3",
        }
    ),
    ApplicationSummary.from_dict(
        {
            **common_application_data,
            "id": "3333",
            "status": "SUBMITTED",
            "fund_id": "222",
            "round_id": "abc-r1",
        }
    ),
    ApplicationSummary.from_dict(
        {
            **common_application_data,
            "id": "4444",
            "status": "READY_TO_SUBMIT",
            "fund_id": "222",
            "round_id": "abc-r1",
        }
    ),
]
TEST_SUBMITTED_APPLICATION_STORE_DATA = data[
    "http://application_store/applications?account_id=test-user-2"
]
TEST_ROUND_STORE_DATA = data[
    "fund_store/funds/funding-service-design/rounds/summer?language=en"
]

TEST_FUNDS_DATA = [
    {
        "id": "111",
        "name": "Test Fund",
        "description": "test test",
        "short_name": "FSD",
        "title": "fund for testing",
    },
    {
        "id": "222",
        "name": "Test Fund 2",
        "description": "test test 2",
        "short_name": "FSD2",
        "title": "fund for testing 2",
    },
]

common_round_data = {
    "opens": "2022-09-01 00:00:01",
    "assessment_deadline": "2030-03-20 00:00:01",
    "assessment_criteria_weighting": [],
    "contact_details": {},
    "support_availability": {},
    "prospectus": "/cof_r2w2_prospectus",
    "instructions": "Round specific instruction text",
}
TEST_ROUNDS_DATA = [
    Round.from_dict(
        {
            **common_round_data,
            "fund_id": "111",
            "id": "fsd-r2w2",
            "short_name": "r2w2",
            "title": "closed_round",
            "deadline": "2023-01-01 00:00:01",
        }
    ),
    Round.from_dict(
        {
            **common_round_data,
            "fund_id": "111",
            "id": "fsd-r2w3",
            "short_name": "r2w3",
            "title": "open_round",
            "deadline": "2050-01-01 00:00:01",
        }
    ),
    Round.from_dict(
        {
            **common_round_data,
            "fund_id": "222",
            "id": "abc-r1",
            "short_name": "r1",
            "title": "closed_round",
            "deadline": "2023-01-01 00:00:01",
        }
    ),
    Round.from_dict(
        {
            **common_round_data,
            "fund_id": "222",
            "id": "abc-r2",
            "short_name": "r2",
            "title": "open_round",
            "deadline": "2050-01-01 00:00:01",
        }
    ),
]

TEST_DISPLAY_DATA = {
    "total_applications_to_display": 4,
    "funds": [
        {
            "fund_data": {
                "id": "funding-service-design",
                "name": "Test Fund",
                "description": "test test",
                "short_name": "FSD",
            },
            "rounds": [
                {
                    "is_past_submission_deadline": True,
                    "is_not_yet_open": False,
                    "round_details": {
                        "opens": "2022-09-01 00:00:01",
                        "deadline": "2030-01-30 00:00:01",
                        "assessment_deadline": "2030-03-20 00:00:01",
                        "id": "cof-r2w2",
                        "title": "Round 2 Window 2",
                        "instructions": "r2w2 instructions",
                        "fund_id": "fund-service-design",
                        "short_name": "R2W2",
                        "assessment_criteria_weighting": [],
                        "contact_details": {},
                        "support_availability": {},
                    },
                    "applications": [
                        {
                            "id": "uuidv4",
                            "reference": "TEST-REF-B",
                            "status": "NOT_SUBMITTED",
                            "round_id": "summer",
                            "fund_id": "funding-service-design",
                            "started_at": "2020-01-01 12:03:00",
                            "project_name": None,
                            "last_edited": datetime.strptime(
                                "2020-01-01 12:03:00", "%Y-%m-%d %H:%M:%S"
                            ),
                        },
                        {
                            "id": "ed221ac8-5d4d-42dd-ab66-6cbcca8fe257",
                            "reference": "TEST-REF-C",
                            "status": "SUBMITTED",
                            "round_id": "summer",
                            "fund_id": "funding-service-design",
                            "started_at": "2023-01-01 12:01:00",
                            "project_name": "",
                            "last_edited": None,
                        },
                    ],
                },
                {
                    "is_past_submission_deadline": False,
                    "is_not_yet_open": False,
                    "round_details": {
                        "opens": "2022-09-01 00:00:01",
                        "deadline": "2030-01-30 00:00:01",
                        "assessment_deadline": "2030-03-20 00:00:01",
                        "id": "summer",
                        "title": "Summer round",
                        "fund_id": "fund-service-design",
                        "short_name": "R2W3",
                        "instructions": "r2w3 instructions",
                        "assessment_criteria_weighting": [],
                        "contact_details": {},
                        "support_availability": {},
                    },
                    "applications": [
                        {
                            "id": "uuidv4",
                            "reference": "TEST-REF-B",
                            "status": "IN_PROGRESS",
                            "round_id": "summer",
                            "fund_id": "funding-service-design",
                            "started_at": "2020-01-01 12:03:00",
                            "project_name": None,
                            "last_edited": datetime.strptime(
                                "2020-01-01 12:03:00", "%Y-%m-%d %H:%M:%S"
                            ),
                        },
                        {
                            "id": "ed221ac8-5d4d-42dd-ab66-6cbcca8fe257",
                            "reference": "TEST-REF-C",
                            "status": "READY_TO_SUBMIT",
                            "round_id": "summer",
                            "fund_id": "funding-service-design",
                            "started_at": "2023-01-01 12:01:00",
                            "project_name": "",
                            "last_edited": None,
                        },
                    ],
                },
            ],
        }
    ],
}


@pytest.fixture
def mock_login(monkeypatch):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )


def test_serialise_application_summary():
    application_list = TEST_APPLICATION_STORE_JSON

    applications = [
        ApplicationSummary.from_dict(application)
        for application in application_list
    ]
    assert len(applications) == 3
    assert isinstance(applications[0].started_at, datetime)
    assert str(applications[0].started_at.tzinfo) == "Europe/London"
    assert applications[1].last_edited is None
    assert applications[1].language == "English"
    assert applications[2].language == "Welsh"


@pytest.mark.parametrize(
    "fund_short_name,round_short_name,expected_search_params",
    [
        (None, None, {"account_id": "test-user"}),
        (
            "COF",
            "R2W2",
            {
                "account_id": "test-user",
                "round_id": "fsd-r2w2",
                "fund_id": "111",
            },
        ),
        ("COF", None, {"account_id": "test-user"}),
    ],
)
def test_dashboard_route_search_call(
    flask_test_client,
    mocker,
    app,
    mock_login,
    fund_short_name,
    round_short_name,
    expected_search_params,
):
    request_mock = mocker.patch("app.default.account_routes.request")
    request_mock.args.get = (
        lambda key: fund_short_name
        if key == "fund"
        else (round_short_name if key == "round" else None)
    )
    get_apps_mock = mocker.patch(
        "app.default.account_routes.get_round_data_by_short_names",
        return_value=TEST_ROUNDS_DATA[0],
    )
    get_apps_mock = mocker.patch(
        "app.default.account_routes.search_applications",
        return_value=TEST_APP_STORE_DATA,
    )
    mocker.patch(
        "app.default.account_routes.build_application_data_for_display",
        return_value=TEST_DISPLAY_DATA,
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200

    get_apps_mock.assert_called_once_with(
        search_params=expected_search_params, as_dict=False
    )


def test_dashboard_route(flask_test_client, mocker, mock_login):

    mocker.patch(
        "app.default.account_routes.search_applications",
        return_value=TEST_APP_STORE_DATA,
    )
    mocker.patch(
        "app.default.account_routes.build_application_data_for_display",
        return_value=TEST_DISPLAY_DATA,
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200

    soup = BeautifulSoup(response.data, "html.parser")

    assert len(soup.find_all("strong", class_="in-progress-tag-new")) == 2
    assert len(soup.find_all("strong", class_="complete-tag")) == 2
    assert len(soup.find_all("a", string="Continue application")) == 2
    assert (
        len(
            soup.find_all(
                "h2",
                string=lambda text: "Window closed - Test Fund "
                + "Round 2 Window 2"
                in text,
            )
        )
        == 1
    )
    assert (
        len(
            soup.find_all(
                "h2",
                string=lambda text: "Window closed - Community Ownership Fund "
                + "Round 2 Window 3"
                in text,
            )
        )
        == 0
    )
    assert (
        len(
            soup.find_all("span", class_="govuk-caption-m", string="Test Fund")
        )
        == 2
    )
    assert (
        len(
            soup.find_all(
                "h2", string=lambda text: "Round 2 Window 2" == str.strip(text)
            )
        )
        == 1
    )
    assert (
        len(
            soup.find_all(
                "h2", string=lambda text: "Round 2 Window 2" == str.strip(text)
            )
        )
        == 1
    )


@pytest.mark.skip(reason="Logic covered in build data for display")
def test_submitted_dashboard_route_shows_no_application_link(
    flask_test_client, mocker, mock_login, mock_get_fund_round
):
    mocker.patch(
        "app.default.account_routes.get_applications_for_account",
        return_value=TEST_SUBMITTED_APPLICATION_STORE_DATA,
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    # there should be no link to application on the page
    assert b"Continue application" not in response.data
    assert b"Submitted" in response.data


def test_dashboard_route_no_applications(
    flask_test_client, mocker, mock_login
):

    mocker.patch(
        "app.default.account_routes.search_applications",
        return_value=[],
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    assert (
        len(
            soup.find_all(
                "p",
                string=lambda text: "0 applications" in text
                if text
                else False,
            )
        )
        == 1
    )
    assert (
        len(
            soup.find_all(
                "button", string=lambda text: "Start new application" in text
            )
        )
        == 1
    )


@pytest.mark.parametrize(
    "funds,rounds,applications,expected_fund_count,expected_round_count,"
    "expected_app_count, fund_short_name",
    [
        # No filters, 2 funds with 2 rounds each
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA,
            TEST_APP_STORE_DATA,
            2,
            4,
            4,
            None,
        ),
        # No fund filter, one fund with no rounds one fund with 2 rounds
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA[0:2],
            TEST_APP_STORE_DATA,
            1,
            2,
            2,
            None,
        ),
        # Filter to fund with open rounds
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA,
            TEST_APP_STORE_DATA,
            1,
            2,
            2,
            "FSD",
        ),
        # Filter to fund with no rounds
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA[0:2],
            TEST_APP_STORE_DATA,
            0,
            0,
            0,
            "FSD2",
        ),
        # 1 app in closed round, 0 in open round
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA,
            TEST_APP_STORE_DATA[0:1],
            1,
            2,
            1,
            "FSD",
        ),
        # 1 app in open round, 0 in closed round
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA,
            TEST_APP_STORE_DATA[1:2],
            1,
            1,
            1,
            "FSD",
        ),
        # 1 fund with 2 rounds and 2 apps, 1 fund with 1 closed round and no
        # apps
        (
            TEST_FUNDS_DATA,
            TEST_ROUNDS_DATA[0:3],
            TEST_APP_STORE_DATA[0:2],
            1,
            2,
            2,
            None,
        ),
    ],
)
def test_build_application_data_for_display(
    funds,
    rounds,
    applications,
    expected_fund_count,
    expected_round_count,
    expected_app_count,
    fund_short_name,
    mocker,
):

    mocker.patch(
        "app.default.account_routes.get_all_funds",
        return_value=funds,
    )
    mocker.patch(
        "app.default.account_routes.get_all_rounds_for_fund",
        new=lambda fund_id, as_dict: [
            round for round in rounds if round.fund_id == fund_id
        ],
    )

    result = build_application_data_for_display(applications, fund_short_name)

    assert result["total_applications_to_display"] == expected_app_count
    assert len(result["funds"]) == expected_fund_count
    assert (
        sum(len(fund["rounds"]) for fund in result["funds"])
        == expected_round_count
    )


@pytest.mark.parametrize(
    "application,round_status,expected_status",
    [
        (
            ApplicationSummary.from_dict(
                {**common_application_data, "status": "IN_PROGRESS"}
            ),
            RoundStatus(False, False, True),
            "IN_PROGRESS",
        ),
        (
            ApplicationSummary.from_dict(
                {**common_application_data, "status": "COMPLETED"}
            ),
            RoundStatus(False, False, True),
            "READY_TO_SUBMIT",
        ),
        (
            ApplicationSummary.from_dict(
                {**common_application_data, "status": "COMPLETED"}
            ),
            RoundStatus(True, False, False),
            "NOT_SUBMITTED",
        ),
        (
            ApplicationSummary.from_dict(
                {**common_application_data, "status": "IN_PROGRESS"}
            ),
            RoundStatus(True, False, False),
            "NOT_SUBMITTED",
        ),
    ],
)
def test_update_application_statuses(
    application, round_status, expected_status
):
    result = update_applications_statuses_for_display(
        [application], round_status
    )
    assert result[0].status == expected_status


@pytest.mark.parametrize(
    "applications,visible",
    [
        (
            [
                ApplicationSummary.from_dict(
                    {**common_application_data, "lang": "en"}
                ),
                ApplicationSummary.from_dict(
                    {**common_application_data, "lang": "cy"}
                ),
            ],
            True,
        ),
        (
            [
                ApplicationSummary.from_dict(
                    {**common_application_data, "lang": "cy"}
                ),
                ApplicationSummary.from_dict(
                    {**common_application_data, "lang": "cy"}
                ),
            ],
            False,
        ),
        ([], False),
    ],
)
def test_determine_show_language_column(applications, visible):
    pass


@pytest.mark.parametrize(
    "funds, filter_value, expected_count",
    [
        ([{"short_name": "ABC"}], "ABC", 1),
        ([{"short_name": "ABC"}], "abc", 1),
        ([{"short_name": "ABC"}], "def", 0),
        ([], "ABC", 0),
        ([{"short_name": "ABC"}, {"short_name": "DEF"}], "abc", 1),
    ],
)
def test_filter_funds_by_short_name(
    funds, filter_value, expected_count, mocker
):
    mocker.patch(
        "app.default.account_routes.get_all_funds", return_value=funds
    )
    result = get_visible_funds(filter_value)
    assert expected_count == len(result)
