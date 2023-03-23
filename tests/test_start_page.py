from app.models.fund import Fund


def test_start_page_unknown_fund(client, mocker):
    mocker.patch(
        "app.default.routes.get_fund_data_by_short_name", return_value=None
    )
    result = client.get("/bad_fund/r2w2")
    assert result.status_code == 404


def test_start_page_unknown_round(client, mocker):
    mocker.patch(
        "app.default.routes.get_fund_data_by_short_name",
        return_value=Fund("", "", "", "", ""),
    )
    mocker.patch(
        "app.default.routes.get_round_data_by_short_names", return_value=None
    )
    result = client.get("/cof/bad_round_id")
    assert result.status_code == 404
