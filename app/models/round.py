from __future__ import annotations

import inspect
from dataclasses import dataclass


@dataclass
class FeedbackSurveyConfig:
    requires_survey: bool = False
    isSurveyOptional: bool = True


@dataclass
class Round:
    id: str
    assessment_deadline: str
    deadline: str
    fund_id: str
    opens: str
    title: str
    short_name: str
    prospectus: str
    privacy_notice: str
    instructions: str
    contact_email: str
    contact_phone: str
    contact_textphone: str
    support_days: str
    support_times: str
    feedback_link: str
    project_name_field_id: str
    application_guidance: str
    feedback_survey_config: FeedbackSurveyConfig = (FeedbackSurveyConfig(),)
    mark_as_complete_enabled: bool = False

    def __post_init__(self):
        self.feedback_survey_config = (
            FeedbackSurveyConfig(
                requires_survey=self.feedback_survey_config["requires_survey"],
                isSurveyOptional=self.feedback_survey_config[
                    "isSurveyOptional"
                ],
            )
            if isinstance(self.feedback_survey_config, dict)
            else self.feedback_survey_config
        )

    @classmethod
    def from_dict(cls, d: dict):
        # Filter unknown fields from JSON dictionary
        return cls(
            **{
                k: v
                for k, v in d.items()
                if k in inspect.signature(cls).parameters
            }
        )
