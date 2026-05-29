import os

# Flask imports
# Flask = main web application object
# render_template = loads HTML files from /templates
# request = reads information sent from forms
# redirect = sends user to another page
# url_for = builds URLs safely from route names
from flask import Flask, render_template, request, redirect, url_for, session

# Import game logic functions
from src.apps.financeferret.game_logic import (
    WEEKLY_ALLOWANCE,
    BIKE_GOAL,
    calculate_goal_progress,
    validate_money_allocation,
    get_random_event,
)

from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

from src.apps.financeferret.models import UserAccount, ChildProfile



from src.common.env_loader import load_env

load_env()


#from src.common.db import get_engine

from src.common.db import get_session

#engine = get_engine()

#Session = sessionmaker(bind=engine)


# Create the Flask application
#
# __name__ tells Flask where this file lives
# Flask uses this to find:
# - templates/
# - static/
# - other resources
app = Flask(__name__)

app.secret_key = "dev-secret-key"



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

    username = session.get(
        "username"
    )

    return render_template(
        "index.html",
        username=username
    )


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


@app.route("/register", methods=["GET", "POST"])
def register():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        password_hash = generate_password_hash(
            password
        )

        new_user = UserAccount(
            username=username,
            email=email,
            password_hash=password_hash
        )

        db_session = get_session()

        try:
            db_session.add(new_user)
            db_session.commit()

            return redirect(
                url_for("home")
            )

        except IntegrityError:
            db_session.rollback()

            error = (
                "That username or email is already registered."
            )

        finally:
            db_session.close()

    return render_template(
        "register.html",
        error=error
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        login_value = request.form.get("login")
        password = request.form.get("password")

        db_session = get_session()

        try:
            user = (
                db_session.query(UserAccount)
                .filter(
                    (UserAccount.username == login_value)
                    | (UserAccount.email == login_value)
                )
                .first()
            )

            if user is None:
                error = "Username/email or password is incorrect."

            elif not check_password_hash(
                user.password_hash,
                password
            ):
                error = "Username/email or password is incorrect."

            else:
                session["user_id"] = user.id
                session["username"] = user.username

                return redirect(
                    url_for("home")
                )

        finally:
            db_session.close()

    return render_template(
        "login.html",
        error=error
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("home")
    )

@app.route("/add-child", methods=["GET", "POST"])
def add_child():

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    error = None

    if request.method == "POST":

        child_name = request.form.get("child_name")
        age_raw = request.form.get("age")

        if not child_name:
            error = "Child name is required."

        else:
            age = None

            if age_raw:
                age = int(age_raw)

            db_session = get_session()

            try:
                child = ChildProfile(
                    user_id=session["user_id"],
                    child_name=child_name,
                    age=age
                )

                db_session.add(child)
                db_session.commit()

                return redirect(
                    url_for("home")
                )

            finally:
                db_session.close()

    return render_template(
        "add_child.html",
        error=error
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
