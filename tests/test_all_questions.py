from bs4 import BeautifulSoup
from werkzeug import test


def test_all_questions_page_from_short_name(flask_test_client):
    response: test.TestResponse = flask_test_client.get(
        "/all_questions/COF/R2W3?lang=en"
    )
    assert response.status_code == 200
    soup = BeautifulSoup(response.data, "html.parser")
    assert soup.find("h1").text == "Full list of application questions"
    assert "Community Ownership Fund Round 2 Window 3" in soup.get_text()
