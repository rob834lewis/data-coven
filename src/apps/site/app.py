from flask import Flask

from src.apps.site.routes import site_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(site_bp)
    return app


app = create_app()


if __name__ == "__main__":
    debug_mode = os.getenv("APP_ENV") == "dev"
    app.run(debug=debug_mode)
