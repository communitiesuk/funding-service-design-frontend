import json
import os

from flask import url_for

from ..config import FORMS_SERVICE_JSONS_PATH

APPLICATION_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
)


class Field(object):
    """A class to hold field definitions and values"""

    def __init__(
        self,
        name: str = "name",
        field_type: str = "text",
        label: str = "What's your name?",
        placeholder_text: str = "eg. John Smith",
        help_text: str = "Please enter your full name",
        hint: str = "Do you need a hint?",
        required: str = None,
        classes: str = "",
        choices: [] = None,
        choices_type: str = "string",
    ):
        self.name = name
        self.field_type = field_type
        self.label = label
        self.placeholder_text = placeholder_text
        self.help_text = help_text
        self.hint = hint
        self.required = required
        self.classes = classes
        self.choices = choices
        self.choices_type = choices_type


class Section(object):
    """A class to hold form sections"""

    def __init__(
        self,
        name: str,
        title: str,
        start_path: str,
    ):
        self.name = name
        self.title = title
        self.start_path = start_path


class Step(object):
    """A class to hold form steps"""

    def __init__(
        self,
        path: str,
        title: str,
        next: str,
        submit_text: str,
        fields: [] = None,
        section: Section = None,
    ):
        self.path = path
        self.title = title
        self.next = next
        self.submit_text = submit_text
        self.fields = fields
        self.section = section

    def add_field(self, field: Field):
        if not self.fields:
            self.fields = []
        self.fields.append(field)

    def add_field_from_json(self, field_json: dict):
        field = Field(
            name=field_json["name"],
            field_type=field_json["field_type"],
            label=field_json["label"],
            placeholder_text=field_json["placeholder_text"],
            help_text=field_json["help_text"],
            hint=field_json["hint"],
            required=field_json["required"],
        )
        self.add_field(field)

    def get_xgov_classes(self, field_type: str):
        classes = ""
        if field_type in ["TextField", "EmailAddressField", "WebsiteField"]:
            classes += " govuk-input--width-20"
        if field_type in ["YesNoField"]:
            classes += " govuk-radios--inline"
        if field_type in ["TelephoneNumberField"]:
            classes += " govuk-input--width-10"
        return classes

    def get_xgov_form_list(self, key: str, form_json: dict):
        list_dict = [
            json_list
            for json_list in form_json["lists"]
            if json_list["name"] == key
        ]
        items_type = list_dict[0]["type"]
        items_list = list_dict[0]["items"]
        return items_type, items_list

    def add_field_from_xgov_json(self, component_json: dict, form_json: dict):
        field_xgov_json_mapping = {
            "name": "name",
            "field_type": "type",
            "label": "title",
            "placeholder_text": "placeholder_text",
            "help_text": "help_text",
            "hint": "hint",
            "required": None,
            "classes": None,
            "choices_type": None,
            "choices_list": None,
        }
        params = {}
        for key, xgov_key in field_xgov_json_mapping.items():
            params.update({key: ""})
            if xgov_key and xgov_key in component_json:
                params.update({key: component_json[xgov_key]})

        params["required"] = component_json["title"] + " is required"
        if "options" in component_json:
            if "required" in component_json["options"]:
                if not component_json["options"]["required"]:
                    params["required"] = None
        if "list" in component_json:
            choices_type, choices_list = self.get_xgov_form_list(
                component_json["list"], form_json
            )
            params["choices_type"] = choices_type
            params["choices_list"] = choices_list

        params["classes"] = self.get_xgov_classes(params["field_type"])

        field = Field(
            name=params["name"],
            field_type=params["field_type"],
            label=params["label"],
            placeholder_text=params["placeholder_text"],
            help_text=params["help_text"],
            hint=params["hint"],
            required=params["required"],
            classes=params["classes"],
            choices=params["choices_list"],
            choices_type=params["choices_type"],
        )
        self.add_field(field)


