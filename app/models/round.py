import inspect
from dataclasses import dataclass


@dataclass
class Round:
    id: str
    name: str
    description: str
    assessment_criteria_weighting: list
    assessment_deadline: str
    deadline: str
    fund_id: str
    opens: str
    title: str

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
