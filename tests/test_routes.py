"""
Tests the routes and their contents using the dict within
"route_testing_conf.py".
"""
from tests.route_testing_conf import routes_and_test_content


def test_routes_status_code(flask_test_client):
    """
    GIVEN Our Flask Hello World Application
    WHEN a route is requested
    THEN check that the get response is successful
    If this test succeedes then our flask application's
    routes are correctly initialised.
    """
    for route, _ in routes_and_test_content.items():

        response = flask_test_client.get(route, follow_redirects=True)
        assert response.status_code == 200


def test_routes_content(flask_test_client):
    """
    GIVEN Our Flask Hello World Application
    WHEN a route is requested
    THEN check that the get response contains the
    expected content.

    If this test succeedes then our flask application's
    routes are correctly initialised.
    """
    for route, should_contain_this in routes_and_test_content.items():

        response = flask_test_client.get(route, follow_redirects=True)
        assert should_contain_this in response.data


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
