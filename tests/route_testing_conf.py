"""
A very basic python configuration file.
Our single source of truth for which
routes need to be tested and their expected
content.
"""
routes_and_test_content = {
    "/": b"Apply for funding to save a building in your community",
    # TODO: re-implement test of tasklist route once
    #  @login_reqired decorator is mocked
    # "/tasklist/test_id": b"Test Fund application",
}
