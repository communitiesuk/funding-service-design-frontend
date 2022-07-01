from app.filters import datetime_format
from app.filters import kebab_case_to_human
from app.filters import snake_case_to_human
from flask import Flask
from flask_babel import Babel
from flask_compress import Compress
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from fsd_utils.logging import logging
from jinja2 import ChoiceLoader
from jinja2 import PackageLoader
from jinja2 import PrefixLoader


def create_app() -> Flask:
    flask_app = Flask(__name__, static_url_path="/assets")

    flask_app.config.from_pyfile("config.py")
    Babel(flask_app)

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

    @flask_app.context_processor
    def inject_global_constants():
        return dict(
            stage="beta",
            service_title="DLUHC Funding Service Design Iteration 2",
            service_meta_description=(
                "DLUHC Funding Service Design Iteration 2"
            ),
            service_meta_keywords="DLUHC Funding Service Design Iteration 1",
            service_meta_author="DLUHC",
        )

    from app.default.routes import default_bp, not_found, internal_server_error

    flask_app.register_error_handler(404, not_found)
    flask_app.register_error_handler(500, internal_server_error)
    flask_app.register_blueprint(default_bp)
    flask_app.jinja_env.filters["datetime_format"] = datetime_format
    flask_app.jinja_env.filters["snake_case_to_human"] = snake_case_to_human
    flask_app.jinja_env.filters["kebab_case_to_human"] = kebab_case_to_human

    # Initialise logging
    logging.init_app(flask_app)

    # Configure Talisman Security Settings
    # csp = {
    #     "default-src": "'self'",
    #     "script-src": [
    #         "'self'",
    #         "'sha256-+6WnXIl4mbFTCARd8N3COQmT3bJJmo32N8q8ZSQAIcU='",
    #         "'sha256-l1eTVSK8DTnK8+yloud7wZUqFrI0atVo6VlC6PJvYaQ='",
    #     ],
    #     "img-src": ["data:", "'self'"],
    # }

    # hss = {
    #     "Strict-Transport-Security": (
    #         "max-age=31536000; includeSubDomains; preload"
    #     ),
    #     "X-Content-Type-Options": "nosniff",
    #     "X-Frame-Options": "SAMEORIGIN",
    #     "X-XSS-Protection": "1; mode=block",
    #     "Feature_Policy": (
    #         "microphone 'none'; camera 'none'; geolocation 'none'"
    #     ),
    # }

    Talisman(
        flask_app,
        # AWAITING CONFIG UPDATE FIX
        # content_security_policy=csp,
        # strict_transport_security=hss,
        # force_https=False,
    )

    csrf = CSRFProtect()
    csrf.init_app(flask_app)

    Compress(flask_app)

    return flask_app


app = create_app()
