import pytest
from scripts.question_reuse.generate_form import build_form_json


@pytest.mark.parametrize(
    "input_json, exp_results",
    [
        (
            {
                "title": "about-your-organisation",
                "pages": ["organisation-name", "organisation-address"],
            },
            {
                "startPage": "/intro-about-your-organisation",
                "pages": [
                    {
                        "path": "/intro-about-your-organisation",
                        "title": "About your organisation",
                        "next": [{"path": "/organisation-name"}],
                    },
                    {
                        "path": "/organisation-name",
                        "title": "Organisation name",
                        "next": [{"path": "/organisation-address"}],
                        "exp_component_count": 2,
                    },
                    {
                        "path": "/organisation-address",
                        "title": "Registered organisation address",
                        "next": [{"path": "/summary"}],
                    },
                    {
                        "path": "/summary",
                        "title": "Check your answers",
                        "next": [],
                    },
                ],
            },
        )
    ],
)
def test_build_form(input_json, exp_results):
    results = build_form_json(input_json)
    assert results
    for exp_page in exp_results["pages"]:
        result_page = next(
            res_page
            for res_page in results["pages"]
            if res_page["path"] == exp_page["path"]
        )
        assert result_page["title"] == exp_page["title"]
        if "exp_component_count" in exp_page:
            assert (
                len(result_page["components"])
                == exp_page["exp_component_count"]
            )
