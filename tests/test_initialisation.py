"""
Some very basic tests. Tests if the flask client spins
up and serves the index. This is a selected subset
of the test_routes.py test. These tests are marked
"init" so that github actions can run them before
the other tests. This saves time.
This is the most basic set of tests.
"""
import pytest
from tests.route_testing_conf import routes_and_test_content


@pytest.mark.initialisation
def test_flask_initiates(flask_test_client):
    """
    GIVEN Our Flask Hello World Application
    WHEN the '/' page (index) is requested (GET)
    THEN check that the get response is successful.
    If this test succeedes then our flask application
    is ATLEAST up and running without errors.
    """
    response = flask_test_client.get("/", follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.content
def test_helloworld_homepage(flask_test_client):
    """
    GIVEN Our Flask Hello World Application
    WHEN the '/' page (index) is requested (GET)
    THEN check that the homepage (/) contains the phrase
    "Hello World".
    """
    response = flask_test_client.get("/", follow_redirects=True)
    # We grab the expected content from routes_and_test_content
    assert routes_and_test_content["/"] in response.data
