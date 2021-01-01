import functools

from flask import (
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    abort,
)
from flask_paginate import Pagination, get_page_parameter
from flight_club import db
from flight_club.models.models import User, Beer, Session
from flight_club.auth.views import login_required
from flight_club.users.fc_member import FCMember
import flight_club.models.db_func as db_func
from sqlalchemy.orm import load_only

bp = Blueprint("users", __name__, url_prefix="/users")

# TODO (dan) move this to a profile view
@bp.route("/<user_id>", methods=["GET"])
def user_page(user_id):
    # If this isn't a valid user, send a 404.
    if not db_func.check_if_user_exists(user_id):
        abort(404)
    user = FCMember(user_id)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = current_app.config["POSTS_PER_PAGE"]
    offset = (page - 1) * per_page
    pagination = Pagination(
        page=page,
        per_page=per_page,
        search=False,
        total=len(user.beers),
        record_name="beers",
        css_framework="bootstrap3",
    )

    return render_template(
        "users/profile.html",
        user=user.username,
        score=user.avg_score,
        beers=user.beers[offset : offset + per_page],
        win_total=user._win_count,
        wins=user.wins,
        avg_abv=user.avg_abv,
        pagination=pagination,
        page=page,
        per_page=per_page,
    )


@bp.route("/profile", methods=["GET"])
@login_required
def profile():
    return user_page(g.username)

def get_users():
    fc_users = User.query.options(load_only('username')).all()
    user_list = []
    for user in fc_users:
        user_list.append(FCMember(user.username))
    return user_list

@bp.route("/list", methods=["GET"])
@login_required
def list_users():
    users = get_users()
    return render_template("users/users_list.html", users=users)
