import re


def use_regex(input_text):
    pattern = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+", re.IGNORECASE)
    return pattern.match(input_text)


def validate_class_name(name):
    return validate_nospace(name.replace("'", "").replace("-", "").title())


def validate_nospace(name):
    return name.replace(" ", "").replace("\"", "")


def validate_general_string(string):
    return string.replace("\"", "\\\"")