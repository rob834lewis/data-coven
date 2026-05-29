# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 29MAY2026

    Purpose         : Initialise database

    Dependencies    :

    Program name    : init_db

    Modifications
    -------------
    29MAY2026   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from sqlalchemy import text

from src.apps.financeferret.models import Base

from src.common.db import get_engine

engine = get_engine()

# Create the missing database tables, look into Alembic migrations for updating existing tables

with engine.begin() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS financeferret"))
    Base.metadata.create_all(connection)

