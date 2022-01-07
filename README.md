# Funding service design frontend.

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


Repo for the funding service design frontend.

Built with Flask.

# Funding Service Design - Iteration 1
This is the first iteration of the Funding Service Design Beta application 

## Prerequisites
- python ^= 3.10
- poetry ^= 1.1.12

## Getting started

# Installation

### Locally:
Clone the repository

### Install Dependences

    poetry config virtualenvs.in-project true

    poetry install

### Create static files

    bash ./build.sh

### Enter the virtual environment

    poetry shell

## How to use
A requirements.txt is included for developer preference. Once you have
installed the dependences (poetry or otherwise), enter the virtual environment
and run:

    flask run

A local dev server will be created on 

    http://127.0.0.1:5000/

This is configurable in .flaskenv
