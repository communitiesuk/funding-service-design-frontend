import json
import multiprocessing
import platform

import pytest
from app.create_app import create_app
from app.models.fund import Fund
from flask import template_rendered
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from tests.test_data import TEST_FUNDS_DATA
from tests.test_data import TEST_ROUNDS_DATA
from webdriver_manager.chrome import ChromeDriverManager

if platform.system() == "Darwin":
    multiprocessing.set_start_method("fork")  # Required on macOSX


@pytest.fixture
def mock_login(monkeypatch):
    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda return_app: {"accountId": "test-user"},
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


@pytest.fixture(scope="class")
def selenium_chrome_driver(request):
    """
    Returns a Selenium Chrome driver as a fixture for testing.
    using an installed Chromedriver from the .venv chromedriver_py package
    install location. Accessible with the
    @pytest.mark.uses_fixture('selenium_chrome_driver')
    :return: A selenium chrome driver.
    """
    service_object = Service(ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # TODO: set chrome_options.binary_location = ...
    #  (if setting to run in container or on GitHub)
    chrome_driver = webdriver.Chrome(
        service=service_object, options=chrome_options
    )
    request.cls.driver = chrome_driver
    yield
    request.cls.driver.close()


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
        "app.default.account_routes.get_fund_data_by_short_name",
        return_value=Fund.from_dict(TEST_FUNDS_DATA[0]),
    )
    mocker.patch(
        "app.default.account_routes.get_round_data_by_short_names",
        return_value=TEST_ROUNDS_DATA[0],
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
        "app.helpers.get_default_round_for_fund",
        return_value=TEST_ROUNDS_DATA[0],
    )
    mocker.patch(
        "app.default.application_routes.get_round_data",
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
    mocker.patch(
        "app.default.content_routes.get_round_data_by_short_names",
        return_value=TEST_ROUNDS_DATA[0],
    )
    mocker.patch(
        "app.default.routes.get_fund_data_by_short_name",
        return_value=Fund.from_dict(TEST_FUNDS_DATA[0]),
    )
    mocker.patch(
        "app.default.routes.get_round_data_by_short_names",
        return_value=TEST_ROUNDS_DATA[0],
    )
