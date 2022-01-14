def test_insecure_post_fails(flask_test_client):
  response = flask_test_client.post(
    '/',
    data = dict(email="test@company.com", password="test"),
    follow_redirects=True
    )
  assert response.status_code == 403
