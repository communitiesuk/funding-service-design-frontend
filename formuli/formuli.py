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
        fields: [] = None,
        *args,
        **kwargs
    ):
        super(Formuli, self).__init__(*args, **kwargs)
        self.name = name
        self.title = title
        self.description = description
        self.current_input_index = 0
        if fields:
            self.fields = fields
        else:
            self.fields = [Field()]

    def add_field(self, field: Field):
        self.fields.append(field)

    @property
    def current_field(self):
        return self.fields[self.current_input_index]
