"""
Some very basic tests. Tests if the flask client spins
up and serves the index. This is a selected subset
of the test_routes.py test. These tests are marked
"init" so that github actions can run them before
the other tests. This saves time.
This is the most basic set of tests.
"""
from tests.route_testing_conf import routes_and_test_content


def test_flask_initiates(flask_test_client):
    """
    GIVEN Our Flask Hello World Application
    WHEN the '/' page (index) is requested (GET)
    THEN check that the get response is successful.
    If this test succeeds then our flask application
    is AT LEAST up and running without errors.
    """
    response = flask_test_client.get("/", follow_redirects=True)
    assert response.status_code == 200


def test_helloworld_homepage(flask_test_client):
    """
    GIVEN Our Flask Application
    WHEN the '/' page (index) is requested (GET)
    THEN check that the homepage (/) contains the phrase
    "Apply for funding to save a building in your community".
    """
    response = flask_test_client.get("/", follow_redirects=True)
    # We grab the expected content from routes_and_test_content
    assert routes_and_test_content["/"] in response.data


def test_healthcheck(flask_test_client):
    response = flask_test_client.get("/healthcheck")

    expected_dict = {"checks": [{"check_flask_running": "OK"}]}
    assert response.status_code == 200, "Unexpected status code"
    assert response.json == expected_dict, "Unexpected json body"
