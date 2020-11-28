import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, abort

from flight_club import db
from flight_club.models.models import User, Beer, Session
from flight_club.auth.views import login_required
from flight_club.users.fc_member import FCMember
import flight_club.models.db_func as db_func

bp = Blueprint('users', __name__, url_prefix='/users')

# TODO (dan) move this to a profile view
@bp.route('/<user_id>', methods=['GET'])
def user_page(user_id):
    # If this isn't a valid user, send a 404.
    if not db_func.check_if_user_exists(user_id):
        abort(404)
    user = FCMember(user_id)
    return render_template('users/profile.html', 
                            user=user.username,
                            score=user.avg_score, 
                            beers=user.beers,
                            win_total=user._win_count,
                            wins=user.wins,
                            avg_abv=user.avg_abv)

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return user_page(g.username)


@bp.route('/list', methods=['GET'])
@login_required
def list_sessions():
    users = User.query.all()
    return render_template('users/users_list.html', users=users)
