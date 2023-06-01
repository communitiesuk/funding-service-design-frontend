from datetime import datetime

from app.models.application_summary import ApplicationSummary
from app.models.round import Round

common_round_data = {
    "opens": "2022-09-01T00:00:01",
    "assessment_deadline": "2030-03-20T00:00:01",
    "contact_email": "test@example.com",
    "contact_phone": "123456789",
    "contact_textphone": "123456789",
    "support_times": "9-5",
    "support_days": "Mon-Fri",
    "prospectus": "/cof_r2w2_prospectus",
    "instructions": "Round specific instruction text",
    "privacy_notice": "",
    "project_name_field_id": "",
    "feedback_link": "",
    "application_guidance": "",
}
common_application_data = {
    "account_id": "test-user",
    "reference": "TEST-REF-B",
    "project_name": "Test project",
    "date_submitted": None,
    "started_at": "2022-05-20T14:47:12",
    "last_edited": "2022-05-24T11:03:59",
    "language": "en",
    "id": "xxxx",
    "status": "IN_PROGRESS",
    "fund_id": "xxx",
    "round_id": "xxx",
}
TEST_APP_STORE_DATA = [
    ApplicationSummary.from_dict(
        {
            **common_application_data,
            "id": "1111",
            "status": "IN_PROGRESS",
            "fund_id": "111",
            "round_id": "fsd-r2w2",
        }
    ),
    ApplicationSummary.from_dict(
        {
            **common_application_data,
            "id": "2222",
            "status": "NOT_STARTED",
            "fund_id": "111",
            "round_id": "fsd-r2w3",
        }
    ),
    ApplicationSummary.from_dict(
        {
            **common_application_data,
            "id": "3333",
            "status": "SUBMITTED",
            "fund_id": "222",
            "round_id": "abc-r1",
        }
    ),
    ApplicationSummary.from_dict(
        {
            **common_application_data,
            "id": "4444",
            "status": "READY_TO_SUBMIT",
            "fund_id": "222",
            "round_id": "abc-r1",
        }
    ),
]
TEST_FUNDS_DATA = [
    {
        "id": "111",
        "name": "Test Fund",
        "description": "test test",
        "short_name": "FSD",
        "title": "fund for testing",
        "welsh_available": True,
    },
    {
        "id": "222",
        "name": "Test Fund 2",
        "description": "test test 2",
        "short_name": "FSD2",
        "title": "fund for testing 2",
        "welsh_available": False,
    },
]

TEST_ROUNDS_DATA = [
    Round.from_dict(
        {
            **common_round_data,
            "fund_id": "111",
            "id": "fsd-r2w2",
            "short_name": "r2w2",
            "title": "closed_round",
            "deadline": "2023-01-01T00:00:01",
        }
    ),
    Round.from_dict(
        {
            **common_round_data,
            "fund_id": "111",
            "id": "fsd-r2w3",
            "short_name": "r2w3",
            "title": "open_round",
            "deadline": "2050-01-01T00:00:01",
        }
    ),
    Round.from_dict(
        {
            **common_round_data,
            "fund_id": "222",
            "id": "abc-r1",
            "short_name": "r1",
            "title": "closed_round",
            "deadline": "2023-01-01T00:00:01",
        }
    ),
    Round.from_dict(
        {
            **common_round_data,
            "fund_id": "222",
            "id": "abc-r2",
            "short_name": "r2",
            "title": "open_round",
            "deadline": "2050-01-01T00:00:01",
        }
    ),
]

TEST_DISPLAY_DATA = {
    "total_applications_to_display": 4,
    "funds": [
        {
            "fund_data": {
                "id": "funding-service-design",
                "name": "Test Fund",
                "description": "test test",
                "short_name": "FSD",
            },
            "rounds": [
                {
                    "is_past_submission_deadline": True,
                    "is_not_yet_open": False,
                    "round_details": {
                        "opens": "2022-09-01T00:00:01",
                        "deadline": "2030-01-30T00:00:01",
                        "assessment_deadline": "2030-03-20T00:00:01",
                        "id": "cof-r2w2",
                        "title": "Round 2 Window 2",
                        "instructions": "r2w2 instructions",
                        "fund_id": "fund-service-design",
                        "short_name": "R2W2",
                        "contact_email": "test@example.com",
                        "contact_phone": "123456789",
                        "contact_textphone": "123456789",
                        "support_times": "9-5",
                        "support_days": "Mon-Fri",
                    },
                    "applications": [
                        {
                            "id": "uuidv4",
                            "reference": "TEST-REF-B",
                            "status": "NOT_SUBMITTED",
                            "round_id": "summer",
                            "fund_id": "funding-service-design",
                            "started_at": "2020-01-01T12:03:00",
                            "project_name": None,
                            "last_edited": datetime.strptime(
                                "2020-01-01T12:03:00", "%Y-%m-%dT%H:%M:%S"
                            ),
                        },
                        {
                            "id": "ed221ac8-5d4d-42dd-ab66-6cbcca8fe257",
                            "reference": "TEST-REF-C",
                            "status": "SUBMITTED",
                            "round_id": "summer",
                            "fund_id": "funding-service-design",
                            "started_at": "2023-01-01T12:01:00",
                            "project_name": "",
                            "last_edited": None,
                        },
                    ],
                },
                {
                    "is_past_submission_deadline": False,
                    "is_not_yet_open": False,
                    "round_details": {
                        "opens": "2022-09-01T00:00:01",
                        "deadline": "2030-01-30T00:00:01",
                        "assessment_deadline": "2030-03-20T00:00:01",
                        "id": "summer",
                        "title": "Summer round",
                        "fund_id": "fund-service-design",
                        "short_name": "R2W3",
                        "instructions": "r2w3 instructions",
                        "contact_email": "test@example.com",
                        "contact_phone": "123456789",
                        "contact_textphone": "123456789",
                        "support_times": "9-5",
                        "support_days": "Mon-Fri",
                    },
                    "applications": [
                        {
                            "id": "uuidv4",
                            "reference": "TEST-REF-B",
                            "status": "IN_PROGRESS",
                            "round_id": "summer",
                            "fund_id": "funding-service-design",
                            "started_at": "2020-01-01T12:03:00",
                            "project_name": None,
                            "last_edited": datetime.strptime(
                                "2020-01-01T12:03:00", "%Y-%m-%dT%H:%M:%S"
                            ),
                        },
                        {
                            "id": "ed221ac8-5d4d-42dd-ab66-6cbcca8fe257",
                            "reference": "TEST-REF-C",
                            "status": "READY_TO_SUBMIT",
                            "round_id": "summer",
                            "fund_id": "funding-service-design",
                            "started_at": "2023-01-01T12:01:00",
                            "project_name": "",
                            "last_edited": None,
                        },
                    ],
                },
            ],
        }
    ],
}
