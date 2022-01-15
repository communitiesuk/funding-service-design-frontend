import pytest
from app.create_app import create_app
from chromedriver_py import binary_path  # this will get you the path variable
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


@pytest.fixture(scope="session")
def app():
    app = create_app()
    return app


# Fixture for Chrome
@pytest.fixture(scope="class")
def selenium_chrome_driver(request):
    # print(binary_path)
    # TODO: Consider using hitchchrome 85.0 to install compatible versions of
    #  chromedriver, chrome and selenium simultaneously
    service_object = Service(binary_path)
    chrome_options = Options()
    chrome_options.add_argument(
        "--headless"
    )  # chrome_options.headless = True # also works
    # TODO: set chrome_options.binary_location = ...
    #  (if setting to run in container or on GitHub)
    chrome_driver = webdriver.Chrome(
        service=service_object, options=chrome_options
    )  # noqa
    request.cls.driver = chrome_driver
    yield
    chrome_driver.close()
