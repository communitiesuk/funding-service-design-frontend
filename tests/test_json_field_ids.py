import json
from pathlib import Path

files = Path("form_jsons/public").glob("*")
forms_using_field_id = {}
form_json_with_field_ids = []


def add_duplicate_field_id(field_id, current_form_name):
    if field_id not in forms_using_field_id.keys():
        forms_using_field_id[field_id] = [current_form_name]
    # if the duplication in a form is already recorded, do not add again
    elif current_form_name not in forms_using_field_id[field_id]:
        forms_using_field_id[field_id].append(current_form_name)
    else:
        pass


def are_strings_are_unique(string_one, string_two):
    if string_one == string_two:
        return False
    else:
        return True


def check_field_id_is_unique(field_id, forms_to_check):
    # loop through all forms to check where this field id is used
    for form in forms_to_check:
        for current_field_id in form["field_ids"]:
            is_unique_field_id = are_strings_are_unique(
                field_id, current_field_id
            )
            if is_unique_field_id is False:
                add_duplicate_field_id(field_id, form["form_name"])


def check_for_duplicate_field_ids_across_form_jsons():
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
    for form_json in form_json_with_field_ids:
        # get other forms to check against
        import copy

        forms_to_check = copy.deepcopy(form_json_with_field_ids)
        for i in range(len(forms_to_check)):
            if forms_to_check[i]["form_name"] == form_json["form_name"]:
                del forms_to_check[i]
                break
        for field_id in form_json["field_ids"]:
            check_field_id_is_unique(field_id, forms_to_check)

    duplicates = []
    for field_id, forms in forms_using_field_id.items():
        # if the field_id is in another form
        if len(forms) > 0:
            duplicates.append(
                f'Duplicated field_id: "{field_id}" in multiple forms:'
                f' {", ".join(forms)}.'
            )
    return duplicates


def test_check_form_json_for_duplicate_field_ids():
    field_id_duplicates_across_forms = (
        check_for_duplicate_field_ids_across_form_jsons()
    )
    # Could add check here for duplicates within the same form_json file,
    # the form builder does not currently allow this field_id duplication
    # witin the same file, so a check is not required.
    number_of_duplicated_field_ids = len(field_id_duplicates_across_forms)
    assert number_of_duplicated_field_ids == 0, "\n".join(
        field_id_duplicates_across_forms
    )
