from flask import abort
from flask import redirect
from flask import render_template
from flask.views import MethodView
from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import RadioField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import URL

from .formzy import create_formzy_from_xgov_json


class FormzyStepView(MethodView):
    def __init__(self, *args, **kwargs):
        super(FormzyStepView, self).__init__(*args, **kwargs)
        self.formzy = None
        self.current_step = None

    def set_step(self, step: str):
        print(self.formzy.title)
        self.current_step = self.formzy.get_step(step)

    def set_field_attributes(self, form):
        for field in self.current_step.fields:
            d_field = getattr(form, field.name)
            for attr in [
                "label",
                "hint",
                "placeholder_text",
                "help_text",
                "field_type",
                "classes",
            ]:
                setattr(d_field, attr, getattr(field, attr))

            if hasattr(d_field, "choices"):
                choice_items = []
                if d_field.choices and len(d_field.choices) > 0:
                    choice_items = [
                        {"key": key, "text": text}
                        for key, text in d_field.choices
                    ]
                setattr(d_field, "choice_items", choice_items)

    def set_error_list(self, form):
        error_list = []
        for key, error in form.errors.items():
            error_list.append({"text": error[0], "href": "#" + key})
        setattr(form, "error_list", error_list)

    def form(self):
        class DynamicForm(FlaskForm):
            pass

        for f in self.current_step.fields:

            setattr(DynamicForm, f.name, self.get_field(f))

        d = DynamicForm()
        self.set_field_attributes(d)

        return d

    def get(self, form_name: str, step: str):
        formzy = create_formzy_from_xgov_json(form_name)
        if not formzy:
            abort(404)
        else:
            self.formzy = formzy
        self.set_step(step)
        form = self.form()

        return render_template(
            "step.html", formzy=self.formzy, step=self.current_step, form=form
        )

    def post(self, form_name: str, step: str):
        self.formzy = create_formzy_from_xgov_json(form_name)
        self.set_step(step)
        form = self.form()
        if form.validate_on_submit():
            print("Validated")
            return redirect(self.formzy.next_url)
        else:
            self.set_error_list(form)
            print("Invalid")

        return render_template(
            "step.html", formzy=self.formzy, step=self.current_step, form=form
        )

    def get_field(self, field):
        validators = []
        choices = []

        if field.field_type == "WebsiteField":
            validators.append(
                URL(
                    message=(
                        "Please enter a valid web address eg."
                        " https://www.yoursite.com"
                    )
                )
            )

        if field.field_type == "EmailAddressField":
            validators.append(
                Email(
                    message=(
                        "Please enter a valid email address eg."
                        " you@somedomain.com"
                    )
                )
            )

        if field.required:
            validators.append(DataRequired(field.required))

        if hasattr(field, "choices"):
            print(field.choices)
            for choice in field.choices:
                choices.append((choice["value"], choice["text"]))

        if field.field_type in [
            "text",
            "TextField",
            "EmailAddressField",
            "TelephoneNumberField",
            "WebsiteField",
        ]:
            f = StringField(field.label, validators=validators)
        elif field.field_type in ["YesNoField"]:
            f = RadioField(
                field.label,
                choices=(("yes", "Yes"), ("no", "No")),
                validators=validators,
            )
        elif field.field_type in ["RadiosField"]:
            f = RadioField(field.label, choices=choices, validators=validators)
        elif field.field_type in ["MultilineTextField"]:
            f = TextAreaField(field.label, validators=validators)
        elif field.field_type == "password":
            f = PasswordField(field.label)
        else:
            f = HiddenField(field.name)

        return f
