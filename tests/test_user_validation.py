import json

from app.default.data import RoundStatus
from app.models.account import Account
from app.models.application import Application
from app.models.fund import Fund
from app.models.round import Round
from config.envs.default import DefaultConfig


class TestUserValidation:
    file = open("tests/api_data/endpoint_data.json")
    data = json.loads(file.read())
    TEST_ID = "test_id"
    TEST_USER = "test-user"
    TEST_APPLICATION_STORE_DATA = data[
        f"application_store/applications/{TEST_ID}"
    ]
    TEST_FUND_DATA = data[
        "fund_store/funds/funding-service-design?language=en"
    ]
    TEST_ROUND_DATA = data[
        "fund_store/funds/47aef2f5-3fcb-4d45-acb5-f0152b5f03c4/"
        "rounds/c603d114-5364-4474-a0c4-c41cbf4d3bbd?language=en"
    ]
    TEST_ROUND_STORE_DATA = data[
        "fund_store/funds/funding-service-design/rounds/summer?language=en"
    ]
    REHYDRATION_TOKEN = "test_token"

    def test_continue_application_correct_user(
        self, flask_test_client, mocker, monkeypatch
    ):
        monkeypatch.setattr(
            "fsd_utils.authentication.decorators._check_access_token",
            lambda: {"accountId": self.TEST_USER},
        )
        mocker.patch(
            "app.default.application_routes.get_application_data",
            return_value=Application.from_dict(
                self.TEST_APPLICATION_STORE_DATA
            ),
        )
        mocker.patch(
            "app.default.application_routes.format_rehydrate_payload",
            return_value="rehydrate_payload",
        )
        mocker.patch(
            "app.default.application_routes."
            "get_token_to_return_to_application",
            return_value=self.REHYDRATION_TOKEN,
        )
        expected_redirect_url = DefaultConfig.FORM_REHYDRATION_URL.format(
            rehydration_token=self.REHYDRATION_TOKEN
        )
        response = flask_test_client.get(
            f"/continue_application/{self.TEST_ID}", follow_redirects=False
        )
        assert 302 == response.status_code, "Incorrect status code"
        assert (
            expected_redirect_url == response.location
        ), "Incorrect redirect url"

    def test_continue_application_bad_user(
        self, flask_test_client, mocker, monkeypatch
    ):
        monkeypatch.setattr(
            "fsd_utils.authentication.decorators._check_access_token",
            lambda: {"accountId": "different-user"},
        )
        mocker.patch(
            "app.default.application_routes.get_application_data",
            return_value=Application.from_dict(
                self.TEST_APPLICATION_STORE_DATA
            ),
        )
        mocker.patch(
            "app.default.data.get_round_data_fail_gracefully",
            return_value=self.TEST_ROUND_DATA,
        )

        response = flask_test_client.get(
            f"/continue_application/{self.TEST_ID}", follow_redirects=False
        )
        assert 401 == response.status_code, "Incorrect status code"

    def test_tasklist_correct_user(
        self, flask_test_client, mocker, monkeypatch
    ):
        monkeypatch.setattr(
            "fsd_utils.authentication.decorators._check_access_token",
            lambda: {"accountId": self.TEST_USER},
        )
        mocker.patch(
            "app.default.application_routes.get_account",
            return_value=Account.from_json(
                {
                    "account_id": self.TEST_USER,
                    "email_address": "test@example.com",
                }
            ),
        )
        mocker.patch(
            "app.default.application_routes.get_application_data",
            return_value=Application.from_dict(
                self.TEST_APPLICATION_STORE_DATA
            ),
        )
        mocker.patch(
            "app.default.application_routes.get_fund_data",
            return_value=Fund.from_dict(self.TEST_FUND_DATA),
        )
        mocker.patch(
            "app.default.application_routes.get_round_data",
            return_value=Round.from_dict(self.TEST_ROUND_DATA),
        )

        response = flask_test_client.get(
            f"/tasklist/{self.TEST_ID}", follow_redirects=False
        )
        assert 200 == response.status_code, "Incorrect status code"
        assert b"<title>Task List" in response.data
        assert b"TEST-REF-A</dd>" in response.data

    def test_tasklist_bad_user(self, flask_test_client, mocker, monkeypatch):
        monkeypatch.setattr(
            "fsd_utils.authentication.decorators._check_access_token",
            lambda: {"accountId": "different-user"},
        )
        mocker.patch(
            "app.default.application_routes.get_application_data",
            return_value=Application.from_dict(
                self.TEST_APPLICATION_STORE_DATA
            ),
        )

        response = flask_test_client.get(
            f"/tasklist/{self.TEST_ID}", follow_redirects=False
        )
        assert 401 == response.status_code, "Incorrect status code"

    def test_submit_correct_user(self, flask_test_client, mocker, monkeypatch):

        mocker.patch(
            "app.default.application_routes.get_application_data",
            return_value=Application.from_dict(
                self.TEST_APPLICATION_STORE_DATA
            ),
        )
        monkeypatch.setattr(
            "fsd_utils.authentication.decorators._check_access_token",
            lambda: {"accountId": self.TEST_USER},
        )
        mocker.patch(
            "app.default.application_routes.determine_round_status",
            return_value=RoundStatus(False, False),
        )
        mocker.patch(
            "app.default.application_routes."
            + "format_payload_and_submit_application",
            return_value={
                "id": self.TEST_ID,
                "email": "test@test.com",
                "reference": "ABC-123",
            },
        )

        response = flask_test_client.post(
            "/submit_application",
            data={"application_id": self.TEST_ID},
            follow_redirects=False,
        )
        assert 200 == response.status_code, "Incorrect status code"
        assert b"Application complete" in response.data
        assert (
            b"Your reference number<br><strong>ABC-123</strong>"
            in response.data
        )

    def test_submit_correct_user_bad_dates(
        self, flask_test_client, mocker, monkeypatch
    ):

        mocker.patch(
            "app.default.application_routes.get_application_data",
            return_value=Application.from_dict(
                self.TEST_APPLICATION_STORE_DATA
            ),
        )
        monkeypatch.setattr(
            "fsd_utils.authentication.decorators._check_access_token",
            lambda: {"accountId": self.TEST_USER},
        )
        mocker.patch(
            "app.default.application_routes.determine_round_status",
            return_value=RoundStatus(True, True),
        )

        response = flask_test_client.post(
            "/submit_application",
            data={"application_id": self.TEST_ID},
            follow_redirects=False,
        )
        assert response.status_code == 302
        assert "/account" == response.location

    def test_submit_bad_user(self, flask_test_client, mocker, monkeypatch):
        monkeypatch.setattr(
            "fsd_utils.authentication.decorators._check_access_token",
            lambda: {"accountId": "different-user"},
        )
        mocker.patch(
            "app.default.application_routes.get_application_data",
            return_value=Application.from_dict(
                self.TEST_APPLICATION_STORE_DATA
            ),
        )
        mocker.patch(
            "app.default.data.get_round_data_fail_gracefully",
            return_value=self.TEST_ROUND_DATA,
        )

        response = flask_test_client.post(
            "/submit_application",
            data={"application_id": self.TEST_ID},
            follow_redirects=False,
        )
        assert 401 == response.status_code, "Incorrect status code"
