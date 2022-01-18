# Funding service design frontend.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

![Funding Service Design Frontend Deploy](https://github.com/communitiesuk/funding-service-design-frontend/actions/workflows/govcloud.yml/badge.svg)

[![CodeQL](https://github.com/communitiesuk/funding-service-design-frontend/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/communitiesuk/funding-service-design-frontend/actions/workflows/codeql-analysis.yml)

Repo for the funding service design frontend.

Built with Flask.

## Prerequisites
- python ^= 3.10

# Getting started

## Installation

Clone the repository

### Create a Virtual environment

    python3 -m venv .venv

### Enter the virtual environment

...either macOS using bash:

    source .venv/bin/activate

...or if on Windows using Command Prompt:

    .venv\Scripts\activate.bat

### Install dependencies
From the top-level directory enter the command to install pip and the dependencies of the project

    python3 -m pip install --upgrade pip && pip install -r requirements.txt

## How to use
Enter the virtual environment as described above, then:

### Create static files

    python build.py

Developer note: If you receive a certification error when running the above command on macOS,
consider if you need to run the Python
'Install Certificates.command' which is a file located in your globally installed Python directory. For more info see [StackOverflow](https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate)

Then run:

    flask run

A local dev server will be created on

    http://127.0.0.1:5000/

This is configurable in .flaskenv

You should see the following:

![Preview of the end result](https://user-images.githubusercontent.com/56394038/148535451-469d8fa4-2354-47a0-9d71-1052bfae78c4.png)

# Pipelines

Place birief descriptions of Pipelines here

* Deploy to Gov PaaS - This is a simple pipeline to demonstrate capabilities.  Builds, tests and deploys a simple python application to the PaaS for evaluation in Dev and Test Only.

# Testing

Made your changes and ready to test? Run the following in your venv:

    pytest

Make sure that pytest is installed (it is included in requirements.txt) or
this will not work.

# Performance Testing

Performance tests are stored in a separate repository which is then run in the pipeline. If you want to run the performance tests yourslef follow the steps in the README for the performance test repo located [here](https://github.com/communitiesuk/funding-service-design-performance-tests/blob/main/README.md)

# Extras

This repo comes with a .pre-commot-config.yaml, if you wish to use this do
the following while in your virtual enviroment:

    pip install pre-commit black

    pre-commit install

Once the above is done you will have autoformatting and pep8 compliance built
into your workflow. You will be notified of any pep8 errors during commits.
