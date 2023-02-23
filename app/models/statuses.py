from flask_babel import gettext

def get_text(value: str):

    statuses = {    
    "NOT_STARTED": gettext("Not Started"),
    "IN_PROGRESS": gettext("In Progress"),
    "COMPLETED": gettext("Assessment complete"),
    "QA_COMPLETED": gettext("QA complete"),
    "FLAGGED": gettext("Flagged"),
    "STOPPED": gettext("Stopped"),
}
    return statuses.get(value, value.replace("_", " ").strip().title())