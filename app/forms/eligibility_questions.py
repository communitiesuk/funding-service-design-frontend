from flask import render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import NumberRange


def minimium_money_question_page(max_amount: int, success_url: str):
    class MinimiumMoneyForm(FlaskForm):

        money_field = IntegerField(
            label="project_money_amount",
            validators=[DataRequired(), NumberRange(max=max_amount)],
        )

    def min_money_page():

        form = MinimiumMoneyForm()
        if form.money_field.data is not None and not form.validate_on_submit():
            return render_template(
                "not_eligible.html",
                message=(
                    f"You can apply for a maximium amount of £{max_amount}."
                ),
            )
        if form.validate_on_submit():
            return render_template(
                "eligible.html",
                service_url=success_url,
            )
        return render_template("min_funding_amount.html", form=form)

    return min_money_page()
