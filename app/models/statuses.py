from enum import Enum
from flask_babel import gettext
from flask import current_app

class Statues(Enum):
    NOT_STARTED = gettext("Not Started")
    IN_PROGRESS = gettext("In Progress")
    COMPLETED = gettext("Assessment complete")
    QA_COMPLETED = gettext("QA complete")
    FLAGGED = gettext("Flagged")
    STOPPED = gettext("Stopped")

def get_translation(value: str):
    current_app.logger.info(
        f"TRANSLATED VALUES PASSED IN :'{value}'"
    )
    translated_value = value
    try:
        translated_value = Statues[value].value
    except KeyError:            
        return translated_value
    current_app.logger.info(
        f"ACTUAL TRANSLATED VALUE RETURNED :'{translated_value}'"
    )
    return translated_value