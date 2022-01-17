import os

from app.config import Config
from flask import Flask
from flask_compress import Compress
from flask_talisman import Talisman
from jinja2 import ChoiceLoader
from jinja2 import PackageLoader
from jinja2 import PrefixLoader


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__, instance_relative_config=True, static_url_path="/assets"
    )  # noqa

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile("config.py", silent=True)
        app.config.from_object(Config())
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    app.jinja_loader = ChoiceLoader(
        [
            PackageLoader("app"),
            PrefixLoader(
                {"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")}
            ),
        ]
    )

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True

    csp = {
        "default-src": "'self'",
        "script-src": [
            "'self'",
            "'sha256-+6WnXIl4mbFTCARd8N3COQmT3bJJmo32N8q8ZSQAIcU='",
            "'sha256-l1eTVSK8DTnK8+yloud7wZUqFrI0atVo6VlC6PJvYaQ='",
        ],
        "img-src": ["data:", "'self'"],
    }

    Compress(app)
    Talisman(app, content_security_policy=csp)

    @app.context_processor
    def inject_global_constants():
        return dict(
            stage="alpha",
            region="NA",
            service_title="DLUHC Funding Service Design Iteration 1",
            service_meta_description="DLUHC Funding Service Design Iteration 1",  # noqa
            service_meta_keywords="DLUHC Funding Service Design Iteration 1",
            service_meta_author="Evoco Digital Services",
        )

    from app.routes import bp as default_routes
    from app.routes import not_found, internal_server_error

    app.register_error_handler(404, not_found)
    app.register_error_handler(500, internal_server_error)
    app.register_blueprint(default_routes)

    return app


app = create_app()
