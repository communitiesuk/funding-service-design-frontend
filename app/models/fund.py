from dataclasses import dataclass
import inspect


@dataclass
class Fund:
    id: str
    name: str
    description: str

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