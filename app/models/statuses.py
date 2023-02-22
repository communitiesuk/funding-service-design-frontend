from enum import Enum
from flask_babel import gettext
from flask import current_app
from app.filters import snake_case_to_human

def get_translation(value: str):

    statuses = {    
    "NOT_STARTED": gettext("Not Started"),
    "IN_PROGRESS": gettext("In Progress"),
    "COMPLETED": gettext("Assessment complete"),
    "QA_COMPLETED": gettext("QA complete"),
    "FLAGGED": gettext("Flagged"),
    "STOPPED": gettext("Stopped"),
}
    try:
        translated_value = statuses[value]
    except KeyError:
        current_app.logger.info(
        f"'{translated_value}' is not in statuses dictionary"
    )
        return snake_case_to_human(value)
  
    return translated_value