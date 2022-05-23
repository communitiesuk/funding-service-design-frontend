import inspect
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ApplicationSummary:
    id: str
    status: str
    round_id: str
    fund_id: str
    started_at: datetime


    def __post_init__(self):
        self.started_at = datetime.fromisoformat(self.started_at)

    @classmethod
    def from_dict(cls, env):
        # Filter unknown fields from JSON dictionary
        return cls(**{
            k: v for k, v in env.items()
            if k in inspect.signature(cls).parameters
        })
