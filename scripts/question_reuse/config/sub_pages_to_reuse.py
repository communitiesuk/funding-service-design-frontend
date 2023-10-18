SUB_PAGES_TO_REUSE = {
    "conditions": [],
    "subpages": [
        {
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
        {
            "path": "/summary",
            "title": "Check your answers",
            "components": [],
            "next": [],
            "section": "uLwBuz",
            "controller": "./pages/summary.js",
        },
    ],
}
