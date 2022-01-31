import json
import os

from flask import url_for

from ..config import APPLICATION_ROOT
from ..config import FORMS_SERVICE_JSONS_PATH


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
    ):
        self.name = name
        self.field_type = field_type
        self.label = label
        self.placeholder_text = placeholder_text
        self.help_text = help_text
        self.hint = hint
        self.required = required
        self.classes = classes


class Step(object):
    """A class to hold form steps"""

    def __init__(
        self,
        path: str,
        title: str,
        next: str,
        submit_text: str,
        fields: [] = None,
    ):
        self.path = path
        self.title = title
        self.next = next
        self.submit_text = submit_text
        self.fields = fields

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
        elif field_type in ["TelephoneNumberField"]:
            classes += " govuk-input--width-10"
        return classes

    def add_field_from_xgov_json(self, component_json: dict):
        name = field_type = label = placeholder_text = help_text = hint = ""
        # required = "" # All fields required for now
        keys = [
            "name",
            "type",
            "title",
            "hint",
        ]
        params = {}
        for key in keys:
            if key in component_json:
                params.update({key: component_json[key]})

        if "name" in params:
            name = params["name"]
        if "type" in params:
            field_type = params["type"]
        if "title" in params:
            label = params["title"]
        if "placeholder" in params:
            placeholder_text = params["placeholder_text"]
        if "help_text" in params:
            help_text = params["help_text"]
        if "hint" in params:
            hint = params["hint"]
        # if "required" in params:
        #     required = params["required"]

        classes = self.get_xgov_classes(field_type)

        field = Field(
            name=name,
            field_type=field_type,
            label=label,
            placeholder_text=placeholder_text,
            help_text=help_text,
            hint=hint,
            required="This is required",
            classes=classes,
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
    ):
        self.name = name
        self.title = title
        self.description = description
        self.current_step_index = 0
        self.steps = steps

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

    def add_step_from_xgov_json(self, page_json: dict):
        next = None
        if "next" in page_json and len(page_json["next"]) > 0:
            if "path" in page_json["next"][0]:
                next = page_json["next"][0]["path"]
        step = Step(
            path=page_json["path"],
            title=page_json["title"],
            next=next,
            submit_text="Next",
        )
        for component_json in page_json["components"]:
            step.add_field_from_xgov_json(component_json)
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


def create_formzy_from_json(form_name: str, status: str = "public"):
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
        formzy.add_step_from_xgov_json(page)
    f.close()

    return formzy
