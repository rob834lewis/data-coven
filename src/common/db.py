# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 28MAY2026

    Purpose         : Database management

    Dependencies    :

    Program name    : db

    Modifications
    -------------
    28MAY2026   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

# ---------------
# --- Imports ---
# ---------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.common.config import config
from src.common.secrets import secrets


# -----------------
# --- Functions ---
# -----------------

_ENGINES = {}
_SESSIONMAKERS = {}


def build_postgres_url() -> str:
    """
    Build a PostgreSQL SQLAlchemy connection URL.

    Config values come from config().
    Secret values come from secrets().
    """

    config_data = config()
    secret_data = secrets()

    username = secret_data.get("db_user")
    password = secret_data.get("db_password")

    db_engine = config_data.get("db_engine")
    host = config_data.get("db_host")
    port = config_data.get("db_port")
    database = config_data.get("db_database")

    return (
        f"{db_engine}://"
        f"{username}:{password}@"
        f"{host}:{port}/"
        f"{database}"
    )


def get_engine(profile_name: str = "postgres.app"):
    """
    Return a cached SQLAlchemy engine.

    The profile_name is used as the cache key.
    """

    if profile_name in _ENGINES:
        return _ENGINES[profile_name]

    config_data = config()
    db_engine = config_data.get("db_engine")

    if db_engine.startswith("postgresql"):
        database_url = build_postgres_url()

        engine = create_engine(
            database_url
        )

    else:
        raise ValueError(
            f"Unsupported database engine: {db_engine}"
        )

    _ENGINES[profile_name] = engine

    return engine


def get_session(profile_name: str = "postgres.app"):
    """
    Return a new database session.

    The sessionmaker is cached.
    The session itself is new each time.
    """

    if profile_name not in _SESSIONMAKERS:
        engine = get_engine(
            profile_name
        )

        _SESSIONMAKERS[profile_name] = sessionmaker(
            bind=engine
        )

    return _SESSIONMAKERS[profile_name]()