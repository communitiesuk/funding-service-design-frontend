def test_csrf_files(flask_test_client):
    """
    The test should return unauthorised message
     if the request is not received from https server
    """
    response = flask_test_client.post("/", follow_redirects=True)
    assert response.status_code == 401
