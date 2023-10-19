COMPONENTS_TO_REUSE = {
    "reuse-organisation-name": {
        "options": {"hideTitle": True, "classes": "govuk-!-width-full"},
        "type": "TextField",
        "title": "Organisation name",
        "hint": "This must match your registered legal organisation name",
        "schema": {},
    },
    "reuse-organisation-address": {
        "options": {},
        "type": "UkAddressField",
        "title": "Organisation address",
    },
    "reuse-organisation-main-purpose": {
        "options": {"hideTitle": True, "maxWords": "500"},
        "type": "FreeTextField",
        "title": "What is your organisation's main purpose?",
        "hint": "This is what the organisation was set up to achieve.",
    },
    "reuse_organisation_other_names_yes_no": {
        "options": {},
        "type": "YesNoField",
        "title": "Does your organisation use any other names?",
        "schema": {},
        "conditions": [
            {
                "name": "organisation_other_names_no",
                "value": "false",
                "operator": "is",
                "destination_page": "CONTINUE",
            },
            {
                "name": "organisation_other_names_yes",
                "value": "true",
                "operator": "is",
                "destination_page": "/alternative-organisation-name",
            },
        ],
    },
    "reuse-organisation-website-social-media-links": {
        "options": {"columnTitles": ["Link", "Action"]},
        "type": "MultiInputField",
        "title": "Website and social media",
        "schema": {},
        "children": [
            {
                "name": "reuse-web-link",
                "options": {"classes": "govuk-!-width-full"},
                "type": "WebsiteField",
                "title": "Link",
                "hint": (
                    "<p>For example, your company's Facebook, Instagram or"
                    " Twitter accounts (if applicable)</p><p>You can add more"
                    " links on the next step</p>"
                ),
                "schema": {},
            }
        ],
    },
}
