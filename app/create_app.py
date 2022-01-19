from flask import Flask
from flask_compress import Compress
from flask_seasurf import SeaSurf
from flask_talisman import Talisman
from jinja2 import ChoiceLoader
from jinja2 import PackageLoader
from jinja2 import PrefixLoader

app = Flask(__name__, static_url_path="/assets")
app.config.from_pyfile("config.py")

csrf = SeaSurf()
csrf.init_app(app)

app.jinja_loader = ChoiceLoader(
    [
        PackageLoader("app"),
        PrefixLoader(
            {"govuk_frontend_jinja": PackageLoader("govuk_frontend_jinja")}
        ),  # noqa
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

hss = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",  # noqa
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "SAMEORIGIN",
    "X-XSS-Protection": "1; mode=block",
    "Feature_Policy": "microphone 'none'; camera 'none'; geolocation 'none'",
}

Compress(app)
Talisman(app, content_security_policy=csp, strict_transport_security=hss)


@app.context_processor
def inject_global_constants():
    return dict(
        stage="alpha",
        region="NA",
        service_title="DLUHC Funding Service Design Iteration 1",
        service_meta_description="DLUHC Funding Service Design Iteration 1",
        service_meta_keywords="DLUHC Funding Service Design Iteration 1",
        service_meta_author="Evoco Digital Services",
    )


from app import routes  # noqa
