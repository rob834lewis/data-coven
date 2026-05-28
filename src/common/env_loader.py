import socket
import os


ENVIRONMENTS = {

    "Lappy": {
        "APP_ENV": "dev",
        "SECRET_BACKEND": "local",
        "DATABASE_BACKEND": "sqlite",
        "PROJECT_ROOT": "C:/Users/Mr_Vo/Documents/Python/projects/data-coven",
    },

    "Desktop": {
        "APP_ENV": "dev",
        "SECRET_BACKEND": "local",
        "DATABASE_BACKEND": "sqlite",
    },

    "data-coven-uat": {
        "APP_ENV": "uat",
        "SECRET_BACKEND": "gsm",
        "DATABASE_BACKEND": "postgres",
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