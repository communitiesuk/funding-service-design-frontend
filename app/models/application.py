import inspect
from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.models.application_parts.form import Form
from flask import current_app


@dataclass
class Application:
    id: str
    reference: str
    account_id: str
    status: str
    fund_id: str
    round_id: str
    project_name: str
    date_submitted: datetime
    started_at: datetime
    last_edited: datetime
    language: str
    forms: List[Form]

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

    def match_forms_to_state(self, display_config):
        current_app.logger.info(
            "Sorting forms into order using section config associated with"
            f"fund: {self.fund_id}, round: {self.round_id}"
            f", for application id:{self.id}."
        )
        sections_config = [
            {
                "section_title": section.title,
                "section_weighting": section.weighting,
                "forms": [
                    {
                        "form_name": form.form_name,
                        "state": None,
                        "form_title": form.title,
                    }
                    for form in section.children
                ],
            }
            for section in display_config
        ]

        # fill the section/forms with form state from the application
        for form_state in self.forms:
            # find matching form in sections
            for section_config in sections_config:
                for form_in_config in section_config["forms"]:
                    if form_in_config["form_name"] == form_state["name"]:
                        form_in_config["state"] = form_state

        return sections_config
