from enum import Enum
from fsd_utils.locale_selector.get_lang import get_lang

class Statues(Enum):
    NOT_STARTED = "Not Started Welsh"
    IN_PROGRESS = "In Progress Welsh"
    COMPLETED = "Assessment complete Welsh"
    QA_COMPLETED = "QA complete Welsh"
    FLAGGED = "Flagged Welsh"
    STOPPED = "Stopped Welsh"

def get_translation(value: str): 
    lang = get_lang()
    if lang == "cy":       
        try:
            translated_value = Statues[value].value
        except KeyError:            
            translated_value = value
    else:        
        translated_value = value.replace("_", " ").strip().title()
    return translated_value