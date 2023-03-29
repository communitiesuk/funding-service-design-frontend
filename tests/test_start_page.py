import pytest
from app.default.data import RoundStatus
from app.models.fund import Fund
from app.models.round import ContactDetails
from app.models.round import Round
from app.models.round import SupportAvailability


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
            "",
            [],
            "",
            "",
            "",
            "",
            "test round title",
            "",
            "",
            ContactDetails("", "", ""),
            SupportAvailability("", "", ""),
        ),
    )


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
        return_value=RoundStatus(False, True),
    )
    result = client.get("/cof/r2w1")
    assert result.status_code == 404


def test_start_page_open(
    client, mocker, mock_get_fund, mock_get_round, templates_rendered
):
    mocker.patch(
        "app.default.routes.determine_round_status",
        return_value=RoundStatus(False, False),
    )
    result = client.get("/cof/r2w3")
    assert result.status_code == 200
    assert 1 == len(templates_rendered)
    rendered_template = templates_rendered[0]
    assert rendered_template[0].name == "fund_start_page.html"
    assert rendered_template[1]["fund_title"] == "test some funding stuff"
    assert rendered_template[1]["round_title"] == "test round title"
