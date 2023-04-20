from os import getenv
from app.default.data import get_fund_data
from app.default.data import get_fund_data_by_short_name
from app.filters import date_format_short_month
from app.filters import datetime_format
from app.filters import datetime_format_short_month
from app.filters import kebab_case_to_human
from app.filters import snake_case_to_human
from app.filters import status_translation
from app.models.fund import FUND_SHORT_CODES
from config import Config
from flask import current_app
from flask import Flask
from flask import make_response
from flask import request
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


def create_app() -> Flask:
    init_sentry()

    flask_app = Flask(__name__, static_url_path="/assets")

    flask_app.config.from_object("config.Config")

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
            } if toggle_client else {},
        )

    @flask_app.context_processor
    def inject_service_name():
        fund = None
        if request.view_args or request.args:
            try:
                fund_short_name = request.view_args.get("fund_short_name")
                if fund_short_name and str.upper(fund_short_name) in [
                    member.value for member in FUND_SHORT_CODES
                ]:
                    fund = get_fund_data_by_short_name(fund_short_name)
                elif request.view_args.get("fund_id"):
                    fund = get_fund_data(
                        request.view_args.get("fund_id"), True
                    )
                elif request.args.get("fund_id"):
                    fund = get_fund_data(request.args.get("fund_id"), True)
                elif request.args.get("fund"):
                    fund = get_fund_data_by_short_name(
                        request.args.get("fund")
                    )
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

    @flask_app.before_request
    def filter_favicon_requests():
        if request.path == "/favicon.ico":
            return make_response("404"), 404

    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())

    return flask_app


app = create_app()
