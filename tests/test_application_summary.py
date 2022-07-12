import json

from app.models.application_summary import ApplicationSummary


TEST_APPLICATION_STORE_DATA = """[
    {
        "id": "uuidv4",
        "status": "IN_PROGRESS",
        "account_id": "test-user",
        "fund_id": "funding-service-design",
        "round_id": "summer",
        "project_name": null,
        "date_submitted": null,
        "started_at": "2022-05-20 14:47:12",
        "last_edited": "2022-05-24 11:03:59"
    },
    {
        "id": "ed221ac8-5d4d-42dd-ab66-6cbcca8fe257",
        "status": "NOT_STARTED",
        "account_id": "test-user",
        "fund_id": "funding-service-design",
        "round_id": "summer",
        "project_name": "",
        "date_submitted": null,
        "started_at": "2022-05-24 10:42:41",
        "last_edited": null,
        "Unknown": "DOES NOT MAKE ME FAIL"
    }
]"""


def test_serialise_application_summary():
    application_list = json.loads(TEST_APPLICATION_STORE_DATA)

    applications = [
        ApplicationSummary.from_dict(application)
        for application in application_list
    ]
    assert len(applications) == 2
    assert applications[0].started_at.__class__.__name__ == "datetime"
    assert applications[1].last_edited is None


def test_dashboard_route(flask_test_client, requests_mock, monkeypatch):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )
    requests_mock.get(
        "http://application_store/applications?account_id=test-user",
        text=TEST_APPLICATION_STORE_DATA,
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert b"IN PROGRESS" in response.data
    assert b"20/05/22" in response.data


def test_dashboard_route_no_applications(
    flask_test_client, requests_mock, monkeypatch
):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )

    requests_mock.get(
        "http://application_store/applications?account_id=test-user",
        text="[]",
    )
    response = flask_test_client.get("/account", follow_redirects=True)
    assert response.status_code == 200
    assert b"Start new application" in response.data
