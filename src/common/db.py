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


_ENGINES = {}
_SESSIONMAKERS = {}


def build_postgres_url(profile: dict) -> str:
    secret_data = secrets()
    profile = config()

    username = secret_data.get("db_user")
    password = secret_data.get("db_password")

    engine = profile.get("db_engine")
    host = profile.get("db_host")
    port = profile.get("db_port")
    database = profile.get("db_database")

    return (
        f"{engine}://"
        f"{username}:{password}@"
        f"{host}:{port}/"
        f"{database}"
    )


def get_engine(profile_name: str):
    if profile_name in _ENGINES:
        return _ENGINES[profile_name]

    if profile["ENGINE"].startswith("postgresql"):
        database_url = build_postgres_url(
            profile
        )

        engine = create_engine(
            database_url
        )

    else:
        raise ValueError(
            f"Unsupported database engine: {profile['ENGINE']}"
        )

    _ENGINES[profile_name] = engine

    return engine


def get_session(profile_name: str):
    if profile_name not in _SESSIONMAKERS:
        engine = get_engine(
            profile_name
        )

        _SESSIONMAKERS[profile_name] = sessionmaker(
            bind=engine
        )

    return _SESSIONMAKERS[profile_name]()