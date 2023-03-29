"""
Tests the routes and their contents using the dict within
"route_testing_conf.py".
"""
from unittest import mock

from app.default.data import get_round_data_fail_gracefully
from bs4 import BeautifulSoup
from requests import HTTPError
from tests.route_testing_conf import routes_and_test_content


def test_routes_status_code(flask_test_client, monkeypatch, mocker):
    """
    GIVEN Our Flask Application
    WHEN a route is requested
    THEN check that the get response is successful
    If this test succeeds then our flask application's
    routes are correctly initialised.
    """

    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )
    for route, _ in routes_and_test_content.items():
        response = flask_test_client.get(route, follow_redirects=True)
        assert (
            200 == response.status_code
        ), f"Incorrect status code returned for route {route}"


def test_routes_content(flask_test_client, monkeypatch):
    """
    GIVEN Our Flask Application
    WHEN a route is requested
    THEN check that the get response contains the
    expected content.

    If this test succeedes then our flask application's
    routes are correctly initialised.
    """

    monkeypatch.setattr(
        "fsd_utils.authentication.decorators._check_access_token",
        lambda: {"accountId": "test-user"},
    )
    for route, should_contain_this in routes_and_test_content.items():
        response = flask_test_client.get(route, follow_redirects=True)
        assert should_contain_this in response.data, f"Error in route {route}"


def test_dodgy_url_returns_404(flask_test_client):
    """
    GIVEN Our Flask Hello World Application
    WHEN a invalid route is requested
    THEN check that the get a 404 response

    If this test succeedes then our flask application's
    routes are correctly initialised.
    """
    response = flask_test_client.get("/rubbish", follow_redirects=True)
    assert response.status_code == 404


def test_page_title_includes_heading(flask_test_client):
    response = flask_test_client.get("/", follow_redirects=True)
    soup = BeautifulSoup(response.data, "html.parser")
    assert (
        soup.title.string
        == "Start or continue an application for funding to save an asset in"
        " your community - Apply for funding to save an asset in your"
        " community"
    )


def test_page_footer_includes_correct_title_and_link_text(flask_test_client):
    response = flask_test_client.get("/", follow_redirects=True)
    soup = BeautifulSoup(response.data, "html.parser")
    assert all(
        [
            string in soup.footer.text
            for string in [
                "Support links",
                "Privacy",
                "Cookies",
                "Accessibility",
                "Statement",
                "Contact us",
            ]
        ]
    )


def test_get_round_data_fail_gracefully(app, mocker):
    mocker.patch("app.default.data.get_lang", return_value="en")
    with mock.patch(
        "app.default.data.get_data"
    ) as get_data_mock, app.app_context():
        get_data_mock.side_effect = HTTPError()
        round_data = get_round_data_fail_gracefully("cof", "r2w2")
        assert round_data.id == ""
