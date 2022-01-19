"""
Tests if selected pages of the website are accessible when rendered,
according to WCAG standards
"""
import os
from urllib.request import urlopen

import pytest
from axe_selenium_python import Axe
from flask import url_for
from json2html import json2html


def print_axe_report(results, route_rel, route_name):
    """
    Prints an html report from aXe generated results
    """
    results_html = json2html.convert(
        json=results["violations"],
        table_attributes="border='1' cellpadding='10' cellspacing='0' bordercolor='black'",  # noqa
    )
    heading = "<h1>Axe Violations Report for route /" + route_rel + "</h1>"
    results_with_title = heading + results_html

    report_filename = route_name
    if not report_filename:
        if route_rel:
            report_filename = route_rel.replace("/", "_")
        else:
            report_filename = "index"

    os.makedirs("axe_reports", exist_ok=True)
    f = open("axe_reports/" + report_filename + ".html", "w")
    f.write(results_with_title)
    f.close()


@pytest.mark.usefixtures("selenium_chrome_driver")
@pytest.mark.usefixtures("live_server")
def run_axe_and_print_report(driver, route_rel="", route_name=None):
    """
    Generates an html report from aXe generate has generated a report
    :return A json report
    """
    route = url_for("routes.index", _external=True) + route_rel
    driver.get(route)
    axe = Axe(driver)
    axe.inject()
    results = axe.run()
    print_axe_report(results, route_rel, route_name)

    return results


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
        route_rel = ""
        results = run_axe_and_print_report(self.driver, str(route_rel))
        assert len(results["violations"]) <= 1
        assert (
            len(results["violations"]) == 0
            or results["violations"][0]["impact"] == "minor"
        )

    def test_unknown_page_returns_accessible_404(self):
        """
        GIVEN Our Flask Application is running
        WHEN the '/page-that-does-not-exist' page is requested (GET)
        THEN check that a 404 page that is returned conforms to WCAG standards
        """
        route_rel = "page-does-not-exist"
        results = run_axe_and_print_report(self.driver, str(route_rel))

        assert len(results["violations"]) <= 1
        assert (
            len(results["violations"]) == 0
            or results["violations"][0]["impact"] == "minor"
        )
