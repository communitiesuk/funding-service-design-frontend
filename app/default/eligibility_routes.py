from app.default.data import get_fund_data
from app.default.data import get_round_data
from app.default.data import get_ttl_hash
from app.helpers import format_rehydrate_payload
from app.helpers import get_token_to_return_to_application
from config import Config
from flask import Blueprint
from flask import current_app
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

eligibility_bp = Blueprint("eligibility_routes", __name__, template_folder="templates")


def get_fund_and_round_short_name(fund_id,round_id):
    fund_data = get_fund_data(
        fund_id=fund_id,
        language="en",
        as_dict=False,
        ttl_hash=get_ttl_hash(Config.LRU_CACHE_TIME),
    )
    round_data = get_round_data(
        fund_id,
        round_id,
        as_dict=False,
        ttl_hash=get_ttl_hash(Config.LRU_CACHE_TIME),
    )
    return fund_data.short_name.lower(), round_data.short_name.lower()


@eligibility_bp.route("/eligibility_result", methods=["GET"])
def eligiblity_result():
    current_app.logger.info(f"Eligibility launch result")
    try:
        eligiblity_result = request.args.get("result")
    except Exception as e:
        current_app.logger.info(f"exception launch result")
    return render_template("eligibility_result.html", eligiblity_result=eligiblity_result)


@eligibility_bp.route("/launch_eligibility/<fund_id>/<round_id>", methods=["POST"])
def launch_eligibility(fund_id, round_id):
    # TODO do something with the fund and round id here to find out what the form name should be
    # It should be stored as part of the eligibility_config json in the round
    fund_name, round_name = get_fund_and_round_short_name(fund_id, round_id)
    form_name = f"{fund_name}-{round_name}-eligibility"

    current_app.logger.info(f"Eligibility launch request for fund {fund_name} round {round_name}")
    return_url = request.host_url + url_for("eligibility_routes.eligiblity_result", result=True)
    current_app.logger.info(f"Url the form runner should return to '{return_url}'.")

    # TODO do we need to retrieve an in-progress eligibility form here?
    # TODO work out what to use for application ID as they don't have one yet -
    # TODO think this might be used as part of the session identifier in form runner so is leaving it blank ok?

    rehydrate_payload = format_rehydrate_payload(
        form_data={"questions": []},
        application_id=None,
        returnUrl=return_url,
        form_name=form_name,
        markAsCompleteEnabled=False  # assume we don't have it for eligibility
        # callback_url=Config.UPDATE_ELIGIBILITY_RESULT_ENDPOINT,
    )

    rehydration_token = get_token_to_return_to_application(form_name, rehydrate_payload)

    redirect_url = Config.FORM_REHYDRATION_URL.format(rehydration_token=rehydration_token)
    if Config.FORMS_SERVICE_PRIVATE_HOST:
        redirect_url = redirect_url.replace(Config.FORMS_SERVICE_PRIVATE_HOST, Config.FORMS_SERVICE_PUBLIC_HOST)
    current_app.logger.info("redirecting to form runner")
    return redirect(redirect_url)
