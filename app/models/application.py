import inspect
from dataclasses import dataclass
from datetime import datetime
from typing import List

from app.models.application_parts.section import Section


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
    sections: List[Section]

    @classmethod
    def get_section_data(cls, application_data, section_name):
        sections_belonging_to_application = application_data.sections
        for section in sections_belonging_to_application:
            if section["section_name"] == section_name:
                return section

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

    # TO DO: ENFORCE TYPES
    # def __post_init__(self):
    #     for (name, field_type) in self.__annotations__.items():
    #         if not isinstance(self.__dict__[name], field_type):
    #             current_type = type(self.__dict__[name])
    #             raise TypeError(f"The field `{name}` was assigned by
    #               `{current_type}` instead of `{field_type}`")
    #     print("Check is passed successfully")
