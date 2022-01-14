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
    for route, _ in routes_and_test_content:

        response = flask_test_client.get(route, follow_redirects=True)
        if route == "/404":
            # This is the only route for which
            # success means a 404 status code.
            assert response.status_code == 404
        else:
            assert response.status_code == 200
