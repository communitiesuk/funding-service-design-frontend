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


def generate_field_info_from_forms(forms_dir: str) -> dict:
    """Generates the display info for all fields in a form

    Args:
        forms_dir (str): Directory containing the forms

    Returns:
        dict: Dictionary of field IDs to display info
    """
    results = {}
    for file_name in os.listdir(forms_dir):
        with open(os.path.join(forms_dir, file_name), "r") as f:
            form_data = json.load(f)
            results.update(
                build_answers_from_form(form_data, file_name.split(".")[0])
            )

    return results


def build_answers_from_form(form_data: dict, form_name: str) -> dict:
    """Generates the list of display info for a particular form

    Args:
        form_data (dict): Full form data
        form_name (str): name of this form

    Returns:
        dict: Dictionary of field IDs to display info
    """
    results = {}
    for page in form_data["pages"]:
        for component in page["components"]:
            question = component.get("title", None)
            if component["type"].lower() == "multiinputfield":
                question = [page["title"]]
                child_fields = {}
                for field in component["children"]:
                    child_fields[field["name"]] = {
                        "column_title": field["title"],
                        "type": field["type"],
                    }
                question.append(child_fields)

            results[component["name"]] = {
                "field_id": component["name"],
                "form_name": form_name,
                "field_type": component["type"],
                "presentation_type": form_json_to_assessment_display_types.get(
                    component["type"].lower(), None
                ),
                "question": question,
            }

    return results


def build_theme(theme_id: str, field_info: dict) -> dict:
    """Creates a theme object and populates with the display info for the answers in that theme

    Args:
        theme_id (str): ID of the theme
        field_info (dict): Dictionary of field display info for all fields

    Returns:
        dict: Dictionary representing a theme within the assessment config
    """
    result = copy.deepcopy(BASIC_THEME_STRUCTURE)
    result.update({"id": theme_id, "name": LOOKUPS[theme_id]})
    for answer in THEMES_TO_REUSE[theme_id]["answers"]:
        result["answers"].append(
            field_info.get(answer, None)
        )

    return result


def build_sub_criteria(sub_criteria: dict, field_info: dict) -> dict:
    """Generates a sub criteria, containing themes

    Args:
        sub_criteria (dict): Input subcriteria details
        field_info (dict): Dictionary of fields and their display info

    Returns:
        dict: Dictionary of subcriteria IDs to their config (containing themes)
    """
    result = copy.deepcopy(BASIC_SUB_CRITERIA_STRUCTURE)
    result.update(
        {"id": sub_criteria["id"], "name": LOOKUPS[sub_criteria["id"]]}
    )
    for theme in sub_criteria["themes"]:
        result["themes"].append(build_theme(theme, field_info))
    return result


def build_assessment_config(input_data: dict, field_info: dict) -> dict:
    """Builds a dictionary represting the full assessment config based on the input data 

    Args:
        input_data (dict): Dictionary of input data (eg. test_data/in/ns_unscored.json)
        field_info (dict): Dictionary of field IDs to their display info

    Returns:
        dict: Full assessment display config
    """
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
    "--forms_dir",
    default="./scripts/question_reuse/test_data/out/forms/",
    help="Directory containing forms",
    prompt=True,
)
def generate_assessment_config(
    input_folder,
    input_file,
    output_folder,
    output_file,
    forms_dir,
):
    with open(os.path.join(input_folder, input_file), "r") as f:
        input_data = json.load(f)

    field_info = generate_field_info_from_forms(forms_dir)

    assessment_config = build_assessment_config(input_data, field_info)

    with open(os.path.join(output_folder, output_file), "w") as f:
        json.dump(assessment_config, f)


if __name__ == "__main__":
    generate_assessment_config()
