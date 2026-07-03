# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 28MAY2026

    Purpose         : Secrets management

    Dependencies    :

    Program name    : secrets

    Modifications
    -------------
    28MAY2026   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

import os
import configparser

from src.common.env_loader import load_env

# -----------------
# --- Functions ---
# -----------------


def secrets():

    # load environment variables from .env file
    load_env()

    env = os.environ.get("APP_ENV")

    # Create a ConfigParser instance
    config = configparser.ConfigParser()

    if env == "dev":

        # read in secrets path
        project_root = os.environ.get("PROJECT_ROOT")
        secrets_path = os.path.join(project_root, ".env", "secrets.ini")

        # Read the INI file
        config.read(secrets_path)

        # Access the username and password from the 'dev.postgres' section
        db_user = config.get("dev.postgres", "USERNAME")
        db_password = config.get("dev.postgres", "PASSWORD")

        # Read the flask secret key from the 'dev.flask' section
        flask_secret_key = config.get("dev.flask", "SECRET_KEY")

    return {
        "db_user": db_user,
        "db_password": db_password,
        "flask_secret_key": flask_secret_key,
    }
