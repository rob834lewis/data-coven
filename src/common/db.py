from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.common.config import get_connection_profile
from src.common.secrets import get_secret


_ENGINES = {}
_SESSIONMAKERS = {}


def build_postgres_url(profile: dict) -> str:
    password = get_secret(
        profile["PASSWORD_SECRET"]
    )

    return (
        f"{profile['ENGINE']}://"
        f"{profile['USERNAME']}:{password}@"
        f"{profile['HOST']}:{profile['PORT']}/"
        f"{profile['DATABASE']}"
    )


def get_engine(profile_name: str):
    if profile_name in _ENGINES:
        return _ENGINES[profile_name]

    profile = get_connection_profile(
        profile_name
    )

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