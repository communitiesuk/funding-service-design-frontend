SUB_PAGES_TO_REUSE = {
    "/alternative-organisation-name": {
        "path": "/alternative-organisation-name",
        "title": "Alternative names of your organisation",
        "components": [
            {
                "name": "reuse-alt-org-name-1",
                "options": {"classes": "govuk-input"},
                "type": "TextField",
                "title": "Alternative name 1",
                "schema": {},
            },
            {
                "name": "reuse-alt-org-name-2",
                "options": {"required": False, "classes": "govuk-input"},
                "type": "TextField",
                "title": "Alternative name 2",
                "schema": {},
            },
            {
                "name": "reuse-alt-org-name-3",
                "options": {"required": False, "classes": "govuk-input"},
                "type": "TextField",
                "title": "Alternative name 3",
                "schema": {},
            },
        ],
    },
    "/authorised-signatory-details": {
      "path": "/authorised-signatory-details",
      "title": "Authorised signatory details",
      "components": [
        {
          "name": "xKWJWW",
          "options": {},
          "type": "Html",
          "content": "<p class=\"govuk-hint\">An authorised signatory:</p>\n<ul class=\"govuk-list govuk-list--bullet govuk-hint\">\n            <li>is allowed to act on behalf of the organisation</li>\n            <li>will sign the grant funding agreement if your application is successful</li>\n          </ul>",
          "schema": {}
        },
        {
          "name": "pDrPDz",
          "options": {
            "classes": "govuk-!-width-full"
          },
          "type": "TextField",
          "title": "Authorised signatory full name",
          "schema": {}
        },
        {
          "name": "teowxM",
          "options": {
            "required": False,
            "classes": "govuk-!-width-full"
          },
          "type": "TextField",
          "title": "Alternative name",
          "schema": {}
        },
        {
          "name": "tikwxM",
          "options": {
            "required": True,
            "classes": "govuk-!-width-full"
          },
          "type": "TextField",
          "title": "Authorised signatory job title",
          "schema": {}
        },
        {
          "name": "ljfzCy",
          "options": {
            "classes": "govuk-!-width-full"
          },
          "type": "EmailAddressField",
          "title": "Authorised signatory email address",
          "schema": {}
        },
        {
          "name": "gNgJme",
          "options": {
            "classes": "govuk-!-width-full"
          },
          "type": "TelephoneNumberField",
          "title": "Authorised signatory telephone number",
          "schema": {}
        }
      ],
    },
    "/summary": {
        "path": "/summary",
        "title": "Check your answers",
        "components": [],
        "next": [],
        "section": "uLwBuz",
        "controller": "./pages/summary.js",
    },
}
