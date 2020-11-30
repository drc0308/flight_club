import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from flight_club import db
from flight_club.models.models import User
import flight_club.models.db_func as db_func

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Function responsible for registration"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif db_func.check_if_user_exists(username):
            error = f"User {username} is already registered."

        if error is None:
            db.session.add(
                User(username=username, password=generate_password_hash(password))
            )
            db.session.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Function reponsible for logging in"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        user = User.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session["user_id"] = user.id
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")


@bp.before_app_request
def load_logged_in_user():
    """function to load logged in user before each request"""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
        g.username = None
    else:
        g.user = User.query.filter_by(id=user_id).first()
        g.username = g.user.username


@bp.route("/logout")
def logout():
    """function to log user out and clear session"""
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    """custom decorator to wrap pages to require login"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
