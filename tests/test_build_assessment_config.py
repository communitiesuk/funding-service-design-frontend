import copy
import json

from scripts.question_reuse.generate_assessment_config import (
    build_assessment_config,
)

TEST_DATA_UNSCORED_NO_SUBCRITERIA = {
    "unscored_sections": [
        {"id": "unscored", "subcriteria": []},
        {"id": "declarations", "subcriteria": []},
    ]
}


TEST_DATA_UNSCORED_WITH_SUBCRITERIA = copy.deepcopy(
    TEST_DATA_UNSCORED_NO_SUBCRITERIA
)
TEST_DATA_UNSCORED_WITH_SUBCRITERIA["unscored_sections"][0]["subcriteria"] = [
    {
        "id": "organisation_information",
        "themes": ["general_information", "activities"],
    }
]

TEST_FORM_NAME = "test-org-info-form"

with open(
    "./scripts/question_reuse/test_data/in/test-org-info-field-info.json"
) as f:
    TEST_FIELD_INFO = json.load(f)


def test_build_basic_structure():

    results = build_assessment_config(TEST_DATA_UNSCORED_NO_SUBCRITERIA, {})
    assert "unscored_sections" in results
    unscored = next(
        section
        for section in results["unscored_sections"]
        if section["id"] == "unscored"
    )
    assert unscored["name"] == "Unscored"


def test_with_field_info():
    results = build_assessment_config(
        TEST_DATA_UNSCORED_WITH_SUBCRITERIA, TEST_FIELD_INFO
    )
    assert len(results["unscored_sections"]) == 2
    unscored_subcriteria = next(
        section
        for section in results["unscored_sections"]
        if section["id"] == "unscored"
    )["sub_criteria"]

    assert unscored_subcriteria[0]["name"] == "Organisation information"

    unscored_themes = unscored_subcriteria[0]["themes"]
    assert len(unscored_themes) == 2

    general_info = unscored_themes[0]
    assert general_info["name"] == "General information"
    assert len(general_info["answers"]) == 4

    activities = unscored_themes[1]
    assert activities["name"] == "Activities"
    assert len(activities["answers"]) == 1
