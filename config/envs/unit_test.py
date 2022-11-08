"""Flask Local Development Environment Configuration."""
from config.envs.default import DefaultConfig
from fsd_utils import configclass


@configclass
class UnitTestConfig(DefaultConfig):
    DefaultConfig.TALISMAN_SETTINGS["force_https"] = False
    USE_LOCAL_DATA = "True"
    SESSION_COOKIE_SECURE = False

    # RSA 256 KEYS
    _test_private_key_path = (
        DefaultConfig.FLASK_ROOT + "/tests/keys/rsa256/private.pem"
    )
    with open(_test_private_key_path, mode="rb") as private_key_file:
        RSA256_PRIVATE_KEY = private_key_file.read()
    _test_public_key_path = (
        DefaultConfig.FLASK_ROOT + "/tests/keys/rsa256/public.pem"
    )
    with open(_test_public_key_path, mode="rb") as public_key_file:
        RSA256_PUBLIC_KEY = public_key_file.read()

    WTF_CSRF_ENABLED = False

    COF_R2_ORDERED_FORMS_CONFIG = (
        {
            "section_title":{
                "en": "About your organisation",
                "cy": "Ynglŷn â'ch sefydliad"
            },
            "ordered_form_names_within_section":[
                {
                    "en":"organisation-information",
                    "cy":"gwybodaeth-am-y-sefydliad"
                },
                {
                    "en":"applicant-information",
                    "cy":"gwybodaeth-am-yr-ymgeisydd"
                },
            ],
            "section_weighting": None
        },
        {
            "section_title":{
                "en":"About your project",
                "cy":"Ynglŷn â'ch prosiect"
            },
            "ordered_form_names_within_section":[
                {
                    "en":"project-information",
                    "cy":"gwybodaeth-am-y-prosiect"
                },
                {
                    "en":"asset-information",
                    "cy":"gwybodaeth-am-yr-ased"
                },
            ],
            "section_weighting": None
        },
        {
            "section_title":{
                "en":"Strategic case",
                "cy":"Achos strategol"
            },
            "ordered_form_names_within_section":[
                {
                    "en":"community-use",
                    "cy":"defnydd-cymunedol"
                },
                {
                    "en":"community-engagement",
                    "cy":"ymgysylltiad-cymunedol"
                },
                {
                    "en":"local-support",
                    "cy":"cefnogaeth-leol"
                },
                {
                    "en":"environmental-sustainability",
                    "cy":"cynaliadwyedd-amgylcheddol"
                },
            ],
            "section_weighting": 30,
        },
        {
            "section_title":{
                "en":"Management case",
                "cy":"Achos rheoli"
            },
            "ordered_form_names_within_section":[
                {
                    "en":"funding-required",
                    "cy":"cyllid-angenrheidiol"
                },
                {
                    "en":"feasibility",
                    "cy":"dichonoldeb"
                },
                {
                    "en":"risk",
                    "cy":"risg"
                },
                {
                    "en":"project-costs",
                    "cy":"costau'r-prosiect"
                },
                {
                    "en":"skills-and-resources",
                    "cy":"sgiliau-ac-adnoddau"
                },
                {
                    "en":"community-representation",
                    "cy":"cynrychiolaeth-gymunedol"
                },
                {
                    "en":"inclusiveness-and-integration",
                    "cy":"cynhwysiant-ac-integreiddio"
                },
                {
                    "en":"upload-business-plan",
                    "cy":"lanlwytho-cynllun-busnes"
                },
            ],
            "section_weighting": 30,
        },
        {
            "section_title":{
                "en": "Potential to deliver community benefits",
                "cy": "Potensial i gyflawni buddion cymunedol"
            },
            "ordered_form_names_within_section":[
                {
                    "en":"community-benefits",
                    "cy":"buddion-cymunedol"
                },
            ],
            "section_weighting": 30
        },
        {
            "section_title":{
                "en": "Added value to community",
                "cy": "Gwerth ychwanegol i'r gymuned"
            },
            "ordered_form_names_within_section":[
                {
                    "en":"value-to-the-community",
                    "cy":"gwerth-i'r-gymuned"
                },
            ],
            "section_weighting": 10
        },
        {
            "section_title":{
                "en": "Subsidy control / state aid",
                "cy": "Rheoli cymorthdaliadau a chymorth gwladwriaethol"
            },
            "ordered_form_names_within_section":[
                {
                    "en":"project-qualification",
                    "cy":"cymhwysedd-y-prosiect"
                },
            ],
            "section_weighting": None
        },
        {
            "section_title":{
                "en": "Check declarations",
                "cy": "Gwirio datganiadau"
            },
            "ordered_form_names_within_section":[
                {
                    "en":"declarations",
                    "cy":"datganiadau"
                },
            ],
            "section_weighting": None
        }
    )
    FORMS_CONFIG_FOR_FUND_ROUND = {
        "funding-service-design:summer": COF_R2_ORDERED_FORMS_CONFIG,
    }