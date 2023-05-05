import inspect
from dataclasses import dataclass
from typing import List


@dataclass
class Form:
    title: str

    @staticmethod
    def from_dict(d: dict):
        return Form(
            **{
                k: v
                for k, v in d.items()
                if k in inspect.signature(Form).parameters
            }
        )


@dataclass
class ApplicationMapping:
    title: str
    weighting: int
    children: List[Form]

    @staticmethod
    def from_dict(d: dict):
        children_data = d.pop("children", [])
        children = [Form.from_dict(child) for child in children_data]
        return ApplicationMapping(
            **{
                k: v
                for k, v in d.items()
                if k in inspect.signature(ApplicationMapping).parameters
            },
            children=children,
        )
