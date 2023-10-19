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
                        "next": [
                            {
                                "path": "/organisation-address",
                                "condition": "organisation_other_names_no",
                            },
                            {
                                "path": "/alternative-organisation-name",
                                "condition": "organisation_other_names_yes",
                            },
                        ],
                        "exp_component_count": 2,
                    },
                    {
                        "path": "/alternative-organisation-name",
                        "title": "Alternative names of your organisation",
                        "next": [
                            {
                                "path": "/organisation-address",
                            }
                        ],
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
                        "exp_component_count": 0,
                    },
                ],
            },
        )
    ],
)
def test_build_form(input_json, exp_results):
    results = build_form_json(input_json)
    assert results
    assert len(results["pages"]) == len(exp_results["pages"])
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
        if "next" in exp_page:
            for exp_next in exp_page["next"]:
                assert exp_next["path"] in [
                    next["path"] for next in result_page["next"]
                ]
                if "condition" in exp_next:
                    assert exp_next["condition"] in [
                        next["condition"] for next in result_page["next"]
                    ]
