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
from werkzeug.exceptions import BadRequestKeyError

bp = Blueprint("beers", __name__, url_prefix="/beers")


def return_sorted_beers(key: str = None, sort: str = None):
    """Returns the beers sorted based on the key and sort value.

    Args:
        key (str, optional): attribute to sort on
        sort (str, optional): sort ascending or descending

    Returns:
        List of Beers.
    """
    if key is None or sort is None:
        return Beer.query.all()
    else:
        if sort == "asc":
            return Beer.query.order_by(getattr(Beer, key)).all()
        elif sort == "desc":
            return Beer.query.order_by(getattr(Beer, key).desc()).all()


@bp.route("/list", methods=["GET"])
@login_required
def list_beers():

    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = current_app.config["POSTS_PER_PAGE"]
    offset = (page - 1) * per_page
    sort_key = request.args.get("key")
    sort_order = request.args.get("sort")

    fc_beers = return_sorted_beers(sort_key, sort_order)

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
