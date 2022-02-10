from app.data_models.eligibility_criteria import eligibility_criterion
from flask import redirect
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange


def form_page_from_criterion(criterion: eligibility_criterion):
    class criterionForm(FlaskForm):

        criterion_field = Field(
            label=criterion.input_name,
            validators=[DataRequired(), criterion.eligibility_validator],
        )

    def criterion_page():

        form = criterionForm()
        input_arg_dict = {
            "label": {"text": criterion.eligibility_question},
            "id": form.criterion_field.id,
            "name": form.criterion_field.id,
        } | criterion.eligibility_component_options
        if form.validate_on_submit():
            return redirect("/")
        return render_template(
            "funding_amount.html", input_dict=input_arg_dict
        )

    return criterion_page()


def must_be_atleast_criterion(min_amount):
    return eligibility_criterion(
        input_name="amount_needed",
        eligibility_component="govukInput",
        eligibility_question="How much money do you need?",
        eligibility_validator=NumberRange(min_amount),
        failed_eligibility_reason=(
            f"You must be applying for atleast £{min_amount}"
        ),
        eligibility_component_options={
            "label": {"text": "Enter your answer using numbers only"},
            "prefix": {"text": "£"},
            "classes": "govuk-input--width-20",
        },
    )
