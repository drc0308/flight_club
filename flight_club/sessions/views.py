import functools

from flask import (
    abort,
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from flight_club import db
from flight_club.models.models import Beer, Session
from flight_club.auth.views import login_required
from flight_club.sessions.fc_sessions import FCSession

import flight_club.models.db_func as db_func

bp = Blueprint("sessions", __name__, url_prefix="/sessions")


@bp.route("/add_session", methods=["GET", "POST"])
@login_required
def add_session():
    if request.method == "POST":
        print(request.form)
        if not request.form["session_id"]:
            error = "There needs to be a session id"
        if not request.form["date"]:
            error = "There needs to be a date"
        if not request.form["beers"] or int(request.form["beers"]) == 0:
            error = "There needs to be at least one beer, but one beer would be a lonely flight club dog dog dog dog dog dog dog "
        else:
            # Check Session isn't duplicate
            session_id = request.form["session_id"]
            if db_func.check_if_session_exists(session_id):
                error = "This is a duplicate session"
            else:
                # Add the session
                date = request.form["date"]
                db.session.add(Session(id=session_id, date=date))
                db.session.commit()

                # Extract Number of Beers
                num_beers = int(request.form["beers"])

                # Loop Through Form
                # TODO (dan) there is a way for this form to submit without there being beers
                # should probably fix the front end..
                for i in range(num_beers):
                    beer_name = request.form["beer_name{}".format(i)]
                    brewery = request.form["brewery{}".format(i)]
                    style = request.form["style{}".format(i)]
                    votes = request.form["votes{}".format(i)]
                    win = request.form["win{}".format(i)]
                    username = request.form["username{}".format(i)]

                    db.session.add(
                        Beer(
                            beer_name=beer_name,
                            brewery=brewery,
                            style=style,
                            votes=votes,
                            win=win,
                            username=username,
                            session_id=session_id,
                        )
                    )

                    db.session.commit()
                return render_template("sessions/fc{}".format(int(session_id)))

        flash(error)
        return render_template("sessions/add_session.html")

    return render_template("sessions/add_session.html")


@bp.route("/fc<id>", methods=["GET"])
@login_required
def view_session(id):
    # If this isn't a valid session, send a 404.
    if not db_func.check_if_session_exists(id):
        abort(404)
    fc_session = FCSession(int(id))
    return render_template(
        "sessions/session_view.html",
        session_id=fc_session.id,
        date=fc_session.date,
        winner=fc_session.winner,
        beers=fc_session.beers,
        avg_abv=fc_session.session_avg_abv,
    )


@bp.route("/list", methods=["GET"])
@login_required
def list_sessions():
    fc_sessions = Session.query.all()
    return render_template("sessions/session_list.html", sessions=fc_sessions)
