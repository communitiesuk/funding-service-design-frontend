# Translations
The pybabel commands we need are pre-defined in `tasks.py` - update these definitions if you need to change input or output paths.

## Updating translations:

1. Edit html pages etc with new text (use `{% trans %}Here is some text{% endtrans %}` tags to indicate translatable text).
2. Run extract to update the `messages.pot` file with new strings

    invoke pybabel-extract

3. Run update to update the `messages.po` file(s) with the new strings

    invoke pybabel-update

4. Update `messages.po` with the translations for the new strings
5. Run compile to make these strings accessible at runtime

    invoke pybabel-compile

6. Test! Put the app into welsh mode and check everything displays correctly (and check forms are navigable through all branches)

## Troubleshoorting

### Whitespace
Whitespace (new lines etc) needs to be outside the translations for it to work properly.

You can make sure you remove whitespace (will move it outside), newlines and tabs from an `.html` file by running:

    invoke fix-trans-tags --path=app/templates/your_file.html

### Merge conflicts
If you resolve merge-conflicts, make sure to run compile again.

### Can't see changes?
* Make sure you've run `compile` after adding translations
* If you compile, make sure you've rebuilt your docker image if you can't see changes.
