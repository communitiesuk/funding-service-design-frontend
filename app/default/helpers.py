import requests
from app.config import FORMS_SERVICE_PUBLIC_HOST


def get_token_to_return_to_application(
    form_name: str, formatted_application_payload
):
    res = requests.post(
        f"{FORMS_SERVICE_PUBLIC_HOST}/session/{form_name}",
        json=formatted_application_payload,
    )
    dictFromServer = res.json()
    print(dictFromServer)
    if res.status_code == 201:
        token_json = res.json()
        return token_json["token"]
    else:
        return None
