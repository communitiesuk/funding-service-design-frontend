import copy
import json
import os

import click
from scripts.question_reuse.config.lookups import LOOKUPS
from scripts.question_reuse.config.themes_to_reuse import THEMES_TO_REUSE


BASIC_SECTION_STRUCTURE = {"id": None, "name": None, "sub_criteria": []}

BASIC_SUB_CRITERIA_STRUCTURE = {"id": None, "name": None, "themes": []}

BASIC_THEME_STRUCTURE = {"id": None, "name": None, "answers": []}

# TODO this is copied from fund-store metadata_utils for now
form_json_to_assessment_display_types = {
    "numberfield": "integer",
    "textfield": "text",
    "yesnofield": "text",
    "freetextfield": "free_text",
    "checkboxesfield": "list",
    "multiinputfield": "table",
    "clientsidefileuploadfield": "s3bucketPath",
    "radiosfield": "text",
    "emailaddressfield": "text",
    "telephonenumberfield": "text",
    "ukaddressfield": "address",
}


def build_answer_from_component(component_name, component, form_name) -> dict:
    result = {
        "field_id": component_name,
        "form_name": form_name,
        "field_type": component["type"],
        "presentation_type": form_json_to_assessment_display_types.get(
            component["type"].lower(), None
        ),
        "question": component["title"],
    }

    return result


def find_component_in_field_info(component_name: str, field_info: dict):
    for form_name, fields in field_info.items():
        for field in fields:
            if field["field_id"] == component_name:
                return field
    return None


def build_theme(theme_id: str, field_info: dict):
    result = copy.deepcopy(BASIC_THEME_STRUCTURE)
    result.update({"id": theme_id, "name": LOOKUPS[theme_id]})
    for answer in THEMES_TO_REUSE[theme_id]["answers"]:
        result["answers"].append(
            # build_answer_from_component(answer, COMPONENTS_TO_REUSE[answer])
            find_component_in_field_info(answer, field_info)
        )

    return result


def build_sub_criteria(sub_criteria, field_info: dict):
    result = copy.deepcopy(BASIC_SUB_CRITERIA_STRUCTURE)
    result.update(
        {"id": sub_criteria["id"], "name": LOOKUPS[sub_criteria["id"]]}
    )
    for theme in sub_criteria["themes"]:
        result["themes"].append(build_theme(theme, field_info))
    return result


def build_assessment_config(input_data: dict, field_info: dict) -> dict:
    results = {}
    for key, value in input_data.items():
        # key = 'unscored_sections'
        assessment_sections = []
        for section in value:
            # id = 'unscored' or 'declarations'
            assessment_section = copy.deepcopy(BASIC_SECTION_STRUCTURE)
            assessment_section.update(
                {"id": section["id"], "name": LOOKUPS[section["id"]]}
            )

            for sc in section["subcriteria"]:
                assessment_section["sub_criteria"].append(
                    build_sub_criteria(sc, field_info)
                )

            assessment_sections.append(assessment_section)
        results[key] = assessment_sections

    return results


@click.command()
@click.option(
    "--input_folder",
    default="./scripts/question_reuse/test_data/in/",
    help="Input configuration",
    prompt=True,
)
@click.option(
    "--input_file",
    default="assmnt_unscored.json",
    help="Input configuration",
    prompt=True,
)
@click.option(
    "--output_folder",
    default="./scripts/question_reuse/test_data/out",
    help="Output destination",
    prompt=True,
)
@click.option(
    "--output_file",
    default="assessment_mapping_unscored.json",
    help="Output destination",
    prompt=True,
)
@click.option(
    "--field_info_file",
    default=(
        "./scripts/question_reuse/test_data/in/test-org-info-field-info.json"
    ),
    help="Input configuration",
    prompt=True,
)
def generate_assessment_config(
    input_folder, input_file, output_folder, output_file, field_info_file
):
    with open(os.path.join(input_folder, input_file), "r") as f:
        input_data = json.load(f)

    with open(field_info_file, "r") as f:
        field_info = json.load(f)

    assessment_config = build_assessment_config(input_data, field_info)

    with open(os.path.join(output_folder, output_file), "w") as f:
        json.dump(assessment_config, f)


if __name__ == "__main__":
    generate_assessment_config()
