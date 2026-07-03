# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 29MAY2026

    Purpose         : Validate child form data

    Dependencies    :

    Program name    : child_logic

    Modifications
    -------------
    29MAY2026   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""


def validate_child_form(
    child_name,
    age_raw,
) -> dict:

    if not child_name:
        return {
            "is_valid": False,
            "error": "Child name is required.",
            "age": None,
        }

    if not age_raw:
        return {
            "is_valid": False,
            "error": "Age is required.",
            "age": None,
        }

    try:
        age = int(age_raw)

    except ValueError:

        return {
            "is_valid": False,
            "error": "Age must be a whole number.",
            "age": None,
        }

    if age < 1 or age > 18:

        return {
            "is_valid": False,
            "error": "Age must be between 1 and 18.",
            "age": None,
        }

    return {
        "is_valid": True,
        "error": None,
        "age": age,
    }
