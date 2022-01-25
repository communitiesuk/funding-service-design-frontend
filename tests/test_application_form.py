"""
Tests if pages of the FORMS_SERVICE_HOST
are accessible according to WCAG standards

Form .json files should be placed in either the
'public' or 'preview' folders beneath the
FORM_SERVICE_JSONS_PATH

Form .json files should follow the following
schema hierarchy:

{
  "metadata": {},
  "startPage": "/about-you",
  "pages": [
    {
      "title": "About you",
      "path": "/about-you",
      "components": [
        {
          "name": "applicant_name",
          "options": {},
          "type": "TextField",
          "title": "Applicant name",
          "schema": {},
          "nameHasError": false
        },
        {
          "type": "EmailAddressField",
          "title": "Email",
          "name": "email-about-you",
          "nameHasError": false,
          "options": {},
          "schema": {}
        }
      ],
      "next": []
    }
  ],
  "lists": [
    {
      "title": "types-of-organisations",
      "name": "IumAbm",
      "type": "string",
      "items": [
        {
          "text": "Local authority",
          "value": "isLocalAuthority"
        }
      ]
    }
  ],
  "sections": [
    {
      "name": "kfFsQz",
      "title": "Question 1 of 2"
    },
  ],
  "conditions": [
    {
      "displayName": "isLimitedCompany",
      "name": "faPfLD",
      "value": {
        "name": "isLimitedCompany",
        "conditions": [
          {
            "field": {
              "name": "kfFsQz.IjcnGk",
              "type": "RadiosField",
              "display": "Type of organisation"
            },
            "operator": "is",
            "value": {
              "type": "Value",
              "value": "Limited Company",
              "display": "Limited Company"
            }
          }
        ]
      }
    }
  ],
  "fees": [],
  "outputs": [],
  "version": 2,
  "skipSummary": false,
  "name": "Most Recent Gov Uk Form",
  "feedback": {
    "feedbackForm": false,
    "url": ""
  },
  "phaseBanner": {
    "phase": "beta"
  }
}
"""
import json
import os

import pytest
from app.config import FORMS_SERVICE_HOST
from app.config import FORMS_SERVICE_JSONS_PATH
from app.config import FORMS_SERVICE_NAME
from app.config import FORMS_SERVICE_TEST_FORM
from app.config import FORMS_SERVICE_TEST_PUBLIC_FORM
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.errorhandler import NoSuchElementException

from .test_accessibility import run_axe_and_print_report


def get_test_form_routes():
    forms = {}
    forms_dir = "preview"
    if FORMS_SERVICE_TEST_PUBLIC_FORM:
        forms_dir = "public"
    form_jsons_dir = os.path.join(".", FORMS_SERVICE_JSONS_PATH, forms_dir)
    form_jsons = os.listdir(form_jsons_dir)
    for form_json in form_jsons:
        f = open(os.path.join(form_jsons_dir, form_json))
        forms.update({form_json.replace(".json", ""): json.load(f)})

    try:
        forms[FORMS_SERVICE_TEST_FORM]
    except KeyError:
        raise Exception(
            "Form "
            + FORMS_SERVICE_TEST_FORM
            + ".json does not exist at "
            + form_jsons_dir
            + ": Either add a valid form .json file at "
            + form_jsons_dir
            + " or set the environment variable"
            " FORMS_SERVICE_TEST_FORM "
            "to the name of a form that does exist here. "
            "Use the FORMS_SERVICE_TEST_PUBLIC_FORM environment switch "
            "to switch between the public or "
            "preview(default) form_jsons folders"
        )

    return forms


# test_form_pages = {
#     "/about-you": {
#         "fields": [
#             {"name": "applicant_name",
#              "label": "Applicant name",
#              "type": "text"
#              },
#         ]
#     },
# }

test_form_pages = get_test_form_routes()[FORMS_SERVICE_TEST_FORM]["pages"]


@pytest.mark.usefixtures("selenium_chrome_driver")
@pytest.mark.usefixtures("live_server")
class TestFormURLsWithChrome:
    def run_axe_print_and_return_results(self, route_rel):
        results = run_axe_and_print_report(
            self.driver,
            {"name": FORMS_SERVICE_NAME, "host": FORMS_SERVICE_HOST},
            route_rel,
        )
        return results

    def test_form_pages_accessible(self):
        """
        GIVEN Our FORM SERVICE Application is running
        at FORMS_SERVICE_HOST and the given
        FORMS_SERVICE_TEST_FORM has been created
        WHEN looping through the given test_form_pages
        THEN check that page returned conforms to WCAG standards
        """
        for page in test_form_pages:
            path = page["path"]
            route_rel = FORMS_SERVICE_TEST_FORM + path
            results = self.run_axe_print_and_return_results(route_rel)
            assert len(results["violations"]) <= 2
            # assert len(results["violations"]) == 0 or all(
            #     [v["impact"] == "minor" for v in results["violations"]]
            # )

    def test_form_pages_contain_expected_fields(self):
        """
        GIVEN FORM SERVICE Application is running
        at FORMS_SERVICE_HOST and the given
        FORMS_SERVICE_TEST_FORM has been created
        WHEN looping through the given test_form_pages
        THEN check each page contains expected TextFields
        """
        for page in test_form_pages:
            path = page["path"]
            form_attrs = page["components"]
            route_rel = "/" + FORMS_SERVICE_TEST_FORM + path
            url = FORMS_SERVICE_HOST + route_rel
            # print(url)
            # print(self.driver.page_source)
            self.driver.get(url=url)
            error_message = ""
            for component in form_attrs:
                found_input = None
                if component["type"] == "TextField":
                    try:
                        found_input = self.driver.find_element(
                            By.NAME, component["name"]
                        )
                    except NoSuchElementException:
                        error_message = (
                            "Component name '"
                            + component["name"]
                            + "' was not found in "
                            + url
                        )
                    assert found_input is not None, error_message

    # def test_insecure_form_post_returns_403(self):
    #     """
    #     GIVEN Our FORM SERVICE Application is running
    #     at FORMS_SERVICE_HOST and the given
    #     FORMS_SERVICE_TEST_FORM has been created
    #     WHEN testing the first given route in test_form_routes
    #     THEN check that an insecure form post returns 403
    #     """
    #     route = test_form_pages[0]
    #     path = route["path"]
    #     route_rel = "/" + FORMS_SERVICE_TEST_FORM + path
    #     url = FORMS_SERVICE_HOST + route_rel
    #     kwargs = {}
    #     # response = self.driver.requests(
    #     #     method="POST",
    #     #     url=url,
    #     #     kwargs=kwargs)
    #     data = parse.urlencode({"name": "Bad Data"}).encode()
    #     req = request.Request(url, data=data)
    #     response = request.urlopen(req)
    #     assert response.code == 403

    def test_unknown_forms_page_returns_accessible_404(self):
        """
        GIVEN Our FORM SERVICE Application is running
        at FORMS_SERVICE_HOST and the given
        WHEN the '/page-that-does-not-exist' page is requested (GET)
        on the FORM_SERVICE_HOST
        THEN check that a 404 page that is returned conforms to WCAG standards
        """
        route_rel = "page-does-not-exist"
        results = self.run_axe_print_and_return_results(route_rel)

        assert len(results["violations"]) <= 2
        # assert len(results["violations"]) == 0 or all(
        #     [viols["impact"] == "minor" for viols in results["violations"]]
        # )
