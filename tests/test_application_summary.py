import json

from app.models.application_summary import ApplicationSummary
from app.models.round import Round
from app.default.account_routes import build_application_data_for_display

file = open("tests/api_data/endpoint_data.json")
data = json.loads(file.read())
TEST_APPLICATION_STORE_DATA = data[
    "http://application_store/applications?account_id=test-user"
]
TEST_SUBMITTED_APPLICATION_STORE_DATA = data[
    "http://application_store/applications?account_id=test-user-2"
]
TEST_ROUND_STORE_DATA = data["http://fund_store/funds/funding-serivce-design/rounds/summer"]

TEST_FUNDS_DATA = data["fund_store/funds?language=en"]
TEST_ROUNDS_DATA = data["fund_store/funds/funding-service-design/rounds?language=en"]


def test_serialise_application_summary():
    application_list = TEST_APPLICATION_STORE_DATA

    applications = [
        ApplicationSummary.from_dict(application)
        for application in application_list
    ]
    assert len(applications) == 2
    assert applications[0].started_at.__class__.__name__ == "datetime"
    assert str(applications[0].started_at.tzinfo) == "Europe/London"
    assert applications[1].last_edited is None


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
        "app.default.account_routes.get_round_data_fail_gracefully",
        return_value=Round.from_dict(TEST_ROUND_STORE_DATA),
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert b"In Progress" in response.data
    assert b"Continue application" in response.data


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
        "app.default.account_routes.get_round_data_fail_gracefully",
        return_value=Round.from_dict(TEST_ROUND_STORE_DATA),
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
        "app.default.account_routes.get_applications_for_account",
        return_value=TEST_SUBMITTED_APPLICATION_STORE_DATA,
    )
    mocker.patch(
        "app.default.account_routes.get_round_data_fail_gracefully",
        return_value=Round.from_dict(TEST_ROUND_STORE_DATA),
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert b"Start new application" in response.data


def test_build_application_data_for_display(mocker, monkeypatch):
    # mocker.patch("app.default.data.get_lang",
    # return_value = "en")

    # mocker.patch("app.default.data.current_app")

    mocker.patch("app.default.account_routes.get_all_funds", return_value=TEST_FUNDS_DATA)
    mocker.patch("app.default.account_routes.get_all_rounds_for_fund", return_value=TEST_ROUNDS_DATA)

    result = build_application_data_for_display([ApplicationSummary.from_dict(app) for app in TEST_APPLICATION_STORE_DATA])
    fsd_fund = result["funding-service-design"]
    assert fsd_fund, "Fund not returned"
    assert "Test Fund" == fsd_fund["fund_data"]["name"]

    assert 2 == len(fsd_fund["rounds"]), "wrong number of rounds returned"
    assert "cof-r2w2" == fsd_fund["rounds"][0]["round_details"]["id"], "cof_r2w2 not present in rounds"
    assert 0 == len(fsd_fund["rounds"][0]["applications"])
    assert "summer" == fsd_fund["rounds"][1]["round_details"]["id"], "summer not present in rounds"
    assert 2 == len(fsd_fund["rounds"][1]["applications"])
