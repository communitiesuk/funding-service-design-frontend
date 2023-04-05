from unittest import mock

import pytest
from app.default.data import get_round_data_fail_gracefully
from app.models.fund import Fund
from bs4 import BeautifulSoup
from config import Config
from flask import render_template
from requests import HTTPError


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


fund_args = {
    "id": "",
    "name": "Testing Fund",
    "short_name": "",
    "description": "",
}
short_name_fund = Fund(**fund_args, title="Test Fund by short name")
id_fund = Fund(**fund_args, title="Test Fund by ID")
default_fund = Fund(**fund_args, title="Default Fund")


@pytest.mark.parametrize(
    "key_name, view_args_value, args_value, expected_title",
    [
        ("fund_short_name", "TEST", None, short_name_fund.title),
        ("fund_short_name", None, None, default_fund.title),
        ("fund_short_name", None, "TEST", default_fund.title),
        ("fund_id", "TEST", None, id_fund.title),
        ("fund_id", None, None, default_fund.title),
        ("fund_id", None, "TEST", id_fund.title),
        ("fund", None, "TEST", short_name_fund.title),
        ("fund", None, None, default_fund.title),
        ("fund", "TEST", None, default_fund.title),
    ],
)
def test_inject_service_name(
    key_name,
    view_args_value,
    args_value,
    expected_title,
    app,
    templates_rendered,
    mocker,
):
    mocker.patch(
        "app.create_app.get_fund_data_by_short_name",
        return_value=short_name_fund,
    )
    mocker.patch(
        "app.create_app.get_fund_data",
        new=lambda fund_id, as_dict: default_fund
        if fund_id == Config.DEFAULT_FUND_ID
        else id_fund,
    )
    request_mock = mocker.patch("app.create_app.request")
    request_mock.view_args.get = (
        lambda key: view_args_value if key == key_name else None
    )
    request_mock.args.get = lambda key: args_value if key == key_name else None
    with app.app_context():
        render_template("fund_start_page.html")
    assert len(templates_rendered) == 1
    assert (
        templates_rendered[0][1]["service_title"]
        == "Apply for " + expected_title
    )


def test_healthcheck(flask_test_client):
    response = flask_test_client.get("/healthcheck")

    expected_dict = {
        "checks": [{"check_flask_running": "OK"}],
        "version": "abc123",
    }
    assert response.status_code == 200, "Unexpected status code"
    assert response.json == expected_dict, "Unexpected json body"


@pytest.mark.app(debug=False)
def test_app(app):
    assert not app.debug, "Ensure the app not in debug mode"
