import json
from config.envs.default import DefaultConfig
class TestContinueApplication:
    file = open("tests/api_data/endpoint_data.json")
    data = json.loads(file.read())
    TEST_ID = "test_id"
    TEST_APPLICATION_STORE_DATA = data[
        f"http://application_store/applications/{TEST_ID}"
    ]
    REHYDRATION_TOKEN = "test_token"

    def test_continue_application_correct_user(self, flask_test_client, mocker, monkeypatch):
        monkeypatch.setattr(
            "fsd_utils.authentication.decorators._check_access_token",
            lambda: {"accountId": "test-user"},
        )
        mocker.patch(
            "app.default.data.get_application_data",
            return_value=self.TEST_APPLICATION_STORE_DATA,
        )
        mocker.patch(
            "app.default.routes.format_rehydrate_payload",
            return_value="rehydrate_payload"
        )
        mocker.patch(
            "app.default.routes.get_token_to_return_to_application",
            return_value=self.REHYDRATION_TOKEN
        )
        expected_redirect_url = DefaultConfig.FORM_REHYDRATION_URL.format(
            rehydration_token=self.REHYDRATION_TOKEN
        )
        response = flask_test_client.get(f"/continue_application/{self.TEST_ID}", follow_redirects=False)
        assert 302 == response.status_code, "Incorrect status code"
        assert expected_redirect_url == response.location, "Incorrect redirect url"

    def test_continue_application_bad_user(self, flask_test_client, mocker, monkeypatch):
        monkeypatch.setattr(
            "fsd_utils.authentication.decorators._check_access_token",
            lambda: {"accountId": "different-user"},
        )
        mocker.patch(
            "app.default.data.get_application_data",
            return_value=self.TEST_APPLICATION_STORE_DATA,
        )
        mocker.patch(
            "app.default.routes.format_rehydrate_payload",
            return_value="rehydrate_payload"
        )
        mocker.patch(
            "app.default.routes.get_token_to_return_to_application",
            return_value=self.REHYDRATION_TOKEN
        )
        expected_redirect_url = DefaultConfig.FORM_REHYDRATION_URL.format(
            rehydration_token=self.REHYDRATION_TOKEN
        )
        response = flask_test_client.get(f"/continue_application/{self.TEST_ID}", follow_redirects=False)
        assert 401 == response.status_code, "Incorrect status code"
