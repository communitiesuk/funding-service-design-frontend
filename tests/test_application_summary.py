import json

from app.default.account_routes import build_application_data_for_display
from app.models.application_summary import ApplicationSummary
from app import app

file = open("tests/api_data/endpoint_data.json")
data = json.loads(file.read())
TEST_APPLICATION_STORE_DATA = data[
    "application_store/applications?account_id="
    + "test-user&order_by=last_edited&order_rev=1"
]
TEST_SUBMITTED_APPLICATION_STORE_DATA = data[
    "http://application_store/applications?account_id=test-user-2"
]
TEST_ROUND_STORE_DATA = data[
    "fund_store/funds/funding-service-design/rounds/summer?language=en"
]

TEST_FUNDS_DATA = data["fund_store/funds?language=en"]
TEST_ROUNDS_DATA = data[
    "fund_store/funds/funding-service-design/rounds?language=en"
]

TEST_DISPLAY_DATA = {
    "funding-service-design": {
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
                        "last_edited": "2020-01-01 12:03:00",
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
                        "last_edited": "2020-01-01 12:03:00",
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
}


def test_serialise_application_summary():
    with app.test_request_context():
        application_list = TEST_APPLICATION_STORE_DATA

        applications = [
            ApplicationSummary.from_dict(application)
            for application in application_list
        ]
        assert len(applications) == 3
        assert applications[0].started_at.__class__.__name__ == "datetime"
        assert str(applications[0].started_at.tzinfo) == "Europe/London"
        assert applications[1].last_edited is None
        assert applications[1].language == "English"
        assert applications[2].language == "Welsh"


def test_dashboard_route(flask_test_client, mocker, monkeypatch):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )
    mocker.patch(
        "app.default.account_routes.get_applications_for_account",
        return_value=TEST_APPLICATION_STORE_DATA,
    )
    mocker.patch(
        "app.default.account_routes.get_all_funds",
        return_value=TEST_FUNDS_DATA,
    )
    mocker.patch(
        "app.default.account_routes.get_all_rounds_for_fund",
        return_value=TEST_ROUNDS_DATA,
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert b"In Progress" in response.data
    assert b"Continue application" in response.data
    assert b"Window closed - Test Fund Round 2 Window 2" in response.data
    assert (
        b"Window closed - Community Ownership Fund Round 2 Window 3"
        not in response.data
    )
    assert b"Test Fund" in response.data
    assert b"Round 2 Window 2" in response.data


def test_submitted_dashboard_route_shows_no_application_link(
    flask_test_client, mocker, monkeypatch
):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )
    mocker.patch(
        "app.default.account_routes.get_applications_for_account",
        return_value=TEST_SUBMITTED_APPLICATION_STORE_DATA,
    )
    mocker.patch(
        "app.default.account_routes.get_all_funds",
        return_value=TEST_FUNDS_DATA,
    )
    mocker.patch(
        "app.default.account_routes.get_all_rounds_for_fund",
        return_value=TEST_ROUNDS_DATA,
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    # there should be no link to application on the page
    assert b"Continue application" not in response.data
    assert b"Submitted" in response.data


def test_dashboard_route_no_applications(
    flask_test_client, mocker, monkeypatch
):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )
    mocker.patch(
        "app.default.account_routes.get_all_funds",
        return_value=TEST_FUNDS_DATA,
    )
    mocker.patch(
        "app.default.account_routes.get_all_rounds_for_fund",
        return_value=TEST_ROUNDS_DATA,
    )

    mocker.patch(
        "app.default.account_routes.get_applications_for_account",
        return_value=[],
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert b"Start new application" in response.data


def test_build_application_data_for_display(mocker):
    mocker.patch(
        "app.default.account_routes.get_all_funds",
        return_value=TEST_FUNDS_DATA,
    )
    mocker.patch(
        "app.default.account_routes.get_all_rounds_for_fund",
        return_value=TEST_ROUNDS_DATA,
    )

    result = build_application_data_for_display(
        [
            ApplicationSummary.from_dict(app)
            for app in TEST_APPLICATION_STORE_DATA
        ]
    )
    assert 3 == result["total_applications_to_display"]
    assert 1 == len(result["funds"])
    fsd_fund = result["funds"][0]
    assert fsd_fund, "Fund not returned"
    assert "Test Fund" == fsd_fund["fund_data"]["name"]

    assert 2 == len(fsd_fund["rounds"]), "wrong number of rounds returned"
    assert (
        "cof-r2w2" == fsd_fund["rounds"][0]["round_details"]["id"]
    ), "cof_r2w2 not present in rounds"
    assert fsd_fund["rounds"][0]["is_past_submission_deadline"] is True
    assert 1 == len(fsd_fund["rounds"][0]["applications"])
    assert "NOT_SUBMITTED" == fsd_fund["rounds"][0]["applications"][0].status

    assert (
        "summer" == fsd_fund["rounds"][1]["round_details"]["id"]
    ), "summer not present in rounds"
    assert fsd_fund["rounds"][1]["is_past_submission_deadline"] is False
    assert 2 == len(fsd_fund["rounds"][1]["applications"])
    assert "IN_PROGRESS" == fsd_fund["rounds"][1]["applications"][0].status
    assert "READY_TO_SUBMIT" == fsd_fund["rounds"][1]["applications"][1].status


def test_build_application_data_for_display_exclude_round_with_no_apps(
    mocker
):
    mocker.patch(
        "app.default.account_routes.get_all_funds",
        return_value=TEST_FUNDS_DATA,
    )
    mocker.patch(
        "app.default.account_routes.get_all_rounds_for_fund",
        return_value=TEST_ROUNDS_DATA,
    )

    result = build_application_data_for_display(
        [
            ApplicationSummary.from_dict(app)
            for app in TEST_APPLICATION_STORE_DATA
            if app["round_id"] == "summer"
        ]
    )
    assert 2 == result["total_applications_to_display"]
    assert 1 == len(result["funds"])
    fsd_fund = result["funds"][0]
    assert fsd_fund, "Fund not returned"
    assert "Test Fund" == fsd_fund["fund_data"]["name"]

    assert 1 == len(fsd_fund["rounds"]), "wrong number of rounds returned"

    assert (
        "summer" == fsd_fund["rounds"][0]["round_details"]["id"]
    ), "summer not present in rounds"
    assert fsd_fund["rounds"][0]["is_past_submission_deadline"] is False
    assert 2 == len(fsd_fund["rounds"][0]["applications"])
    assert "IN_PROGRESS" == fsd_fund["rounds"][0]["applications"][0].status
    assert "READY_TO_SUBMIT" == fsd_fund["rounds"][0]["applications"][1].status
