"""
Tests the routes and their contents using the dict within
"route_testing_conf.py".
"""
from bs4 import BeautifulSoup
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
