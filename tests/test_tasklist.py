import json

from app.default.data import RoundStatus
from app.models.application import Application
from app.models.application_display_mapping import ApplicationMapping
from tests.test_data import TEST_APP_STORE_DATA
from tests.test_data import TEST_DISPLAY_DATA

file = open("tests/api_data/endpoint_data.json")
data = json.loads(file.read())
TEST_APPLICATION_STORE_DATA = data[
    "http://application_store/test-application-id"
]

TEST_SUBMITTED_APPLICATION_STORE_DATA = data[
    "http://application_store/test-application-submit"
]

TEST_APPLICATION_DISPLAY_RESPONSE = data[
    "fund_store/funds/funding-service-design/"
    "rounds/summer/sections/application"
]


def test_tasklist_route(flask_test_client, mocker, mock_login):
    mocker.patch(
        "app.default.application_routes.get_application_data",
        return_value=Application.from_dict(TEST_APPLICATION_STORE_DATA),
    )
    mocker.patch(
        "app.default.application_routes.determine_round_status",
        return_value=RoundStatus(False, False, True),
    )
    mocker.patch(
        "app.default.application_routes.get_application_display_config",
        return_value=[
            ApplicationMapping.from_dict(section)
            for section in TEST_APPLICATION_DISPLAY_RESPONSE
        ],
    )
    response = flask_test_client.get(
        "tasklist/test-application-id", follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Help with filling out your application" in response.data
    assert b"Test Section 1" in response.data
    assert b"Risk" in response.data


def test_tasklist_route_after_deadline(flask_test_client, mocker, mock_login):
    mocker.patch(
        "app.default.application_routes.get_application_data",
        return_value=Application.from_dict(TEST_APPLICATION_STORE_DATA),
    )
    mocker.patch(
        "app.default.application_routes.determine_round_status",
        return_value=RoundStatus(True, False, False),
    )
    response = flask_test_client.get(
        "tasklist/test-application-id", follow_redirects=False
    )
    assert response.status_code == 302
    assert "/account" == response.location


def test_tasklist_for_submit_application_route(
    flask_test_client, mocker, mock_login
):
    mocker.patch(
        "app.default.application_routes.get_application_data",
        return_value=Application.from_dict(
            TEST_SUBMITTED_APPLICATION_STORE_DATA
        ),
    )
    mocker.patch(
        "app.default.application_routes.determine_round_status",
        return_value=RoundStatus(False, False, True),
    )

    get_apps_mock = mocker.patch(
        "app.default.account_routes.search_applications",
        return_value=TEST_APP_STORE_DATA,
    )
    mocker.patch(
        "app.default.account_routes.build_application_data_for_display",
        return_value=TEST_DISPLAY_DATA,
    )
    response = flask_test_client.get(
        "tasklist/test-application-submit", follow_redirects=True
    )
    assert response.status_code == 200
    get_apps_mock.assert_called_once_with(
        search_params={
            "account_id": "test-user",
            "fund_id": "111",
            "round_id": "fsd-r2w2",
        },
        as_dict=False,
    )
