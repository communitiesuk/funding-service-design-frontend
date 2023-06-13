from os import getenv

from app.default.data import get_application_data
from app.default.data import get_default_round_for_fund
from app.default.data import get_fund_data
from app.default.data import get_fund_data_by_short_name
from app.default.data import get_round_data
from app.default.data import get_round_data_fail_gracefully
from app.filters import date_format_short_month
from app.filters import datetime_format
from app.filters import datetime_format_short_month
from app.filters import kebab_case_to_human
from app.filters import snake_case_to_human
from app.filters import status_translation
from app.models.fund import Fund
from app.models.fund import FUND_SHORT_CODES
from config import Config
from flask import current_app
from flask import Flask
from flask import make_response
from flask import request
from flask import url_for
from flask_babel import Babel
from flask_babel import gettext
from flask_babel import pgettext
from flask_compress import Compress
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from fsd_utils import init_sentry
from fsd_utils import LanguageSelector
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.locale_selector.get_lang import get_lang
from fsd_utils.logging import logging
from fsd_utils.toggles.toggles import create_toggles_client
from fsd_utils.toggles.toggles import initialise_toggles_redis_store
from fsd_utils.toggles.toggles import load_toggles
from jinja2 import ChoiceLoader
from jinja2 import PackageLoader
from jinja2 import PrefixLoader


def find_round_in_request(fund):
    if round_short_name := request.view_args.get(
        "round_short_name"
    ) or request.args.get("round"):
        round = get_round_data_fail_gracefully(
            fund.short_name, round_short_name, True
        )
        # use default round if incorrect round name is provided
        if not round.id:
            round = get_default_round_for_fund(fund.short_name)
            current_app.logger.warning(
                f"Invalid round_short_name '{round_short_name}' provided."
                f" Using default '{round.short_name}' round for"
                f" {fund.short_name}."
            )
    elif (
        application_id := request.args.get("application_id")
        or request.view_args.get("application_id")
        or request.form.get("application_id")
    ):
        application = get_application_data(application_id, as_dict=True)
        round = get_round_data(
            fund_id=application.fund_id,
            round_id=application.round_id,
            language=application.language,
        )
    else:
        round = get_default_round_for_fund(fund.short_name)
        current_app.logger.warn(
            "Couldn't find round in request. Using"
            f" {round.short_name} as default for fund {fund.short_name}"
        )
    return round


def find_fund_in_request():
    if (
        fund_short_name := request.view_args.get("fund_short_name")
        or request.args.get("fund")
    ) and str.upper(fund_short_name) in [
        member.value for member in FUND_SHORT_CODES
    ]:
        fund = get_fund_data_by_short_name(fund_short_name, as_dict=False)
    elif fund_id := request.view_args.get("fund_id") or request.args.get(
        "fund_id"
    ):
        fund = get_fund_data(fund_id, as_dict=True)
    elif (
        application_id := request.args.get("application_id")
        or request.view_args.get("application_id")
        or request.form.get("application_id")
    ):
        application = get_application_data(application_id, as_dict=True)
        fund = get_fund_data(
            fund_id=application.fund_id,
            language=application.language,
            as_dict=True,
        )
    else:
        current_app.logger.warn("Couldn't find any fund in the request")
        return None
    return fund


