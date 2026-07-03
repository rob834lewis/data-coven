from src.apps.financeferret.child_logic import validate_child_form


def test_child_name_is_required():
    result = validate_child_form("", "10")

    assert result["is_valid"] is False
    assert result["error"] == "Child name is required."


def test_age_is_required():
    result = validate_child_form("Jane", "")

    assert result["is_valid"] is False
    assert result["error"] == "Age is required."


def test_age_must_be_number():
    result = validate_child_form("Emily", "banana")

    assert result["is_valid"] is False
    assert result["error"] == "Age must be a whole number."


def test_age_must_be_greater_than_1():
    result = validate_child_form("Emily", "-1")

    assert result["is_valid"] is False
    assert result["error"] == "Age must be between 1 and 18."


def test_age_must_be_less_than_19():
    result = validate_child_form("Emily", "19")

    assert result["is_valid"] is False
    assert result["error"] == "Age must be between 1 and 18."


def test_valid_child_form():
    result = validate_child_form("Emily", "9")

    assert result["is_valid"] is True
    assert result["age"] == 9
