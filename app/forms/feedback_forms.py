from flask_wtf import FlaskForm
from wtforms import HiddenField
from wtforms import IntegerField
from wtforms import RadioField
from wtforms import TextAreaField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired


# Always has an application_id, as it's required by @verify_application_owner_local on POST requests.
class ApplicationFlaskForm(FlaskForm):
    application_id = HiddenField()


class DefaultSectionFeedbackForm(ApplicationFlaskForm):
    experience = RadioField(
        "How easy did you find it to complete this section?",
        choices=[
            ("very easy", "Very easy"),
            ("easy", "Easy"),
            ("neither easy or difficult", "Neither easy nor difficult"),
            ("difficult", "Difficult"),
            ("very difficult", "Very difficult"),
        ],
        validators=[InputRequired(message="Select a score")],
    )
    more_detail = TextAreaField("Explain why you chose this score (optional)")

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
        "How was your overall application experience?",
        choices=[
            ("very good", "Very good"),
            ("good", "Good"),
            ("average", "Average"),
            ("poor", "Poor"),
            ("very poor", "Very poor"),
        ],
        validators=[InputRequired(message="Select a score")],
    )
    more_detail = TextAreaField("Explain why you chose this score (optional)")


class EndOfApplicationPage2Form(EndOfApplicationPageForm):
    demonstrate_why_org_funding = RadioField(
        "To what extent do you agree that this application form allowed you to"
        " demonstrate why your organisation should receive funding?",
        choices=[
            ("strongly agree", "Strongly agree"),
            ("agree", "Agree"),
            ("neither agree nor disagree", "Neither agree nor disagree"),
            ("disagree", "Disagree"),
            ("strongly disagree", "Strongly disagree"),
        ],
        validators=[InputRequired(message="Select a score")],
    )


class EndOfApplicationPage3Form(EndOfApplicationPageForm):
    understand_eligibility_criteria = RadioField(
        "How easy was it to understand the eligibility criteria for this"
        " fund?",
        choices=[
            ("very easy", "Very easy"),
            ("easy", "Easy"),
            ("neither easy or difficult", "Neither easy nor difficult"),
            ("difficult", "Difficult"),
            ("very difficult", "Very difficult"),
        ],
        validators=[DataRequired(message="Select a score")],
    )


class EndOfApplicationPage4Form(EndOfApplicationPageForm):
    hours_spent = IntegerField(
        "Number of hours spent:",
        validators=[DataRequired(message="Enter number of hours")],
    )


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