def create_app() -> Flask:
    init_sentry()

    flask_app = Flask(__name__, static_url_path="/assets")

    flask_app.config.from_object("config.Config")

    toggle_client = None
    if getenv("FLASK_ENV") != "unit_test":
        initialise_toggles_redis_store(flask_app)
        toggle_client = create_toggles_client()
        load_toggles(Config.FEATURE_CONFIG, toggle_client)

    babel = Babel(flask_app)
    babel.locale_selector_func = get_lang
    LanguageSelector(flask_app)

    flask_app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PrefixLoader(
                {"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")}
            ),
        ]
    )

    flask_app.jinja_env.trim_blocks = True
    flask_app.jinja_env.lstrip_blocks = True
    flask_app.jinja_env.add_extension("jinja2.ext.i18n")
    flask_app.jinja_env.globals["get_lang"] = get_lang
    flask_app.jinja_env.globals["pgettext"] = pgettext

    # Initialise logging
    logging.init_app(flask_app)

    # Configure application security with Talisman
    Talisman(flask_app, **Config.TALISMAN_SETTINGS)

    csrf = CSRFProtect()
    csrf.init_app(flask_app)

    Compress(flask_app)

    from app.default.routes import default_bp
    from app.default.application_routes import application_bp
    from app.default.content_routes import content_bp
    from app.default.account_routes import account_bp
    from app.default.error_routes import not_found, internal_server_error

    flask_app.register_error_handler(404, not_found)
    flask_app.register_error_handler(500, internal_server_error)
    flask_app.register_blueprint(default_bp)
    flask_app.register_blueprint(application_bp)
    flask_app.register_blueprint(content_bp)
    flask_app.register_blueprint(account_bp)
    flask_app.jinja_env.filters[
        "datetime_format_short_month"
    ] = datetime_format_short_month
    flask_app.jinja_env.filters[
        "date_format_short_month"
    ] = date_format_short_month
    flask_app.jinja_env.filters["datetime_format"] = datetime_format
    flask_app.jinja_env.filters["snake_case_to_human"] = snake_case_to_human
    flask_app.jinja_env.filters["kebab_case_to_human"] = kebab_case_to_human
    flask_app.jinja_env.filters["status_translation"] = status_translation

    @flask_app.context_processor
    def inject_global_constants():
        return dict(
            stage="beta",
            service_meta_description=(
                "Apply for funding to save an asset in your community"
            ),
            service_meta_keywords=(
                "Apply for funding to save an asset in your community"
            ),
            service_meta_author=(
                "Department for Levelling up Housing and Communities"
            ),
            toggle_dict={
                feature.name: feature.is_enabled()
                for feature in toggle_client.list()
            }
            if toggle_client
            else {},
        )

    @flask_app.context_processor
    def inject_service_name():
        fund = None
        if request.view_args or request.args or request.form:
            try:
                fund = find_fund_in_request()
            except Exception as e:  # noqa
                current_app.logger.warn(
                    f"""Exception: {e}, occured when trying to
                    reach url: {request.url}, with view_args:
                    {request.view_args}, and args: {request.args}"""
                )
        if fund:
            service_title = gettext("Apply for") + " " + fund.title
        else:
            service_title = gettext("Access Funding")
        return dict(service_title=service_title)

    @flask_app.context_processor
    def inject_content_urls():
        try:
            fund: Fund = find_fund_in_request()
            round = find_round_in_request(fund)
            if round:
                return dict(
                    contact_us_url=url_for(
                        "content_routes.contact_us",
                        fund=fund.short_name,
                        round=round.short_name,
                    ),
                    privacy_url=url_for(
                        "content_routes.privacy",
                        fund=fund.short_name,
                        round=round.short_name,
                    ),
                    feedback_url=url_for(
                        "content_routes.feedback",
                        fund=fund.short_name,
                        round=round.short_name,
                    ),
                )
        except Exception as e:  # noqa
            current_app.logger.warn(
                f"""Exception: {e}, occured when trying to
                reach url: {request.url}, with view_args:
                {request.view_args}, and args: {request.args}"""
            )
        return dict(
            contact_us_url=url_for("content_routes.contact_us"),
            privacy_url=url_for("content_routes.privacy"),
            feedback_url=url_for("content_routes.feedback"),
        )

    @flask_app.after_request
    def after_request(response):
        if "Cache-Control" not in response.headers:
            response.headers[
                "Cache-Control"
            ] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        return response

    @flask_app.before_request
    def filter_favicon_requests():
        if request.path == "/favicon.ico":
            return make_response("404"), 404

    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())

    return flask_app


app = create_app()
