# --------------------------------------------------
# POCKETQUEST GAME LOGIC
# --------------------------------------------------
#
# This file contains the rules of the game.
#
# The Flask app should handle web pages, forms and routes.
# This file should handle game/business rules.
#
# In data terms:
#
# app.py       = orchestration / interface layer
# game_logic.py = validation / transformation layer
# templates   = presentation layer


# Weekly pocket money amount for the player.
#
# Keeping this as a constant means we can reuse it
# across the app without hard-coding 20 everywhere.
WEEKLY_ALLOWANCE = 20


def validate_money_allocation(spend_raw, save_raw, share_raw, allowance):
    """
    Validate how the player splits their weekly money.

    Parameters
    ----------
    spend_raw:
        Raw value from the form for Spend.

    save_raw:
        Raw value from the form for Save.

    share_raw:
        Raw value from the form for Share.

    allowance:
        The total weekly allowance available for allocation.

    These values are "raw" because data from an HTML form
    arrives as text, even if the input type is number.

    Example:
        User enters 5

    Flask receives:
        "5"

    Returns
    -------
    dict
        A result dictionary containing:

        is_valid:
            True or False

        error:
            Error message if invalid, otherwise None

        spend/save/share:
            Clean integer values

        total_allocated:
            Total amount allocated across the three pots
    """

    # Create default result.
    #
    # This gives us a predictable return structure.
    # The route can always expect these keys to exist.
    result = {
        "is_valid": False,
        "error": None,
        "spend": 0,
        "save": 0,
        "share": 0,
        "total_allocated": 0,
    }

    # --------------------------------------------------
    # VALIDATION 1: TYPE CHECKING
    # --------------------------------------------------
    #
    # HTML form values arrive as strings.
    #
    # Example:
    #
    # "10"
    #
    # We need to convert them into integers before doing
    # maths with them.
    #
    # If someone sends "banana", int("banana") fails.
    # The try/except prevents the whole app crashing.
    try:
        spend = int(spend_raw)
        save = int(save_raw)
        share = int(share_raw)

    except ValueError:
        result["error"] = "Only whole numbers can be entered."
        return result

    # --------------------------------------------------
    # VALIDATION 2: NEGATIVE VALUES
    # --------------------------------------------------
    #
    # A player should not be able to allocate:
    #
    # Spend = -10
    #
    # because that would let them cheat the totals.
    if spend < 0 or save < 0 or share < 0:
        result["error"] = "Money values cannot be negative."
        return result

    # --------------------------------------------------
    # VALIDATION 3: ALLOWANCE LIMIT
    # --------------------------------------------------
    #
    # Add the three pots together.
    total_allocated = spend + save + share

    # The player only has WEEKLY_ALLOWANCE available.
    #
    # If they allocate more than that, reject the input.
    if total_allocated > allowance:
        result["error"] = (
            f"You only have £{allowance}. " f"You tried to use £{total_allocated}."
        )
        return result

    # --------------------------------------------------
    # SUCCESS
    # --------------------------------------------------
    #
    # If we get this far, all rules passed.
    result["is_valid"] = True
    result["spend"] = spend
    result["save"] = save
    result["share"] = share
    result["total_allocated"] = total_allocated

    return result


BIKE_GOAL = {
    "name": "Bike",
    "target": 50,
}


def calculate_goal_progress(saved_amount, goal_target):
    """
    Work out how much progress the player has made
    towards a savings goal.
    """

    progress_percent = int((saved_amount / goal_target) * 100)

    return min(progress_percent, 100)


# --------------------------------------------------
# RANDOM EVENTS
# --------------------------------------------------

RANDOM_EVENTS = [
    {
        "name": "School trip",
        "cost": 8,
        "message": "A school trip is coming up. It costs £8.",
    }
]


def get_random_event():
    """
    Return one event for the week.

    For now this is deliberately simple.
    Later we can use random.choice() when we have
    several possible events.
    """

    return RANDOM_EVENTS[0]
