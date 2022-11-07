import inspect
from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.models.application_parts.form import Form
from config import Config
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

    @staticmethod
    def create_blank_sections(fund_id, round_id, language):
        sections = {}
        FORMS_CONFIG_FOR_FUND_ROUND = Config.FORMS_CONFIG_FOR_FUND_ROUND
        sections_config = FORMS_CONFIG_FOR_FUND_ROUND.get(
            ":".join([fund_id, round_id])
        )
        for section_config in sections_config:
            sections[section_config["section_title"][language]] = {}
            for form in section_config["ordered_form_names_within_section"]:
                sections[section_config["section_title"][language]][
                    form[language]
                ] = None
        return sections

    def get_sections(self, application):
        current_app.logger.info(
            "get ordered forms associated with"
            f" application id:{application.id}."
        )

        sections = self.create_blank_sections(
            application.fund_id, application.round_id, application.language
        )

        # def fill_sections_with_form_state
        for form_state in self.forms:
            for section_title, section_forms in sections.items():
                for section_form_name in section_forms:
                    if section_form_name == form_state["name"]:
                        section_forms[section_form_name] = form_state
                        # add form state to ordered_forms dict
        return sections
