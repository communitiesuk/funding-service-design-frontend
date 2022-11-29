import os
import re

from invoke import task

_VALID_JINJA_EXTENSIONS = (".html", ".jinja", ".jinja2", ".j2")


def remove_whitespace_newlines_from_trans_tags(file):
    with open(file, "r") as f:
        content = f.read()

    matches = re.findall(
        r"({%\s*trans\s*%}(\s*)(.*|[\S\s]*)(\s*){%\s*endtrans\s*%})", content
    )
    for outer, lwhitespace, _, rwhitespace in matches:
        no_newline_or_tabs_trans = outer.replace("\n", "").replace("\t", "")
        normalised_whitespace_trans = re.sub(
            r"\s+", " ", no_newline_or_tabs_trans
        )
        content_preserved_whitespace = (
            f"{lwhitespace}{normalised_whitespace_trans}{rwhitespace}"
        )
        content_replaced = content.replace(outer, content_preserved_whitespace)

    if content != content_replaced:
        with open(file, "w") as f:
            f.write(content_replaced)
        print(f"Removed newlines/tabs from {file}")
    else:
        print(f"No newlines/tabs to remove from {file}")


@task
def fix_trans_tags(_, path="app/templates"):
    if os.name == "nt":
        path = path.replace("/", "\\")

    filepath = os.path.join(os.getcwd(), path)
    if os.path.isfile(filepath) and filepath.endswith(_VALID_JINJA_EXTENSIONS):
        remove_whitespace_newlines_from_trans_tags(filepath)

    for _, _, files in os.walk(filepath):
        for file in files:
            full_filepath = os.path.join(filepath, file)
            if file.endswith(_VALID_JINJA_EXTENSIONS):
                remove_whitespace_newlines_from_trans_tags(full_filepath)


@task
def pybabel_extract(c):
    c.run("pybabel extract -F babel.cfg -o messages.pot .")


@task
def pybabel_update(c):
    c.run("pybabel update -i messages.pot -d app/translations")


@task
def pybabel_compile(c):
    c.run("pybabel compile -d app/translations")
