import inspect
from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.models.application_parts.form import Form
from config import Config


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

    @classmethod
    def get_form_data(cls, application_data, form_name):
        for form in application_data.forms:
            if form["form_name"] == form_name:
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

    def create_sections(self, fund_id, round_id):
        for form in self.forms:
            form_name = form["form_name"]
            # update the sections with the applications form state
            for (
                section,
                section_config,
            ) in Config.COF_R2_SECTION_CONFIG.items():
                if form_name in section_config["forms_within_section"]:
                    section_config["forms_within_section"][form_name] = form
            # TODO post mvp
            # Update the section weighting using the FUND STORE weightings
            # i.e query the fund store HERE and load weightings into sections
            # get_round_data(fund_id=fund_id, round_id=round_id)
        self.sections = Config.COF_R2_SECTION_CONFIG
