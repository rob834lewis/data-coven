# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 28MAY2026

    Purpose         : Configuration management

    Dependencies    :

    Program name    : config

    Modifications
    -------------
    28MAY2026   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

import os, configparser

from src.common.env_loader import load_env

# -----------------
# --- Functions ---
# -----------------

def config():

    # load environment variables from .env file
    load_env()

    env = os.environ.get("APP_ENV")

    # Create a ConfigParser instance
    config = configparser.ConfigParser()

    if env == "dev":

        # read in config path
        project_root = os.environ.get("PROJECT_ROOT")
        config_path = os.path.join(project_root, "config", "config.ini")

        # Read the INI file
        config.read(config_path)

        # Access the username and password from the 'dev.postgres' section
        db_engine = config.get('dev.postgres', 'ENGINE')
        db_host = config.get('dev.postgres', 'HOST')
        db_port = config.get('dev.postgres', 'PORT')
        db_database = config.get('dev.postgres', 'DATABASE')

    return {
        "db_engine": db_engine,
        "db_host": db_host,
        "db_port": db_port,
        "db_database": db_database
    }