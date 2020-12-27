from flask import (
    abort,
    Blueprint,
    current_app,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flask_paginate import Pagination, get_page_parameter
from flight_club import db
from flight_club.models.models import Beer
from flight_club.auth.views import login_required

bp = Blueprint("beers", __name__, url_prefix="/beers")


@bp.route("/list", methods=["GET"])
@login_required
def list_beers():

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = current_app.config["POSTS_PER_PAGE"]
    offset = (page - 1) * per_page

    fc_beers = Beer.query.all()
    pagination = Pagination(
        page=page,
        per_page=per_page,
        search=False,
        total=len(fc_beers),
        record_name="beers",
        css_framework="bootstrap3",
    )

    return render_template(
        "beers/beer_list.html",
        beers=fc_beers[offset : offset + per_page],
        pagination=pagination,
    )
