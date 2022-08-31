import json

from app.models.application_summary import ApplicationSummary

file = open("tests/api_data/endpoint_data.json")
data = json.loads(file.read())
TEST_APPLICATION_STORE_DATA = data[
    "http://application_store/applications?account_id=test-user"
]
TEST_SUBMITTED_APPLICATION_STORE_DATA = data[
    "http://application_store/applications?account_id=test-user-2"
]


def test_serialise_application_summary():
    application_list = TEST_APPLICATION_STORE_DATA

    applications = [
        ApplicationSummary.from_dict(application)
        for application in application_list
    ]
    assert len(applications) == 2
    assert applications[0].started_at.__class__.__name__ == "datetime"
    assert applications[1].last_edited is None


def test_dashboard_route(flask_test_client, mocker, monkeypatch):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )
    mocker.patch(
        "app.default.routes.get_applications_for_account",
        return_value=TEST_APPLICATION_STORE_DATA,
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert b"In Progress" in response.data
    assert b"Continue application" in response.data
    assert b"20/05/22" in response.data


def test_submitted_dashboard_route_shows_no_application_link(
    flask_test_client, mocker, monkeypatch
):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )
    mocker.patch(
        "app.default.routes.get_applications_for_account",
        return_value=TEST_SUBMITTED_APPLICATION_STORE_DATA,
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
        "app.default.routes.get_applications_for_account",
        return_value=TEST_SUBMITTED_APPLICATION_STORE_DATA,
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert b"Start new application" in response.data
