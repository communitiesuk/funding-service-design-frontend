from flask import redirect
from flask import render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange


def minimium_money_question_page(min_amount: int, success_url: str):
    class criterionForm(FlaskForm):

        money_field = IntegerField(
            label="project_money_amount",
            validators=[DataRequired(), NumberRange(min_amount)],
        )

    def criterion_page():

        form = criterionForm()
        if form.money_field.data is not None and not form.validate_on_submit():
            return render_template(
                "not_eligible.html",
                message=f"You must be applying for at least £{min_amount}.",
            )
        if form.validate_on_submit():
            return redirect(success_url)
        return render_template("min_funding_amount.html", form=form)

    return criterion_page()
