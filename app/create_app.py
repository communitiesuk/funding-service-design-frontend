from app.filters import date_format_short_month
from app.filters import datetime_format
from app.filters import datetime_format_short_month
from app.filters import kebab_case_to_human
from app.filters import snake_case_to_human
from config import Config
from flask import Flask
from flask_babel import Babel
from flask_babel import gettext
from flask_compress import Compress
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from fsd_utils import init_sentry
from fsd_utils import LanguageSelector
from fsd_utils.healthchecks.checkers import FlaskRunningChecker
from fsd_utils.healthchecks.healthcheck import Healthcheck
from fsd_utils.locale_selector.get_lang import get_lang
from fsd_utils.logging import logging
from jinja2 import ChoiceLoader
from jinja2 import PackageLoader
from jinja2 import PrefixLoader


def create_app() -> Flask:
    init_sentry()

    flask_app = Flask(__name__, static_url_path="/assets")

    flask_app.config.from_object("config.Config")

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

    # Initialise logging
    logging.init_app(flask_app)

    # Configure application security with Talisman
    Talisman(flask_app, **Config.TALISMAN_SETTINGS)

    csrf = CSRFProtect()
    csrf.init_app(flask_app)

    Compress(flask_app)

    from app.default.routes import default_bp, not_found, internal_server_error

    flask_app.register_error_handler(404, not_found)
    flask_app.register_error_handler(500, internal_server_error)
    flask_app.register_blueprint(default_bp)
    flask_app.jinja_env.filters[
        "datetime_format_short_month"
    ] = datetime_format_short_month
    flask_app.jinja_env.filters[
        "date_format_short_month"
    ] = date_format_short_month
    flask_app.jinja_env.filters["datetime_format"] = datetime_format
    flask_app.jinja_env.filters["snake_case_to_human"] = snake_case_to_human
    flask_app.jinja_env.filters["kebab_case_to_human"] = kebab_case_to_human

    @flask_app.context_processor
    def inject_global_constants():
        return dict(
            stage="beta",
            service_title=(
                gettext("Apply for funding to save an asset in your community")
            ),
            service_meta_description=(
                "Apply for funding to save an asset in your community"
            ),
            service_meta_keywords=(
                "Apply for funding to save an asset in your community"
            ),
            service_meta_author=(
                "Department for Levelling up Housing and Communities"
            ),
        )

    health = Healthcheck(flask_app)
    health.add_check(FlaskRunningChecker())

    return flask_app


app = create_app()
