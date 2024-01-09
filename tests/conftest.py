import json
import multiprocessing
import platform

import pytest
from app.create_app import create_app
from app.models.fund import Fund
from flask import template_rendered
from tests.test_data import TEST_FUNDS_DATA
from tests.test_data import TEST_ROUNDS_DATA

if platform.system() == "Darwin":
    multiprocessing.set_start_method("fork")  # Required on macOSX


@pytest.fixture
def mock_login(monkeypatch):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda return_app: {
            "accountId": "test-user",
            "fullName": "Test User",
            "email": "test-user@test.com",
            "roles": [],
        },
    )


def post_driver(driver, path, params):
    driver.execute_script(
        """
    function post(path, params, method='post') {
        const form = document.createElement('form');
        form.method = method;
        form.action = path;

        for (const key in params) {
            if (params.hasOwnProperty(key)) {
            const hiddenField = document.createElement('input');
            hiddenField.type = 'hidden';
            hiddenField.name = key;
            hiddenField.value = params[key];

            form.appendChild(hiddenField);
        }
      }

      document.body.appendChild(form);
      form.submit();
    }

    post(arguments[0], arguments[1]);
    """,
        path,
        params,
    )


@pytest.fixture(scope="session")
def app():
    """
    Returns an instance of the Flask app as a fixture for testing,
    which is available for the testing session and accessed with the
    @pytest.mark.uses_fixture('live_server')
    :return: An instance of the Flask app.
    """
    yield create_app()


@pytest.fixture()
def flask_test_client():
    """
    Creates the test client we will be using to test the responses
    from our app, this is a test fixture.
    :return: A flask test client.
    """
    with create_app().test_client() as test_client:
        yield test_client


def mock_get_data(endpoint):
    file = open("tests/api_data/endpoint_data.json")
    data = json.loads(file.read())
    return data[endpoint]


@pytest.fixture()
def mock_get_application(mocker):
    file = open("tests/api_data/endpoint_data.json")
    data = json.loads(file.read())  # noqa
    # mock the function in the file it is invoked (not where it is declared)
    mocker.patch(
        "app.default.routes.get_data",
        new=mock_get_data,
    )


@pytest.fixture(scope="function")
def templates_rendered(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture(autouse=True)
def mock_get_fund_round(mocker):
    mocker.patch(
        "app.default.account_routes.get_all_funds",
        return_value=TEST_FUNDS_DATA,
    )
    mocker.patch(
        "app.default.account_routes.get_all_rounds_for_fund",
        return_value=TEST_ROUNDS_DATA,
    )
    mocker.patch(
        "app.helpers.get_round_data_by_short_names",
        return_value=TEST_ROUNDS_DATA[0],
    )
    mocker.patch(
        "app.helpers.get_fund_data_by_short_name",
        return_value=Fund.from_dict(TEST_FUNDS_DATA[0]),
    )
    mocker.patch(
        "app.default.routes.get_all_fund_short_names",
        return_value=["COF", "NSTF"],
    )
    mocker.patch(
        "app.helpers.get_all_fund_short_names",
        return_value=["COF", "NSTF"],
    )
    mocker.patch(
        "app.helpers.get_default_round_for_fund",
        return_value=TEST_ROUNDS_DATA[0],
    )
    mocker.patch(
        "app.default.application_routes.get_round_data",
        return_value=TEST_ROUNDS_DATA[0],
    )
    mocker.patch(
        "app.default.application_routes.get_round",
        return_value=TEST_ROUNDS_DATA[0],
    )
    mocker.patch(
        "app.default.application_routes.get_fund_data",
        return_value=Fund.from_dict(TEST_FUNDS_DATA[0]),
    )
    mocker.patch(
        "app.default.data.get_round_data_fail_gracefully",
        return_value=TEST_ROUNDS_DATA[0],
    )
    mocker.patch("app.default.account_routes.get_lang", return_value="en")
