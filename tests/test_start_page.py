from unittest import mock

import pytest
from app.default.data import get_default_round_for_fund
from app.default.data import RoundStatus
from app.models.fund import Fund
from app.models.round import Round
from app.models.round import SupportAvailability


default_round_fields = {
    "assessment_criteria_weighting": [],
    "assessment_deadline": "",
    "fund_id": "",
    "title": "test round title",
    "short_name": "SHORT",
    "prospectus": "",
    "instructions": "",
    "contact_details": {"email_address": "blah@google.com"},
    "support_availability": SupportAvailability("", "", ""),
}


@pytest.fixture
def mock_get_fund(mocker):
    mocker.patch(
        "app.default.routes.get_fund_data_by_short_name",
        return_value=Fund(
            "", "Testing Fund", "", "", "test some funding stuff"
        ),
    )


@pytest.fixture
def mock_get_round(mocker):
    mocker.patch(
        "app.default.routes.get_round_data_by_short_names",
        return_value=Round(
            id="1",
            opens="",
            deadline="2023-01-01 12:00:00",
            **default_round_fields,
        ),
    )


def test_old_index_redirect(client):
    result = client.get("/", follow_redirects=False)
    assert result.status_code == 302
    assert result.location == "/cof/r2w3"


def test_start_page_unknown_fund(client, mocker):
    mocker.patch(
        "app.default.routes.get_fund_data_by_short_name", return_value=None
    )
    result = client.get("/bad_fund/r2w2")
    assert result.status_code == 404


def test_start_page_unknown_round(client, mocker, mock_get_fund):
    mocker.patch(
        "app.default.routes.get_round_data_by_short_names", return_value=None
    )
    result = client.get("/cof/bad_round_id")
    assert result.status_code == 404


def test_start_page_not_yet_open(
    client, mocker, mock_get_fund, mock_get_round
):
    mocker.patch(
        "app.default.routes.determine_round_status",
        return_value=RoundStatus(False, True, False),
    )
    result = client.get("/cof/r2w1")
    assert result.status_code == 404


def test_start_page_open(
    client, mocker, mock_get_fund, mock_get_round, templates_rendered
):
    mocker.patch(
        "app.default.routes.determine_round_status",
        return_value=RoundStatus(False, False, True),
    )
    result = client.get("/cof/r2w3")
    assert result.status_code == 200
    assert 1 == len(templates_rendered)
    rendered_template = templates_rendered[0]
    assert rendered_template[0].name == "fund_start_page.html"
    assert rendered_template[1]["fund_title"] == "test some funding stuff"
    assert rendered_template[1]["round_title"] == "test round title"
    assert rendered_template[1]["is_past_submission_deadline"] is False


def test_start_page_closed(
    client, mocker, mock_get_fund, mock_get_round, templates_rendered
):
    mocker.patch(
        "app.default.routes.determine_round_status",
        return_value=RoundStatus(True, False, False),
    )
    result = client.get("/cof/r2w3")
    assert result.status_code == 200
    assert 1 == len(templates_rendered)
    rendered_template = templates_rendered[0]
    assert rendered_template[0].name == "fund_start_page.html"
    assert rendered_template[1]["fund_title"] == "test some funding stuff"
    assert rendered_template[1]["round_title"] == "test round title"
    assert rendered_template[1]["is_past_submission_deadline"] is True


@pytest.mark.parametrize(
    "rounds,expected_default_id",
    [
        (  # 111 opens after 222
            [
                Round(
                    id="111",
                    deadline="2040-01-01 12:00:00",
                    opens="2030-01-01 12:00:00",
                    **default_round_fields,
                ),
                Round(
                    id="222",
                    deadline="2010-01-01 12:00:00",
                    opens="2010-01-01 12:00:00",
                    **default_round_fields,
                ),
            ],
            "111",
        ),
        (  # 333 opens after 444
            [
                Round(
                    id="444",
                    deadline="2010-01-01 12:00:00",
                    opens="2010-01-01 12:00:00",
                    **default_round_fields,
                ),
                Round(
                    id="333",
                    deadline="2040-01-01 12:00:00",
                    opens="2020-01-01 12:00:00",
                    **default_round_fields,
                ),
            ],
            "333",
        ),
        (  # neither open, 666 closed most recently
            [
                Round(
                    id="555",
                    deadline="2010-01-01 12:00:00",
                    opens="2010-01-01 12:00:00",
                    **default_round_fields,
                ),
                Round(
                    id="666",
                    deadline="2020-01-01 12:00:00",
                    opens="2020-01-01 12:00:00",
                    **default_round_fields,
                ),
            ],
            "666",
        ),
    ],
)
def test_get_default_round_for_fund(rounds, expected_default_id, mocker):
    mocker.patch(
        "app.default.data.get_all_rounds_for_fund", return_value=rounds
    )
    result = get_default_round_for_fund("fund")
    assert result.id == expected_default_id


def test_get_default_round_for_fund_no_rounds(mocker):
    mocker.patch("app.default.data.get_all_rounds_for_fund", return_value=[])
    result = get_default_round_for_fund("fund")
    assert result is None


def test_fund_only_start_page(client, mocker):
    mocker.patch(
        "app.default.routes.get_default_round_for_fund",
        return_value=Round(
            id="111", deadline="", opens="", **default_round_fields
        ),
    )
    result = client.get("/cof", follow_redirects=False)
    assert result.status_code == 302
    assert result.location == "/cof/SHORT"


def test_fund_only_start_page_no_rounds(client, mocker):
    mocker.patch(
        "app.default.routes.get_default_round_for_fund", return_value=None
    )
    result = client.get("/cof", follow_redirects=False)
    assert result.status_code == 404


def test_fund_only_start_page_bad_fund(client):
    with mock.patch(
        "app.default.data.get_all_rounds_for_fund"
    ) as mock_get_rounds:
        mock_get_rounds.side_effect = Exception
        result = client.get("/asdf", follow_redirects=False)
        assert result.status_code == 404


def test_favicon_filter(client):
    result = client.get("/favicon.ico", follow_redirects=False)
    assert result.status_code == 404
    assert result.data == b"404"
