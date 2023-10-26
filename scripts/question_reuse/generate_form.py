import copy
import json
import os

import click
from scripts.question_reuse.config.components_to_reuse import (
    COMPONENTS_TO_REUSE,
)
from scripts.question_reuse.config.lookups import LOOKUPS
from scripts.question_reuse.config.pages_to_reuse import PAGES_TO_REUSE
import datetime
from scripts.question_reuse.config.sub_pages_to_reuse import SUB_PAGES_TO_REUSE

BASIC_FORM_STRUCTURE = {
    "metadata": {},
    "startPage": None,
    "backLinkText": "Go back to application overview",
    "pages": [],
    "lists": [],
    "conditions": [],
    "fees": [],
    "sections": [],
    "outputs": [
        {
            "name": "update-form",
            "title": "Update form in application store",
            "type": "savePerPage",
            "outputConfiguration": {
                "savePerPageUrl": (
                    "https://webhook.site/af39d1c4-d002-4607-9154-3c4abcbd68cc"
                )
            },
        }
    ],
    "skipSummary": False,
    "name": f"Generated by script {datetime.datetime.now()}",
}

BASIC_PAGE_STRUCTURE = {
    "path": None,
    "title": None,
    "components": [],
    "next": [],
    # "controller": None,
    "options": {},
}

SUMMARY_PAGE = SUB_PAGES_TO_REUSE["/summary"]


def build_conditions(component_name, component: dict) -> dict:
    results = []
    for condition in component["conditions"]:
        result = {
            "displayName": condition["name"],
            "name": condition["name"],
            "value": {
                "name": condition["name"],
                "conditions": [
                    {
                        "field": {
                            "name": component_name,
                            "type": component["type"],
                            "display": component["title"],
                        },
                        "operator": condition["operator"],
                        "value": {
                            "type": "Value",
                            "value": condition["value"],
                            "display": condition["value"],
                        },
                    }
                ],
            },
        }
        results.append(result)

    return results


def build_page(input_page_name: str) -> dict:
    input_page = PAGES_TO_REUSE[input_page_name]
    page = copy.deepcopy(BASIC_PAGE_STRUCTURE)
    page.update(
        {
            "path": f"/{input_page_name}",
            "title": LOOKUPS.get(input_page_name, input_page_name),
        }
    )
    # Having a 'null' controller element breaks the form-json, needs to not be there if blank
    if controller := input_page.get("controller", None):
        page["controller"] = controller
    for component_name in input_page["component_names"]:
        component = copy.deepcopy(COMPONENTS_TO_REUSE[component_name])
        component["name"] = component_name
        conditions = component.get("conditions", None)
        if conditions:
            component.pop("conditions")

        page["components"].append(component)

    return page


def build_navigation(results: dict, input_pages: list[str]) -> dict:
    for i in range(0, len(input_pages)):
        if i < len(input_pages) - 1:
            next_path = input_pages[i + 1]
        elif i == len(input_pages) - 1:
            next_path = "summary"
        else:
            next_path = None

        this_path = input_pages[i]
        this_page_in_results = next(
            p for p in results["pages"] if p["path"] == f"/{this_path}"
        )

        conditions_include_direct_next = False
        for c_name in PAGES_TO_REUSE[this_path]["component_names"]:
            component = COMPONENTS_TO_REUSE[c_name]
            if "conditions" in component:

                form_json_conditions = build_conditions(c_name, component)
                results["conditions"].extend(form_json_conditions)
                for condition in component["conditions"]:
                    if condition["destination_page"] == "CONTINUE":
                        conditions_include_direct_next = True
                        destination_path = f"/{next_path}"
                    else:
                        destination_path = condition["destination_page"]

                    # Check if we need to add this in from SUBPAGES_TO_REUSE
                    if destination_path not in [
                        page["path"] for page in results["pages"]
                    ]:
                        sub_page = copy.deepcopy(
                            SUB_PAGES_TO_REUSE[destination_path]
                        )
                        if not sub_page.get("next", None):
                            sub_page["next"] = [{"path": f"/{next_path}"}]

                        results["pages"].append(sub_page)

                    this_page_in_results["next"].append(
                        {
                            "path": destination_path,
                            "condition": condition["name"],
                        }
                    )

        # If there were no conditions and we just continue to the next page
        if not conditions_include_direct_next:
            this_page_in_results["next"].append({"path": f"/{next_path}"})

    return results


def build_form_json(input_json: dict) -> dict:

    results = copy.deepcopy(BASIC_FORM_STRUCTURE)

    start_page = copy.deepcopy(BASIC_PAGE_STRUCTURE)
    start_page.update(
        {
            "title": LOOKUPS[input_json["title"]],
            "path": f"/intro-{input_json['title']}",
            "controller": "./pages/start.js",
            "next": [{"path": f"/{input_json['pages'][0]}"}],
        }
    )

    results["pages"].append(start_page)
    results["startPage"] = start_page["path"]

    for page in input_json["pages"]:
        results["pages"].append(build_page(page))

    results = build_navigation(results, input_json["pages"])

    results["pages"].append(SUMMARY_PAGE)

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
    default="org-info_basic_name_address.json",
    help="Input configuration",
    prompt=True,
)
@click.option(
    "--output_folder",
    default="../digital-form-builder/runner/dist/server/forms/",
    help="Output destination",
    prompt=True,
)
@click.option(
    "--output_file",
    default="single_name_address.json",
    help="Output destination",
    prompt=True,
)
def generate_form_json(input_folder, input_file, output_folder, output_file):
    with open(os.path.join(input_folder, input_file), "r") as f:
        input_data = json.load(f)

    form_json = build_form_json(input_data)

    with open(os.path.join(output_folder, output_file), "w") as f:
        json.dump(form_json, f)


if __name__ == "__main__":
    generate_form_json()
