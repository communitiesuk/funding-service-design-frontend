from app.models.round import Round
from bs4 import BeautifulSoup


empty_round_data = Round(
    id="",
    assessment_deadline="",
    deadline="",
    fund_id="",
    opens="",
    title="",
    short_name="",
    prospectus="",
    privacy_notice="",
    instructions="",
    contact_email="",
    contact_phone="",
    contact_textphone="",
    support_days="",
    support_times="",
    feedback_link="",
    project_name_field_id="",
    application_guidance="",
)

default_round_fields = {
    "id": "111",
    "deadline": "2040-01-01 12:00:00",
    "opens": "2030-01-01 12:00:00",
    "assessment_deadline": "",
    "fund_id": "",
    "title": "test round title",
    "short_name": "SHORT",
    "prospectus": "",
    "privacy_notice": "",
    "instructions": "",
    "contact_email": "test@example.com",
    "contact_phone": "123456789",
    "contact_textphone": "123456789",
    "support_times": "9-5",
    "support_days": "Mon-Fri",
    "project_name_field_id": "",
    "feedback_link": "",
    "application_guidance": "",
}
default_round_data = Round(**default_round_fields)


def test_404(client, mocker):
    mocker.patch(
        "app.default.error_routes.get_round_data_fail_gracefully",
        return_value=default_round_data,
    )
    response = client.get("not_found?fund=test_fund&round=bad_round_id")
    assert response.status_code == 404
    soup = BeautifulSoup(response.data, "html.parser")
    assert "test@example.com" in soup.find("li").text


def test_404_with_bad_fund(client, mocker):
    mocker.patch(
        "app.default.error_routes.get_round_data_fail_gracefully",
        return_value=empty_round_data,
    )
    mocker.patch(
        "app.default.error_routes.get_default_round_for_fund",
        return_value=None,
    )
    response = client.get("not_found?fund=bad_fund&round=r2w2")
    assert response.status_code == 404
    soup = BeautifulSoup(response.data, "html.parser")
    assert "fsd.support@levellingup.gov.uk" in soup.find("li").text


def test_404_with_bad_round(client, mocker):
    mocker.patch(
        "app.default.error_routes.get_round_data_fail_gracefully",
        return_value=empty_round_data,
    )
    mocker.patch(
        "app.default.error_routes.get_default_round_for_fund",
        return_value=default_round_data,
    )
    response = client.get("not_found?fund=test_fund&round=bad_round_id")
    assert response.status_code == 404
    soup = BeautifulSoup(response.data, "html.parser")
    assert "test@example.com" in soup.find("li").text


def test_404_with_bad_fund_n_round(client, mocker):
    mocker.patch(
        "app.default.error_routes.get_round_data_fail_gracefully",
        return_value=empty_round_data,
    )
    mocker.patch(
        "app.default.error_routes.get_default_round_for_fund",
        return_value=None,
    )
    response = client.get("not_found?fund=bad_fund&round=bad_round_id")
    assert response.status_code == 404
    soup = BeautifulSoup(response.data, "html.parser")
    assert "fsd.support@levellingup.gov.uk" in soup.find("li").text


def test_500(client, mocker):
    mocker.patch(
        "app.default.error_routes.get_round_data_fail_gracefully",
        return_value=default_round_data,
    )
    response = client.get(
        "unauthorised_error?fund=test_fund&round=bad_round_id"
    )
    assert response.status_code == 404
    soup = BeautifulSoup(response.data, "html.parser")
    assert "test@example.com" in soup.find("li").text


def test_500_with_bad_fund_n_round(client, mocker):
    mocker.patch(
        "app.default.error_routes.get_round_data_fail_gracefully",
        return_value=empty_round_data,
    )
    mocker.patch(
        "app.default.error_routes.get_default_round_for_fund",
        return_value=None,
    )
    response = client.get(
        "unauthorised_error?fund=bad_fund&round=bad_round_id"
    )
    assert response.status_code == 404
    soup = BeautifulSoup(response.data, "html.parser")
    assert "fsd.support@levellingup.gov.uk" in soup.find("li").text
