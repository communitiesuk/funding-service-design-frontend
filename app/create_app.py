import imp
from flask import Flask
from flask_compress import Compress
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect
from jinja2 import ChoiceLoader
from jinja2 import PackageLoader
from jinja2 import PrefixLoader
from build import build_assets


def create_app() -> Flask:
    flask_app = Flask(__name__, static_url_path="/assets")

    flask_app.config.from_pyfile("config.py")

        # Auto build the static assets if we are in the dev environment.
    # In production we will most likely install static assets differently.
    if flask_app.config.get("ENV") == "development":

        build_assets()


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

    csp = {
        "default-src": "'self'",
        "script-src": [
            "'self'",
            "'sha256-+6WnXIl4mbFTCARd8N3COQmT3bJJmo32N8q8ZSQAIcU='",
            "'sha256-l1eTVSK8DTnK8+yloud7wZUqFrI0atVo6VlC6PJvYaQ='",
        ],
        "img-src": ["data:", "'self'"],
    }

    hss = {
        "Strict-Transport-Security": (
            "max-age=31536000; includeSubDomains; preload"
        ),
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-XSS-Protection": "1; mode=block",
        "Feature_Policy": (
            "microphone 'none'; camera 'none'; geolocation 'none'"
        ),
    }

    Compress(flask_app)
    Talisman(
        flask_app, content_security_policy=csp, strict_transport_security=hss
    )

    csrf = CSRFProtect()

    csrf.init_app(flask_app)

    @flask_app.context_processor
    def inject_global_constants():
        return dict(
            stage="alpha",
            region="NA",
            service_title="DLUHC Funding Service Design Iteration 1",
            service_meta_description=(
                "DLUHC Funding Service Design Iteration 1"
            ),
            service_meta_keywords="DLUHC Funding Service Design Iteration 1",
            service_meta_author="DLUHC",
        )

    from app.default.routes import default_bp, not_found, internal_server_error

    flask_app.register_error_handler(404, not_found)
    flask_app.register_error_handler(500, internal_server_error)
    flask_app.register_blueprint(default_bp)

    return flask_app


app = create_app()
