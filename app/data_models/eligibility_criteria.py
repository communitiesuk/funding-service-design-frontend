"""
This file defines the data model for eligibility criteria.
"""
from typing import Callable

from attr import define


@define
class eligibility_criterion:
    input_name: str
    eligibility_component: str
    eligibility_question: str
    eligibility_validator: Callable
    failed_eligibility_reason: str
    eligibility_component_options: str = ""
