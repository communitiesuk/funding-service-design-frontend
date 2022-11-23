# Translations

Updating translations:

    pybabel extract -F babel.cfg -o messages.pot .
    pybabel update -i messages.pot -d app/translations
    pybabel compile -d app/translations

Note: If you resolve merge-conflicts, make sure to run compile again.
