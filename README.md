# Funding service design frontend.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


Repo for the funding service design frontend.

Built with Flask.

## Prerequisites
- python ^= 3.10
- poetry ^= 1.1.12 (brew install poetry)

# Getting started

## Installation

### Locally:
Clone the repository

### Start a Virtual environment

    python -m venv venv

### Install dependencies
From the top-level directory enter the command to install pip and the dependencies of the project

    python -m pip install --upgrade pip && pip install -r requirements.txt

### Create static files

    python build.py

## How to use
A requirements.txt is included for developer preference. Once you have
installed the dependences (poetry or otherwise), enter the virtual environment
and run:

    flask run

A local dev server will be created on 

    http://127.0.0.1:5000/

This is configurable in .flaskenv
