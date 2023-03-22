"""
A very basic python configuration file.
Our single source of truth for which
routes need to be tested and their expected
content.
"""
routes_and_test_content = {
    "/": b"Apply for funding to save an asset in your community",
    "/tasklist/test_id": (
        b"Application for funding to save an asset in your community"
    ),
}
