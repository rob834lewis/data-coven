# -*- coding: utf-8 -*-
"""
---------------------------------------------------------------------------------------------------
    Written by      : Rob Lewis

    Date            : 28MAY2026

    Purpose         : Environment variable loading

    Dependencies    :

    Program name    : env_loader

    Modifications
    -------------
    28MAY2026   RLEWIS  Initial Version
---------------------------------------------------------------------------------------------------
"""

import socket
import os


ENVIRONMENTS = {

    "Lappy": {
        "APP_ENV": "dev",
        "SECRET_BACKEND": "local",
        "DATABASE_BACKEND": "sqlite",
        "PROJECT_ROOT": "C:\\Users\\Mr_Vo\\Documents\\Python\\projects\\data-coven",
    },

    "VoudounAMD": {
        "APP_ENV": "dev",
        "SECRET_BACKEND": "local",
        "DATABASE_BACKEND": "sqlite",
        "PROJECT_ROOT": "C:\\Users\\Mr_Vo\\Documents\\Python\\projects\\data-coven",
    },

    "data-coven-uat": {
        "APP_ENV": "uat",
        "SECRET_BACKEND": "gsm",
        "DATABASE_BACKEND": "postgres",
        "PROJECT_ROOT": "C:\\Users\\Mr_Vo\\Documents\\Python\\projects\\data-coven",
    }

}


def load_env():

    hostname = socket.gethostname()

    if hostname not in ENVIRONMENTS:
        raise RuntimeError(
            f"Unknown host: {hostname}"
        )


    for key, value in ENVIRONMENTS[
        hostname
    ].items():

        os.environ[key] = value