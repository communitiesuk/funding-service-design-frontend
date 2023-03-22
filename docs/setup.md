# Set-up Service

## **Prerequisites**

### Python version
- See requirements.in file

### Flask version
- See requirements.in file

### Contributor tooling
This repo comes with a .pre-commit-config.yaml, you will have autoformatting and pep8 compliance built into your workflow.

You will be notified of any pep8 errors during commits.


## **Clone the repository**

### Create a Virtual environment

    python3 -m venv .venv

### Enter the virtual environment

...either macOS using bash:

    source .venv/bin/activate

...or if on Windows using Command Prompt:

    .venv\Scripts\activate.bat

## **Install dependencies**

requirements-dev.txt and requirements.txt are updated using [pip-tools pip-compile](https://github.com/jazzband/pip-tools)
To update requirements please manually add the dependencies in the .in files (not the requirements.txt files)
Then run (in the following order):

    pip-compile requirements.in

    pip-compile requirements-dev.in

From the top-level directory enter the command to install pip and the dependencies of the project

    python3 -m pip install --upgrade pip && pip install -r requirements-dev.txt


## **Create static files**

Download and extract the static files by running:

    python3 build.py

Developer note: If you receive a certification error when running the above command on macOS,
consider if you need to run the Python
'Install Certificates.command' which is a file located in your globally installed Python directory. For more info see [StackOverflow](https://stackoverflow.com/questions/52805115/certificate-verify-failed-unable-to-get-local-issuer-certificate)
