import json
from pathlib import Path

files = Path("form_jsons/public").glob("*")


def check_form_json_files_for_duplicate_field_ids():
    forms_using_field_id = {}
    form_json_with_field_ids = []

    for file in files:
        form_name = file.name
        field_ids = []
        with open(file) as jsonFile:
            data = json.load(jsonFile)
            for page in data["pages"]:
                for component in page["components"]:
                    field_id = component["name"]
                    field_ids.append(field_id)

        form_json_with_field_ids.append(
            {"form_name": form_name, "field_ids": field_ids}
        )

    def add_duplicate_field_id(field_id, current_form_name):
        if field_id not in forms_using_field_id.keys():
            forms_using_field_id[field_id] = [current_form_name]
        elif current_form_name not in forms_using_field_id[field_id]:
            forms_using_field_id[field_id].append(current_form_name)
        else:
            pass

    def are_strings_are_unique(string_one, string_two):
        if string_one == string_two:
            return False
        else:
            return True

    def check_field_id_is_unique(field_id):
        # loop through all forms to check where this field id is used
        for form in form_json_with_field_ids:
            for current_field_id in form["field_ids"]:
                is_unique_field_id = are_strings_are_unique(
                    field_id, current_field_id
                )
                if is_unique_field_id is False:
                    add_duplicate_field_id(field_id, form["form_name"])

    for form_json in form_json_with_field_ids:
        for field_id in form_json["field_ids"]:
            check_field_id_is_unique(field_id)

    duplicates = []
    for field_id, forms in forms_using_field_id.items():
        # if the field_id is in more than one form
        if len(forms) > 1:
            duplicates.append(
                f'Duplicated field_id: "{field_id}" in multiple forms:'
                f' {", ".join(forms)}.'
            )
    return duplicates


def test_check_form_json_for_duplicate_field_ids():
    field_id_duplicates = check_form_json_files_for_duplicate_field_ids()
    number_of_duplicated_field_ids = len(field_id_duplicates)
    assert number_of_duplicated_field_ids == 0, "\n".join(field_id_duplicates)
