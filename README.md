# Funding service design frontend.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


Repo for the funding service design frontend.

Built with Flask.

## Prerequisites
- python ^= 3.10

# Getting started

## Installation

### Locally:
Clone the repository

### Start a Virtual environment

    python3 -m venv venv

### Install dependencies
From the top-level directory enter the command to install pip and the dependencies of the project

    python3 -m pip install --upgrade pip && pip install -r requirements.txt

## How to use

###Enter the virtual environment

...either macOS using bash:

    source venv/bin/activate

...or if on Windows using Command Prompt:

    venv\Scripts\activate.bat

### Create static files

    python build.py
Then run:

    flask run

A local dev server will be created on 

    http://127.0.0.1:5000/

This is configurable in .flaskenv
