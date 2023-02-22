from enum import Enum
from flask_babel import gettext
from flask import current_app

def get_translation(value: str):

    statuses = {    
    "NOT_STARTED": gettext("Not Started"),
    "IN_PROGRESS": gettext("In Progress"),
    "COMPLETED": gettext("Assessment complete"),
    "QA_COMPLETED": gettext("QA complete"),
    "FLAGGED": gettext("Flagged"),
    "STOPPED": gettext("Stopped"),
}
    return statuses.get(value, value.replace("_", " ").strip().title())