import inspect
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ApplicationSummary:
    id: str
    status: str
    round_id: str
    fund_id: str
    started_at: datetime
    project_name: str
    last_edited: Optional[datetime] = None

    def __post_init__(self):
        self.started_at = datetime.fromisoformat(self.started_at)
        self.last_edited = (
            datetime.fromisoformat(self.last_edited)
            if self.last_edited
            else None
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
