from typing import TypedDict


from typing_extensions import TypedDict
from datetime import datetime

class ApplicationSummary(TypedDict):
    id: str
    status: str
    round_id: str
    date_submitted: datetime
    assessment_deadline: datetime