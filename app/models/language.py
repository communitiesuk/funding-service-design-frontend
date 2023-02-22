from flask_babel import gettext

def get_text(value: str):
    languages = {
        "en" : gettext("English"),
        "cy" : gettext("Welsh")
    }        
    try:
        translated_value = languages[value]
    except KeyError:            
        translated_value = value

    return translated_value