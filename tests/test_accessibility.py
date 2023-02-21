from urllib.request import urlopen

import pytest
from bs4 import BeautifulSoup
from flask import url_for


@pytest.mark.app(debug=False)
def test_app(app):
    assert not app.debug, "Ensure the app not in debug mode"


@pytest.mark.usefixtures("live_server")
def test_server_is_up_and_running():
    """
    GIVEN Our Flask Application is running
    WHEN the '/' page (index) is requested (GET)
    THEN check that page returns a 200 response code
    """
    res = urlopen(url_for("routes.index", _external=True))
    assert res.code == 200


@pytest.mark.usefixtures("live_server")
def test_start_page_message_correct():
    """
    GIVEN Our Flask Application is running
    WHEN the '/' page (index) is requested (GET)
    THEN check that page returns a 'Apply for funding to
    save a building in your community' message
    """
    res = urlopen(url_for("routes.index", _external=True))
    soup = BeautifulSoup(res.read(), "html.parser")
    assert (
        "Apply for funding to save a building in your community"
        in soup.find("h1").text
    )
    assert res.code == 200
