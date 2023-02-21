from enum import Enum
from fsd_utils.locale_selector.get_lang import get_lang

class Language(Enum):
    English = "Saesneg"
    Welsh = "Cymraeg"


def get_text(value: str): 
    lang = get_lang()
    if lang == "cy":       
        try:
            translated_value = Language[value].value
        except KeyError:            
            translated_value = value
    else:        
        translated_value = value
    return translated_value