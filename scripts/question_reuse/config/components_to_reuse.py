COMPONENTS_TO_REUSE = {
    "reuse-organisation-name": {
        "options": {"hideTitle": False, "classes": "govuk-!-width-full"},
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
    "reuse-english-region": {
        "options": {"classes": "govuk-!-width-full"},
        "type": "TextField",
        "title": "Which region of England do you work in?",
    },
    "reuse-charitable-objects": {
        "options": {"hideTitle": True, "maxWords": "500"},
        "type": "FreeTextField",
        "title": "What are your organisation’s charitable objects?",
        "hint": "You can find this in your organisation's governing document.",
    },
    "ns-membership-organisations": {
        "options": {"hideTitle": True},
        "type": "RadiosField",
        "title": "Which membership organisations are you a member of?",
        "list": "list_ns_membership_organisations",
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
    "reuse-annual-turnover-23": {
        "options": {
            "prefix": "£",
            "hideTitle": True,
            "classes": "govuk-input--width-10",
        },
        "type": "NumberField",
        "title": "Annual turnover for 1 April 2022 to 31 March 2023",
        "hint": (
            '<label class="govuk-body" for="YauUjZ">1 April 2022 to 31 March'
            " 2023</label>"
        ),
    },
    "reuse-annual-turnover-22": {
        "options": {
            "prefix": "£",
            "hideTitle": True,
            "classes": "govuk-input--width-10",
        },
        "type": "NumberField",
        "hint": (
            '<label class="govuk-body" for="zuCRBk">1 April 2021 to 31 March'
            " 2022</label>"
        ),
        "title": "Annual turnover for 1 April 2021 to 31 March 2022",
    },
    "reuse-lead-contact-name": {
        "options": {"classes": "govuk-!-width-full"},
        "type": "TextField",
        "title": "Name of lead contact",
        "hint": (
            "They will receive all the information about this application."
        ),
    },
    "reuse-lead-contact-job-title": {
        "options": {"classes": "govuk-!-width-full"},
        "type": "TextField",
        "title": "Lead contact job title",
    },
    "reuse-lead-contact-email": {
        "options": {"classes": "govuk-!-width-full"},
        "type": "EmailAddressField",
        "title": "Lead contact email address",
    },
    "reuse-lead-contact-phone": {
        "options": {"classes": "govuk-!-width-full"},
        "type": "TelephoneNumberField",
        "title": "Lead contact telephone number",
    },
    "reuse_is_lead_contact_same_as_auth_signatory": {
        "options": {},
        "type": "YesNoField",
        "title": (
            "Is the lead contact the same person as the authorised signatory?"
        ),
        "hint": (
            '<p class="govuk-hint">An authorised signatory:<ul'
            ' class="govuk-list govuk-list--bullet govuk-hint"> <li>is allowed'
            " to act on behalf of the organisation</li> <li>will sign the"
            " grant funding agreement if your application is"
            " successful</li></ul></p>"
        ),
        "conditions": [
            {
                "name": "lead_contact_same_as_signatory_yes",
                "value": "true",
                "operator": "is",
                "destination_page": "CONTINUE",
            },
            {
                "name": "lead_contact_same_as_signatory_no",
                "value": "false",
                "operator": "is",
                "destination_page": "/authorised-signatory-details",
            },
        ],
    },
}
