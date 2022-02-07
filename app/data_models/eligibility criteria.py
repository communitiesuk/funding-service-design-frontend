"""
This file defines the data model for eligibility criteria.
"""
from attr import define


@define
class eligibility_criteria:
    minimium_fund_amount: float
