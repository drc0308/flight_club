import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from flight_club import db
from flight_club.models.models import User, Beer, Session
from flight_club.auth.views import login_required

bp = Blueprint('users', __name__, url_prefix='/users')

# TODO (dan) move this to a profile view
@bp.route('/<user_id>', methods=['GET'])
def user_page(user_id):
    if type(user_id) is str:
        print('here')
        user = User.query.filter_by(username=user_id).first()
    else:
        user = user_id

    beers = user.beers
    return render_template('users/profile.html', beers=beers)

@bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return user_page(g.user)
    