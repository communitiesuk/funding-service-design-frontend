from flask import redirect
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange


def form_page_from_criterion(min_amount: int):
    class criterionForm(FlaskForm):

        criterion_field = Field(
            label="project_money_amount",
            validators=[DataRequired(), NumberRange(min_amount)],
        )

    def criterion_page():

        form = criterionForm()
        if form.validate_on_submit():
            return redirect("/")
        return render_template("min_funding_amount.html", form=form)

    return criterion_page()
