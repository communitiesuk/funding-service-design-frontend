import json

from app.models.account import Account
from app.models.application import Application
from app.models.fund import Fund
from app.models.round import Round

file = open("tests/api_data/endpoint_data.json")
data = json.loads(file.read())
TEST_APPLICATION_STORE_DATA = data[
    "http://application_store/test-application-id"
]
TEST_FUND_STORE = data["fund_store/funds/funding-service-design"]
TEST_ROUND_STORE = data["fund_store/funds/47aef2f5-3fcb-4d45-acb5-f0152b5f03c4/rounds/c603d114-5364-4474-a0c4-c41cbf4d3bbd"]
   

TEST_SUBMITTED_APPLICATION_STORE_DATA = data[
    "http://application_store/test-application-submit"
]

TEST_ACCOUNT_STORE_DATA = data[
    "account_store/accounts?account_id=test-user"
]


def test_tasklist_route(flask_test_client, mocker, monkeypatch):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )
    mocker.patch(
        "app.default.routes.get_application_data",
        return_value=Application.from_dict(TEST_APPLICATION_STORE_DATA),
    )
    mocker.patch(
        "app.default.routes.get_fund_data",
        return_value=Fund.from_dict(TEST_FUND_STORE),
    )
    mocker.patch(
        "app.default.routes.get_round_data",
        return_value=Round.from_dict(TEST_ROUND_STORE),
    )
    mocker.patch(
        "app.default.routes.get_account",
        return_value=Account.from_json(TEST_ACCOUNT_STORE_DATA),
    )
    response = flask_test_client.get(
        "tasklist/test-application-id", follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Help with filling out your application" in response.data
    assert b"About your organisation" in response.data


def test_tasklist_for_submit_application_route(
    flask_test_client, mocker, monkeypatch
):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )
    mocker.patch(
        "app.default.routes.get_application_data",
        return_value=Application.from_dict(
            TEST_SUBMITTED_APPLICATION_STORE_DATA
        ),
    )
    mocker.patch(
        "app.default.routes.get_account",
        return_value=Account.from_json(TEST_ACCOUNT_STORE_DATA),
    )
    response = flask_test_client.get(
        "tasklist/test-application-submit", follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Application complete" in response.data
    assert b"Return to your applications page" in response.data
    assert b"test@example.com" in response.data
