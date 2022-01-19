import json
import os
from dataclasses import dataclass

from flask_wtf import FlaskForm
from wtforms import BooleanField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


@dataclass
class Field:
    name: str = "name"
    type: str = "text"
    label: str = "What's your name?"
    placeholder_text: str = "eg. John Smith"
    help_text: str = "Please enter your full name"
    hint: str = "Do you need a hint?"
    is_heading: bool = True
    required: bool = True
    submit_text: str = "next"


class Formuli(FlaskForm):
    """A class to extend a WTForms FlaskForm with dynamic
    Formuli form attributes and fields"""

    def __init__(
        self,
        name: str = "example",
        title: str = "Example Form",
        description: str = "An example form",
        fields: [] = [],
        *args,
        **kwargs
    ):
        super(Formuli, self).__init__(*args, **kwargs)
        self.name = name
        self.title = title
        self.description = description
        self.current_input_index = 0
        self.fields = fields

    def add_field(self, field: Field):
        self.fields.append(field)

    @property
    def current_field(self):
        return self.fields[self.current_input_index]


def create_form_with_json():
    f = open(os.path.dirname(os.path.realpath(__file__)) + "/forms.json")
    forms_json = json.load(f)

    formuli = Formuli(
        name=forms_json["name"],
        title=forms_json["title"],
        description=forms_json["description"],
    )
    for field_json in forms_json["fields"]:
        field = Field(
            name=field_json["name"],
            type=field_json["type"],
            label=field_json["label"],
            placeholder_text=field_json["placeholder_text"],
            help_text=field_json["help_text"],
            hint=field_json["hint"],
            is_heading=field_json["is_heading"],
            required=field_json["required"],
            submit_text=field_json["submit_text"],
        )
        formuli.add_field(field)
    f.close()

    return formuli
