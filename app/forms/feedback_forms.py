from flask_babel import gettext
from flask_wtf import FlaskForm
from wtforms import FloatField
from wtforms import HiddenField
from wtforms import RadioField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import NumberRange


# Always has an application_id, as it's required by @verify_application_owner_local on POST requests.
class ApplicationFlaskForm(FlaskForm):
    application_id = HiddenField()


class DefaultSectionFeedbackForm(ApplicationFlaskForm):
    experience = RadioField(
        label="How easy did you find it to complete this section?",
        validators=[InputRequired(message=gettext("Select a score"))],
    )
    more_detail = TextAreaField(
        label="Explain why you chose this score (optional)"
    )

    def __init__(self, *args, **kwargs):
        super(DefaultSectionFeedbackForm, self).__init__(*args, **kwargs)
        self.experience.label.text = gettext(
            "How easy did you find it to complete this section?"
        )
        self.experience.choices = [
            ("very easy", gettext("Very easy")),
            ("easy", gettext("Easy")),
            (
                "neither easy or difficult",
                gettext("Neither easy nor difficult"),
            ),
            ("difficult", gettext("Difficult")),
            ("very difficult", gettext("Very difficult")),
        ]
        self.more_detail.label.text = gettext(
            "Explain why you chose this score (optional)"
        )

    @property
    def as_dict(self):
        return {
            "application_id": self.application_id.data,
            "experience": self.experience.data,
            "more_detail": self.more_detail.data,
        }


class EndOfApplicationPageForm(ApplicationFlaskForm):
    def back_fill_data(self, data: dict):
        for field_name, field in self._fields.items():
            if field_name != "application_id":
                field.data = data.get(field_name)

    def as_dict(self):
        return {
            field_name: field.data
            for field_name, field in self._fields.items()
            if field_name != "application_id"
        }


class EndOfApplicationPage1Form(EndOfApplicationPageForm):
    overall_application_experience = RadioField(
        label="How was your overall application experience?",
        validators=[InputRequired(message="Select a score")],
    )
    more_detail = TextAreaField(
        label="Explain why you chose this score (optional)"
    )

    def __init__(self, *args, **kwargs):
        super(EndOfApplicationPage1Form, self).__init__(*args, **kwargs)
        self.overall_application_experience.label.text = gettext(
            "How was your overall application experience?"
        )
        self.overall_application_experience.choices = [
            ("very good", gettext("Very good")),
            ("good", gettext("Good")),
            ("average", gettext("Average")),
            ("poor", gettext("Poor")),
            ("very poor", gettext("Very poor")),
        ]
        self.more_detail.label.text = gettext(
            "Explain why you chose this score (optional)"
        )


class EndOfApplicationPage2Form(EndOfApplicationPageForm):
    demonstrate_why_org_funding = RadioField(
        label=(
            "To what extent do you agree that this application form allowed"
            " you to demonstrate why your organization should receive funding?"
        ),
        validators=[InputRequired(message="Select a score")],
    )

    def __init__(self, *args, **kwargs):
        super(EndOfApplicationPage2Form, self).__init__(*args, **kwargs)
        self.demonstrate_why_org_funding.label.text = gettext(
            "To what extent do you agree that this application form allowed"
            " you to demonstrate why your organization should receive funding?"
        )
        self.demonstrate_why_org_funding.choices = [
            ("strongly agree", gettext("Strongly agree")),
            ("agree", gettext("Agree")),
            (
                "neither agree nor disagree",
                gettext("Neither agree nor disagree"),
            ),
            ("disagree", gettext("Disagree")),
            ("strongly disagree", gettext("Strongly disagree")),
        ]


class EndOfApplicationPage3Form(EndOfApplicationPageForm):
    understand_eligibility_criteria = RadioField(
        label=(
            "How easy was it to understand the eligibility criteria for this"
            " fund?"
        ),
        validators=[DataRequired(message="Select a score")],
    )

    def __init__(self, *args, **kwargs):
        super(EndOfApplicationPage3Form, self).__init__(*args, **kwargs)
        self.understand_eligibility_criteria.label.text = gettext(
            "How easy was it to understand the eligibility criteria for this"
            " fund?"
        )
        self.understand_eligibility_criteria.choices = [
            ("very easy", gettext("Very easy")),
            ("easy", gettext("Easy")),
            (
                "neither easy or difficult",
                gettext("Neither easy nor difficult"),
            ),
            ("difficult", gettext("Difficult")),
            ("very difficult", gettext("Very difficult")),
        ]


class EndOfApplicationPage4Form(EndOfApplicationPageForm):
    hours_spent = FloatField(
        label="Number of hours spent:",
        validators=[
            DataRequired(
                message=(
                    "Enter a number only. The number must be at least 0.5 or"
                    " greater."
                )
            ),
            NumberRange(min=0.5),
        ],
    )

    def __init__(self, *args, **kwargs):
        super(EndOfApplicationPage4Form, self).__init__(*args, **kwargs)
        self.hours_spent.label.text = gettext("Number of hours spent:")


END_OF_APPLICATION_FEEDBACK_SURVEY_PAGE_NUMBER_MAP = {
    "1": (
        EndOfApplicationPage1Form,
        "end_of_application_feedback_page_1.html",
    ),
    "2": (
        EndOfApplicationPage2Form,
        "end_of_application_feedback_page_2.html",
    ),
    "3": (
        EndOfApplicationPage3Form,
        "end_of_application_feedback_page_3.html",
    ),
    "4": (
        EndOfApplicationPage4Form,
        "end_of_application_feedback_page_4.html",
    ),
}
