"""
Tests if pages of the FORMS_SERVICE_PUBLIC_HOST
and FORMS_SERVICE_PREVIEW_HOST
are accessible according to WCAG standards

The form .json files should be placed in either the
'public' or 'preview' folders beneath the
FORM_SERVICE_JSONS_PATH

These tests have been designed to test .json
schema generated by the XGov Forms Builder.
Examples of the latest schema can be found at:
https://github.com/XGovFormBuilder/digital-form-builder/tree/main/runner/src/server/forms
"""
import fnmatch
import json
import os

import pytest
from config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.errorhandler import NoSuchElementException
from tests.test_accessibility import run_axe_and_print_report
from tests.utils import print_html_page


@pytest.mark.usefixtures("selenium_chrome_driver")
@pytest.mark.usefixtures("live_server")
class TestFormURLsWithChrome:
    form_dirs = ["public", "preview"]

    @staticmethod
    def get_form_service_host(form_dir):
        host = Config.FORMS_SERVICE_PUBLIC_HOST
        if form_dir == "preview":
            host = Config.FORMS_SERVICE_PREVIEW_HOST
        return host

    def get_test_form_pages(self):
        form_pages = []
        for form_dir, forms in self.get_test_forms().items():
            for form_name, form_json in forms.items():
                pages = form_json["pages"]
                form_pages.append((form_dir, form_name, pages))
        return form_pages

    def get_test_forms(self):
        forms = {}
        for form_dir in self.form_dirs:
            form_jsons_dir = os.path.join(
                ".", Config.FORMS_SERVICE_JSONS_PATH, form_dir
            )
            form_jsons = fnmatch.filter(os.listdir(form_jsons_dir), "*.json")
            forms.update({form_dir: {}})
            for form_json in form_jsons:
                f = open(os.path.join(form_jsons_dir, form_json))
                forms[form_dir].update(
                    {form_json.replace(".json", ""): json.load(f)}
                )

        if all([dir_forms == {} for form_dir, dir_forms in forms.items()]):
            raise Exception(
                "No form .json files exist at "
                + str(
                    ", ".join(
                        [
                            "/".join(
                                [Config.FORMS_SERVICE_JSONS_PATH, form_dir]
                            )
                            for form_dir in self.form_dirs
                        ]
                    )
                )
                + ". Please add one or more .json form"
                " files here to test against."
            )
        return forms

    def run_axe_print_and_return_results(self, service, route_rel):
        results = run_axe_and_print_report(
            driver=self.driver,
            service_dict=service,
            route_rel=route_rel,
        )
        return results

    def test_form_pages_accessible(self):
        """
        GIVEN Our FORM SERVICE Application is running
        WHEN looping through the given test_form_pages
        THEN check that page returned conforms to WCAG standards
        """
        for form_dir, form_name, pages in self.get_test_form_pages():
            for page in pages:
                path = page["path"]
                route_rel = form_name + path
                results = self.run_axe_print_and_return_results(
                    {
                        "name": Config.FORMS_SERVICE_NAME,
                        "host": self.get_form_service_host(form_dir),
                    },
                    route_rel,
                )
                assert len(results["violations"]) <= 4
                assert len(results["violations"]) <= 4 or all(
                    [
                        viols["impact"] not in ["serious", "critical"]
                        for viols in results["violations"]
                    ]
                )

    def test_form_pages_contain_expected_fields(self):
        """
        GIVEN FORM SERVICE Application is running
        WHEN looping through the given test_form_pages
        THEN check each page contains expected TextFields
        """
        for form_dir, form_name, pages in self.get_test_form_pages():
            for page in pages:
                path = page["path"]
                form_attrs = page["components"]
                route_rel = "/" + form_name + path
                url = self.get_form_service_host(form_dir) + route_rel
                self.driver.get(url=url)
                source = self.driver.page_source
                print_html_page(
                    html=source,
                    service_dict={
                        "name": Config.FORMS_SERVICE_NAME,
                        "host": self.get_form_service_host(form_dir),
                    },
                    route_rel=route_rel,
                )
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

    def test_unknown_forms_page_on_public_host_returns_accessible_404(self):
        """
        GIVEN Our FORM SERVICE Application is running
        WHEN the '/page-that-does-not-exist' page is requested (GET)
        THEN check that a 404 page that is returned conforms to WCAG standards
        """
        route_rel = "page-does-not-exist"
        results = self.run_axe_print_and_return_results(
            {
                "name": Config.FORMS_SERVICE_NAME,
                "host": self.get_form_service_host("public"),
            },
            route_rel,
        )

        assert len(results["violations"]) <= 2
        assert len(results["violations"]) == 0 or all(
            [
                viols["impact"] not in ["serious", "critical"]
                for viols in results["violations"]
            ]
        )

    # TODO: Ensure that CSRF Protection is available on the Forms Service
    # def test_insecure_form_post_returns_403(self):
    #     """
    #     GIVEN Our FORM SERVICE Application is running
    #     WHEN testing the first given route in test_form_routes
    #     THEN check that an insecure form post returns 403
    #     """
    #     for form_dir, form_name, pages in self.get_test_form_pages():
    #         for page in pages:
    #             path = page["path"]
    #             route_rel = "/" + form_name + path
    #             url = self.get_form_service_host(form_dir) + route_rel
    #             data = parse.urlencode({"name": "Bad Data"}).encode()
    #             req = request.Request(url, data=data)
    #             try:
    #                 response = request.urlopen(req)
    #                 response_code = response.code
    #             except HTTPError as err:
    #                 response_code = err.code
    #             assert response_code == 403
