from flask_sqlalchemy import SQLAlchemy


# SQLAlchemy database object.
# This gets connected to the Flask app in app.py.
db = SQLAlchemy()


class User(db.Model):
    """
    Stores login users.

    For now this could be a parent account.
    Later, one parent user could have multiple child profiles.
    """

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(80),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )


class Allocation(db.Model):
    """
    Stores one weekly money allocation.

    Example:
    Rob saves:
    - spend £5
    - save £10
    - share £5

    That becomes one row in this table.
    """

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    week_number = db.Column(
        db.Integer,
        nullable=False
    )

    spend = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    save = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    share = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )