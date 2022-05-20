import inspect
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ApplicationSummary:
    id: str
    status: str
    round_id: str
    date_submitted: datetime
    assessment_deadline: datetime
    fund_id: str

    def __post_init__(self):
        self.date_submitted = datetime.fromisoformat(self.date_submitted)
        self.assessment_deadline = datetime.fromisoformat(
            self.assessment_deadline
        )

    @classmethod
    def from_dict(cls, env):
        # Filter unknown fields from JSON dictionary
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })
