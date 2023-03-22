# Translations

Updating translations:

    invoke pybabel-extract
    invoke pybabel-update
    invoke pybabel-compile

Update these commands in the `tasks.py` file if you need to change the source or output directories.

You can make sure you remove whitespace (will move it outside), newlines and tabs from an `.html` file by running:

    invoke fix-trans-tags --path=app/templates/your_file.html


If you resolve merge-conflicts, make sure to run compile again.

If you compile, make sure you've rebuilt your docker image if you can't see changes.
