# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 25MAY2026

    Purpose         : Finance Ferret web application

    Dependencies    :

    Program name    : app

    Modifications
    -------------
    25MAY2026   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

import os

from flask import Flask, render_template, request, redirect, url_for, session

# Import game logic functions
from src.apps.financeferret.game_logic import (
    validate_money_allocation,
    get_random_event,
)

from sqlalchemy.exc import IntegrityError

from werkzeug.security import generate_password_hash, check_password_hash

from src.apps.financeferret.models import UserAccount, ChildProfile, WeeklyAllocation

from src.common.env_loader import load_env
from src.common.db import get_session
from src.apps.financeferret.child_logic import validate_child_form
from src.common.secrets import secrets

# ----------------
# --- Main App ---
# ----------------

# load environment variables from .env file
load_env()

# Create Flask app instance
app = Flask(__name__)

# Set secret key for session management - in production, this should be a secure random value stored in an environment variable or secrets manager
secret_data = secrets()

app.secret_key = secret_data.get("flask_secret_key")

# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------


@app.route("/")
def home():

    username = session.get("username")

    child_name = session.get("active_child_name")

    return render_template("index.html", username=username, child_name=child_name)


# --------------------------------------------------
# START PAGE
# --------------------------------------------------


@app.route("/start", methods=["GET", "POST"])
def start():

    if request.method == "POST":

        player_name = request.form.get("player_name")

        return redirect(url_for("week", player_name=player_name))

    return render_template("start.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    error = None

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        password_hash = generate_password_hash(password)

        new_user = UserAccount(
            username=username, email=email, password_hash=password_hash
        )

        db_session = get_session()

        try:
            db_session.add(new_user)
            db_session.commit()

            return redirect(url_for("home"))

        except IntegrityError:
            db_session.rollback()

            error = "That username or email is already registered."

        finally:
            db_session.close()

    return render_template("register.html", error=error)


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

            elif not check_password_hash(user.password_hash, password):
                error = "Username/email or password is incorrect."

            else:
                session["user_id"] = user.id
                session["username"] = user.username

                return redirect(url_for("home"))

        finally:
            db_session.close()

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


@app.route("/add-child", methods=["GET", "POST"])
def add_child():

    if "user_id" not in session:
        return redirect(url_for("login"))

    error = None

    if request.method == "POST":

        child_name = request.form.get("child_name")
        age_raw = request.form.get("age")

        validation = validate_child_form(
            child_name,
            age_raw,
        )

        if not validation["is_valid"]:
            error = validation["error"]

            return render_template("add_child.html", error=error)

        age = validation["age"]

        db_session = get_session()

        try:
            child = ChildProfile(
                user_id=session["user_id"], child_name=child_name, age=age
            )

            db_session.add(child)
            db_session.commit()

            return redirect(url_for("home"))

        finally:
            db_session.close()

    return render_template("add_child.html", error=error)


@app.route("/select-child", methods=["GET", "POST"])
def select_child():

    if "user_id" not in session:
        return redirect(url_for("login"))

    error = None
    db_session = get_session()

    try:
        if request.method == "POST":

            child_id = request.form.get("child_id")

            child = (
                db_session.query(ChildProfile)
                .filter_by(id=child_id, user_id=session["user_id"])
                .first()
            )

            if child is None:
                error = "Child profile not found."

            else:
                session["active_child_id"] = child.id
                session["active_child_name"] = child.child_name

                return redirect(url_for("home"))

        children = (
            db_session.query(ChildProfile).filter_by(user_id=session["user_id"]).all()
        )

    finally:
        db_session.close()

    return render_template("select_child.html", children=children, error=error)


@app.route("/child-settings", methods=["GET", "POST"])
def child_settings():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if "active_child_id" not in session:
        return redirect(url_for("select_child"))

    error = None
    success = None

    db_session = get_session()

    try:
        child = (
            db_session.query(ChildProfile)
            .filter_by(
                id=session["active_child_id"],
                user_id=session["user_id"],
            )
            .first()
        )

        if child is None:
            session.pop("active_child_id", None)
            session.pop("active_child_name", None)

            return redirect(url_for("select_child"))

        if request.method == "POST":

            allowance_raw = request.form.get("weekly_allowance")

            try:
                weekly_allowance = int(allowance_raw)

            except ValueError:
                error = "Weekly pocket money must be a whole number."

            else:
                if weekly_allowance < 0:
                    error = "Weekly pocket money cannot be negative."

                else:
                    child.weekly_allowance = weekly_allowance
                    db_session.commit()

                    session["active_child_name"] = child.child_name

                    success = "Settings saved."

        child_data = {
            "id": child.id,
            "child_name": child.child_name,
            "weekly_allowance": child.weekly_allowance,
        }

    finally:
        db_session.close()

    return render_template(
        "child_settings.html",
        child=child_data,
        error=error,
        success=success,
    )


# --------------------------------------------------
# GAME PAGE
# --------------------------------------------------


@app.route("/weekly_allocation", methods=["GET", "POST"])
def weekly_allocation():

    if "user_id" not in session:
        return redirect(url_for("login"))

    if "active_child_id" not in session:
        return redirect(url_for("select_child"))

    error = None
    success = None
    event = get_random_event()

    db_session = get_session()

    try:
        child = (
            db_session.query(ChildProfile)
            .filter_by(
                id=session["active_child_id"],
                user_id=session["user_id"],
            )
            .first()
        )

        if child is None:
            session.pop("active_child_id", None)
            session.pop("active_child_name", None)
            return redirect(url_for("select_child"))

        latest_allocation = (
            db_session.query(WeeklyAllocation)
            .filter_by(child_id=child.id)
            .order_by(WeeklyAllocation.week_number.desc())
            .first()
        )

        if latest_allocation is None:
            week_number = 1
            allocation = None
        else:
            week_number = latest_allocation.week_number + 1
            allocation = latest_allocation

        if request.method == "POST":

            result = validate_money_allocation(
                request.form.get("spend", 0),
                request.form.get("save", 0),
                request.form.get("share", 0),
                allowance=child.weekly_allowance,
            )

            if not result["is_valid"]:
                error = result["error"]

            else:
                new_allocation = WeeklyAllocation(
                    child_id=child.id,
                    week_number=week_number,
                    allowance=child.weekly_allowance,
                    spend=result["spend"],
                    save=result["save"],
                    share=result["share"],
                )

                db_session.add(new_allocation)
                db_session.commit()

                success = "Weekly allocation saved."

                allocation = new_allocation
                week_number = new_allocation.week_number

        child_data = {
            "id": child.id,
            "child_name": child.child_name,
            "weekly_allowance": child.weekly_allowance,
        }

        allocation_data = None

        if allocation is not None:
            allocation_data = {
                "week_number": allocation.week_number,
                "allowance": allocation.allowance,
                "spend": allocation.spend,
                "save": allocation.save,
                "share": allocation.share,
            }

    finally:
        db_session.close()

    return render_template(
        "weekly_allocation.html",
        child=child_data,
        week_number=week_number,
        allocation=allocation_data,
        event=event,
        error=error,
        success=success,
    )


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    debug_mode = os.getenv("APP_ENV") == "dev"

    app.run(debug=debug_mode)
