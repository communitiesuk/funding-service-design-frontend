from flask import redirect
from flask import render_template
from flask.views import MethodView
from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import DataRequired

from .formzy import create_formzy_from_json


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

    def form(self):
        class DynamicForm(FlaskForm):
            pass

        for f in self.current_step.fields:
            print(f.name)

            setattr(DynamicForm, f.name, self.get_field(f))

        d = DynamicForm()
        self.set_field_attributes(d)

        return d

    def get(self, form_name: str, step: str):
        self.formzy = create_formzy_from_json(form_name)
        self.set_step(step)
        form = self.form()

        return render_template(
            "step.html", formzy=self.formzy, step=self.current_step, form=form
        )

    def post(self, form_name: str, step: str):
        self.formzy = create_formzy_from_json(form_name)
        self.set_step(step)
        form = self.form()
        if form.validate_on_submit():
            print("Validated")
            return redirect(self.formzy.next_url)
        else:
            print("Invalid")

        return render_template(
            "step.html", formzy=self.formzy, step=self.current_step, form=form
        )

    def get_field(self, field):
        f = HiddenField(field.name)
        validators = []
        if field.required:
            validators.append(DataRequired(field.required))

        if field.field_type in [
            "text",
            "TextField",
            "EmailAddressField",
            "TelephoneNumberField",
            "WebsiteField",
        ]:
            f = StringField(field.label, validators=validators)
        if field.field_type in ["MultilineTextField"]:
            f = TextAreaField(field.label, validators=validators)
        if field.field_type == "password":
            f = PasswordField(field.label)

        return f
