import os
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Hello World"


if __name__ == "__main__":
    debug_mode = os.getenv("APP_ENV") == "dev"
    app.run(debug=debug_mode)
