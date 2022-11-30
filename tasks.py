import os
import re

from invoke import task

_VALID_JINJA_EXTENSIONS = (".html", ".jinja", ".jinja2", ".j2")


def _remove_whitespace_newlines_from_trans_tags(content: str):
    matches = re.findall(
        r"({%\s*trans\s*%}(.|[\S\s]*?){%\s*endtrans\s*%})", content
    )

    content_replaced = content
    for outer, center in matches:
        normalised_whitespace_trans = re.sub(r"\s+", " ", center).strip()

        outer_replaced = outer.replace(center, normalised_whitespace_trans)

        rwhitespace = center[len(center.rstrip()) :]  # noqa: E203
        lwhitespace = center[: len(center) - len(center.lstrip())]

        outer_replaced_whitespace = lwhitespace + outer_replaced + rwhitespace
        content_replaced = content_replaced.replace(
            outer, outer_replaced_whitespace
        )

    return content_replaced


def _process_file(file: str):
    with open(file, "r") as f:
        content = f.read()

    content_replaced = _remove_whitespace_newlines_from_trans_tags(content)

    if content != content_replaced:
        with open(file, "w") as f:
            f.write(content_replaced)
        print(f"Removed newlines/tabs from {file}")
    else:
        print(f"No newlines/tabs to remove from {file}")

    return 0


@task
def fix_trans_tags(_, path="app/templates"):
    ret = 0

    if os.name == "nt":
        path = path.replace("/", "\\")

    filepath = os.path.join(os.getcwd(), path)
    if os.path.isfile(filepath) and filepath.endswith(_VALID_JINJA_EXTENSIONS):
        ret |= _process_file(filepath)

    for _, _, files in os.walk(filepath):
        for file in files:
            full_filepath = os.path.join(filepath, file)
            if file.endswith(_VALID_JINJA_EXTENSIONS):
                ret |= _process_file(full_filepath)

    return ret


@task
def pybabel_extract(c):
    c.run("pybabel extract -F babel.cfg -o messages.pot .")


@task
def pybabel_update(c):
    c.run("pybabel update -i messages.pot -d app/translations")


@task
def pybabel_compile(c):
    c.run("pybabel compile -d app/translations")
