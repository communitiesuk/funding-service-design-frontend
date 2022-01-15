"""
Tests if selected pages of the website are accessible when rendered,
according to WCAG standards
"""
import multiprocessing
from urllib.request import urlopen

import pytest
from axe_selenium_python import Axe
from flask import url_for

multiprocessing.set_start_method("fork")  # Required on macOSX


@pytest.mark.app(debug=False)
def test_app(app):
    assert not app.debug, "Ensure the app not in debug mode"


@pytest.mark.usefixtures("live_server")
class TestLiveServer:
    def test_server_is_up_and_running(self):
        res = urlopen(url_for("routes.index", _external=True))
        assert b"Hello World" in res.read()
        assert res.code == 200


@pytest.mark.usefixtures("selenium_chrome_driver")
@pytest.mark.usefixtures("live_server")
class TestURLChrome:
    def test_open_url(self):
        self.driver.get("https://www.google.com/")

    def test_homepage_accessible(self):
        """
        GIVEN Our Flask Application is running
        WHEN the '/' page (index) is requested (GET)
        THEN check that page returned conforms to WCAG standards
        """
        self.driver.get(url_for("routes.index", _external=True))
        axe = Axe(
            self.driver,
            ".venv/lib/python3.10/site-packages/"
            "axe_selenium_python/node_modules/axe-core/axe.min.js",
        )
        axe.inject()
        results = axe.run()
        axe.write_results(results, "axe_report.json")
        assert len(results["violations"]) <= 1
