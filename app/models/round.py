from __future__ import annotations

import inspect
from dataclasses import dataclass


@dataclass
class FeedbackSurveyConfig:
    requires_survey: bool = False
    isSurveyOptional: bool = True
    requires_section_feedback: bool = False


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
    mark_as_complete_enabled: bool = False
    feedback_survey_config: FeedbackSurveyConfig = None

    def __post_init__(self):
        if isinstance(self.feedback_survey_config, dict):
            self.feedback_survey_config = FeedbackSurveyConfig(
                **{
                    k: v
                    for k, v in self.feedback_survey_config.items()
                    if k in inspect.signature(FeedbackSurveyConfig).parameters
                }
            )
        elif self.feedback_survey_config is None:
            self.feedback_survey_config = FeedbackSurveyConfig()

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
