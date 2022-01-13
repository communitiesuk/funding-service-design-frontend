# flake8: noqa: F811
from tests.testconf import flask_test_client  # noqa


def test_flask_initiates(flask_test_client):
    """
    GIVEN Our Flask Hello World Application
    WHEN the '/' page (index) is requested (GET)
    THEN check that the get response is successful.
    If this test succeedes then our flask application
    is ATLEAST up and running.
    """
    response = flask_test_client.get("/", follow_redirects=True)
    assert response.status_code == 200


def test_helloworld_homepage(flask_test_client):
    """
    GIVEN Our Flask Hello World Application
    WHEN the '/' page (index) is requested (GET)
    THEN check that the homepage contains the phrase
    "Hello World".
    """
    response = flask_test_client.get("/", follow_redirects=True)
    assert b"Hello World" in response.data
