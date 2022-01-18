"""
Tests if selected pages of the website are accessible when rendered,
according to WCAG standards
"""
from urllib.request import urlopen

import pytest
from axe_selenium_python import Axe
from flask import url_for


@pytest.mark.app(debug=False)
def test_app(app):
    assert not app.debug, "Ensure the app not in debug mode"


@pytest.mark.usefixtures("live_server")
class TestLiveServer:
    def test_server_is_up_and_running(self):
        """
        GIVEN Our Flask Application is running
        WHEN the '/' page (index) is requested (GET)
        THEN check that page returns a 200 response code
        """
        res = urlopen(url_for("routes.index", _external=True))
        assert res.code == 200

    def test_hello_world_message(self):
        """
        GIVEN Our Flask Application is running
        WHEN the '/' page (index) is requested (GET)
        THEN check that page returns a 'Hello World' message
        """
        res = urlopen(url_for("routes.index", _external=True))
        assert b"Hello World" in res.read()
        assert res.code == 200


@pytest.mark.usefixtures("selenium_chrome_driver")
@pytest.mark.usefixtures("live_server")
class TestURLsWithChrome:
    def test_homepage_accessible(self):
        """
        GIVEN Our Flask Application is running
        WHEN the '/' page (index) is requested (GET)
        THEN check that page returned conforms to WCAG standards
        """
        self.driver.get(url_for("routes.index", _external=True))
        axe = Axe(
            self.driver,
        )
        axe.inject()
        results = axe.run()
        axe.write_results(results, "axe_report.json")
        assert len(results["violations"]) <= 1

    def test_unknown_page_returns_accessible_404(self):
        """
        GIVEN Our Flask Application is running
        WHEN the '/page-that-does-not-exist' page is requested (GET)
        THEN check that a 404 page that is returned conforms to WCAG standards
        """
        self.driver.get(url_for("routes.index", _external=True) + "rubbish")
        axe = Axe(
            self.driver,
        )
        axe.inject()
        results = axe.run()
        axe.write_results(results, "axe_report.json")
        assert len(results["violations"]) <= 1
