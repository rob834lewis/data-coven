from flask import Blueprint, render_template

from src.apps.site.project_data import PROJECTS

site_bp = Blueprint(
    "site",
    __name__,
    template_folder="templates",
)


@site_bp.route("/")
def home():
    return render_template(
        "site/home.html",
        projects=PROJECTS,
    )