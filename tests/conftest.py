import pytest
from app.create_app import create_app
from chromedriver_py import binary_path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# Fixture of app instance
@pytest.fixture(scope="session")
def app():
    """Returns an instance of the Flask app as a fixture for testing
    which is available for the testing session and accessed with the
    @pytest.mark.uses_fixture('live_server')"""

    app = create_app()
    return app


# Fixture for Chrome
@pytest.fixture(scope="class")
def selenium_chrome_driver(request):
    """Returns a Selenium Chrome driver as a fixture for testing,
    using an installed Chromedriver from the .venv chromedriver_py package
    install location. Accessible with the
    @pytest.mark.uses_fixture('selenium_chrome_driver')"""

    # TODO: Consider using hitchchrome 85.0 to install compatible versions of
    #  chromedriver, chrome and selenium simultaneously
    service_object = Service(binary_path)
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # TODO: set chrome_options.binary_location = ...
    #  (if setting to run in container or on GitHub)
    chrome_driver = webdriver.Chrome(
        service=service_object, options=chrome_options
    )  # noqa
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()
