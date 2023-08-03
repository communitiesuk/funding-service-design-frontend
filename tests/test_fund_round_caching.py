from unittest import mock

from app.helpers import CACHED_FUND_ROUNDS_PROPERTY
from app.helpers import FUNDS_BY_ID_PROPERTY
from app.helpers import FUNDS_BY_SHORT_NAME_PROPERTY
from app.helpers import get_fund_and_round
from app.helpers import ROUNDS_BY_ID_PROPERTY
from app.helpers import ROUNDS_BY_SHORT_NAME_PROPERTY
from app.models.fund import Fund
from app.models.round import Round
from tests.test_data import common_round_data
from tests.test_data import TEST_FUNDS_DATA


def test_get_fund_round_session_populated_fund_and_round(
    flask_test_client, mocker
):
    expected_fund_as_dict = TEST_FUNDS_DATA[0]
    expected_round_as_dict = {
        **common_round_data,
        "fund_id": "111",
        "id": "fsd-r2w2",
        "short_name": "r2w2",
        "title": "closed_round",
        "deadline": "2023-01-01T00:00:01",
    }
    expected_fund = Fund.from_dict(expected_fund_as_dict)
    expected_round = Round.from_dict(expected_round_as_dict)
    with (
        mock.patch(
            "app.helpers.get_round_data", return_value=expected_round
        ) as mock_get_round_by_id,
        mock.patch(
            "app.helpers.get_fund_data", return_value=expected_fund
        ) as mock_get_fund_by_id,
        mock.patch(
            "app.helpers.get_fund_data_by_short_name",
            return_value=expected_fund,
        ) as mock_get_fund_by_short_name,
        mock.patch(
            "app.helpers.get_round_data_by_short_names",
            return_value=expected_round,
        ) as mock_get_round_by_short_name,
        flask_test_client.application.test_request_context(),
    ):
        # with flask_test_client.session_transaction() as session:
        mocker.patch(
            "app.helpers.session",
            {
                CACHED_FUND_ROUNDS_PROPERTY: {
                    FUNDS_BY_ID_PROPERTY: {"123": expected_fund_as_dict},
                    FUNDS_BY_SHORT_NAME_PROPERTY: {
                        "123": expected_fund_as_dict
                    },
                    ROUNDS_BY_ID_PROPERTY: {"123": expected_round_as_dict},
                    ROUNDS_BY_SHORT_NAME_PROPERTY: {
                        "123": expected_round_as_dict
                    },
                }
            },
        )
        # response = flask_test_client.get("/funding-round/123/123")
        fund, round = get_fund_and_round("123", "123", None, None)
        assert fund.id == expected_fund.id
        assert round.id == expected_round.id
        mock_get_round_by_id.assert_not_called()
        mock_get_round_by_short_name.assert_not_called()
        mock_get_fund_by_id.assert_not_called()
        mock_get_fund_by_short_name.assert_not_called()


def test_get_fund_round_session_populated_fund_not_round():
    assert "Not yet written" == "Passed"


def test_get_fund_round_session_populated_round_not_fund():
    assert "Not yet written" == "Passed"


def test_get_fund_round_session_populated_without_this_fund():
    assert "Not yet written" == "Passed"


def test_get_fund_round_session_populated_without_this_round():
    assert "Not yet written" == "Passed"
