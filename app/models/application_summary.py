import dataclasses
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
        self.assessment_deadline = datetime.fromisoformat(self.assessment_deadline)

    def __init__(self, **kwargs):
        # Ignore unknown fields for future compatability
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)

