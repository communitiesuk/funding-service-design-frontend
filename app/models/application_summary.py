import inspect
import langcodes
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from pytz import timezone


@dataclass
class ApplicationSummary:
    id: str
    reference: str
    status: str
    round_id: str
    fund_id: str
    started_at: datetime
    project_name: str
    language: str
    last_edited: Optional[datetime] = None

    def __post_init__(self):
        self.started_at = datetime.fromisoformat(self.started_at).astimezone(
            timezone("Europe/London")
        )
        self.last_edited = (
            datetime.fromisoformat(self.last_edited).astimezone(
                timezone("Europe/London")
            )
            if self.last_edited
            else None
        )
        self.language = langcodes.Language.make(self.language).language_name()

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
