def datetime_format(value, format="%d/%m/%y"):
    return value.strftime(format)


def snake_case_to_human(word):
    if word:
        return word.replace("_", " ").title()


def kebab_case_to_human(word):
    if word:
        return word.replace("-", " ").title()
