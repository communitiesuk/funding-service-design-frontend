"""
Tests the routes and their contents using the dict within
"route_testing_conf.py".
"""
from unittest import mock

import pytest
from app.default.data import get_round_data_fail_gracefully
from app.models.fund import Fund
from bs4 import BeautifulSoup
from config import Config
from flask import render_template
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
        render_template("index.html")
    assert len(templates_rendered) == 1
    assert (
        templates_rendered[0][1]["service_title"]
        == "Apply for " + expected_title
    )
