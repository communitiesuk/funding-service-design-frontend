import inspect
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from typing import List

from app.models.application_parts.form import Form
from app.models.application_parts.sections import COF_R2_SECTION_DISPLAY_CONFIG
from app.models.application_parts.sections import Sections
from flask import current_app


@dataclass
class Application:
    id: str
    account_id: str
    status: str
    fund_id: str
    round_id: str
    project_name: str
    date_submitted: datetime
    started_at: datetime
    last_edited: datetime
    forms: List[Form]
    sections: Sections = field(
        default_factory=lambda: COF_R2_SECTION_DISPLAY_CONFIG
    )

    @classmethod
    def get_form_data(cls, application_data, form_name):
        for form in application_data.forms:
            if form["name"] == form_name:
                return form

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

    def create_sections(self, application):
        current_app.logger.info(
            "filling application sections with form state associated with"
            f" application id:{application.id}."
        )
        for form in self.forms:
            form_name = form["name"]
            for (
                section,
                section_config,
            ) in self.sections.items():
                if form_name in section_config["forms_within_section"]:
                    section_config["forms_within_section"][form_name] = form
            # TODO post mvp
            # Update the section weighting using the FUND STORE weightings
            # i.e query the fund store HERE and load weightings into sections
            # get_round_data(fund_id=fund_id, round_id=round_id)
            # current_app.logger.info(
            #     f"Applying section weightings for
            #       fund_id: {application.fund_id},
            #       round_id: {application.round_id}"
            # )
