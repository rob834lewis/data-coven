import os

# Flask imports
# Flask = main web application object
# render_template = loads HTML files from /templates
# request = reads information sent from forms
# redirect = sends user to another page
# url_for = builds URLs safely from route names
from flask import Flask, render_template, request, redirect, url_for

# Import game logic functions
from src.apps.financeferret.game_logic import (
    WEEKLY_ALLOWANCE,
    BIKE_GOAL,
    calculate_goal_progress,
    validate_money_allocation,
    get_random_event,
)

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash

from src.apps.financeferret.models import UserAccount

from src.common.env_loader import load_env

load_env()


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


# Create the Flask application
#
# __name__ tells Flask where this file lives
# Flask uses this to find:
# - templates/
# - static/
# - other resources
app = Flask(__name__)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

# @app.route() tells Flask:
#
# "When someone visits this URL,
# run the function underneath it"
#
# "/" means:
#
# http://localhost:5000/
#
# This is the root/home page
@app.route("/")
def home():

    # render_template loads HTML files
    #
    # Flask automatically looks inside:
    #
    # templates/index.html
    #
    return render_template("index.html")


# --------------------------------------------------
# START PAGE
# --------------------------------------------------

# methods tells Flask which HTTP actions
# this page accepts
#
# GET:
# User asks to VIEW data/page
#
# Browser:
# GET /start
#
# Example:
# User clicks:
# Start Game
#
# Flask returns the page
#
# POST:
# User SENDS data to server
#
# Example:
#
# Name field:
# Rob
#
# Browser sends:
#
# POST /start
# player_name=Rob
#
@app.route("/start", methods=["GET", "POST"])
def start():

    # request.method tells us which
    # type of HTTP request happened
    #
    # GET = show page
    # POST = process form data
    if request.method == "POST":

        # Get value from HTML form
        #
        # <input name="player_name">
        #
        # becomes:
        #
        # request.form["player_name"]
        #
        player_name = request.form.get(
            "player_name"
        )

        # redirect sends user elsewhere
        #
        # url_for("week")
        #
        # means:
        #
        # find route linked to:
        #
        # def week()
        #
        # Flask creates URL automatically
        #
        # Result:
        #
        # /week?player_name=Rob
        #
        return redirect(
            url_for(
                "week",
                player_name=player_name
            )
        )

    # If GET request:
    #
    # Show start screen
    return render_template(
        "start.html"
    )


# --------------------------------------------------
# GAME PAGE
# --------------------------------------------------

@app.route(
    "/week",
    methods=["GET", "POST"]
)
def week():

    player_name = request.args.get(
        "player_name",
        "Player"
    )

    spend = 0
    save = 0
    share = 0
    error = None

    if request.method == "POST":

        result = validate_money_allocation(
            request.form.get("spend", 0),
            request.form.get("save", 0),
            request.form.get("share", 0),
        )

        if result["is_valid"]:
            spend = result["spend"]
            save = result["save"]
            share = result["share"]
        else:
            error = result["error"]

    goal_progress = calculate_goal_progress(
        save,
        BIKE_GOAL["target"]
    )

    event = get_random_event()

    return render_template(
        "week.html",
        player_name=player_name,
        allowance=WEEKLY_ALLOWANCE,
        spend=spend,
        save=save,
        share=share,
        error=error,
        goal=BIKE_GOAL,
        goal_progress=goal_progress,
        event=event,
    )


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    # Read environment variable
    #
    # APP_ENV=dev
    #
    # returns True
    #
    # Anything else:
    # False
    #
    debug_mode = (
        os.getenv("APP_ENV")
        == "dev"
    )

    # Start local web server
    #
    # Default:
    #
    # http://127.0.0.1:5000
    #
    # debug=True means:
    #
    # - auto reload
    # - error messages
    # - developer tools
    #
    app.run(
        debug=debug_mode
    )
