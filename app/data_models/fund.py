"""
This file contains the data model for the funds.
"""
from app.data_models.eligibility_criteria import eligibility_criteria
from attr import define


@define
class fund:
    eligibility_data: eligibility_criteria