class Formzy(object):
    """A class to hold dynamic
    form attributes, steps and fields"""

    def __init__(
        self,
        name: str = "example",
        title: str = "Example Form",
        description: str = "An example form",
        steps: {} = None,
        sections: {} = None,
    ):
        self.name = name
        self.title = title
        self.description = description
        self.current_step_index = 0
        self.steps = steps
        self.sections = sections

    @property
    def next_url(self):
        url = url_for(
            "formzy_step", form_name=self.name, step=self.current_step.next[1:]
        )
        return url

    def add_step(self, step: Step):
        if not self.steps:
            self.steps = {}
        self.steps.update({step.path: step})

    def get_xgov_form_section(self, key: str, form_json: dict):
        section_dict = [
            json_section
            for json_section in form_json["sections"]
            if json_section["name"] == key
        ]
        return section_dict[0]

    def add_section(self, section: Section):
        if not self.sections:
            self.sections = {}
        if section.name not in self.sections:
            self.sections.update({section.name: section})

    def add_step_from_json(self, step_path: str, step_json: dict):
        step = Step(
            path=step_path,
            title=step_json["title"],
            next=step_json["next"],
            submit_text=step_json["submit_text"],
        )
        for field_json in step_json["fields"]:
            step.add_field_from_json(field_json)
        self.add_step(step)

    def add_section_from_xgov_json(self, page_json: dict, form_json: dict):
        section = None
        if "section" in page_json:
            section_json = self.get_xgov_form_section(
                page_json["section"], form_json
            )
            section = Section(
                name=section_json["name"],
                title=section_json["title"],
                start_path=page_json["path"],
            )
            self.add_section(section)
        return section

    def add_step_from_xgov_json(self, page_json: dict, form_json: dict):
        next = None
        if "next" in page_json and len(page_json["next"]) > 0:
            if "path" in page_json["next"][0]:
                next = page_json["next"][0]["path"]
        section = self.add_section_from_xgov_json(page_json, form_json)

        step = Step(
            path=page_json["path"],
            title=page_json["title"],
            next=next,
            submit_text="Next",
            section=section,
        )
        for component_json in page_json["components"]:
            step.add_field_from_xgov_json(component_json, form_json)
        self.add_step(step)

    @property
    def current_step(self):
        steps_as_list = [step for path, step in self.steps.items()]
        return steps_as_list[self.current_step_index]

    def get_step(self, step: str):
        return self.steps.get("/" + step)


def create_formzy_with_json(
    absolute_path: str = os.path.dirname(os.path.realpath(__file__))
    + "/forms.json",
):
    f = open(absolute_path)
    forms_json = json.load(f)
    formzy = Formzy(
        name=forms_json["name"],
        title=forms_json["title"],
        description=forms_json["description"],
    )
    for step_path, step_json in forms_json["steps"].items():
        formzy.add_step_from_json(step_path, step_json)
    f.close()

    return formzy


def get_json_forms(status: str = "public"):
    json_path = os.path.join(
        APPLICATION_ROOT, FORMS_SERVICE_JSONS_PATH, status
    )
    files = os.listdir(json_path)

    return files


def create_formzy_from_xgov_json(form_name: str, status: str = "public"):
    json_path = os.path.join(
        APPLICATION_ROOT, FORMS_SERVICE_JSONS_PATH, status, form_name + ".json"
    )
    f = open(json_path)
    forms_json = json.load(f)
    name = form_name
    title = form_name.replace("_", " ").replace("-", " ").title()
    description = "An Example Form"
    metadata = forms_json["metadata"]
    if "name" in metadata:
        name = metadata["name"]
    if "title" in metadata:
        description = metadata["title"]
    if "description" in metadata:
        description = metadata["description"]

    formzy = Formzy(
        name=name,
        title=title,
        description=description,
    )
    for page in forms_json["pages"]:
        formzy.add_step_from_xgov_json(page, forms_json)
    f.close()

    return formzy
