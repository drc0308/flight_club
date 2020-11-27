from flight_club import db
from flight_club.models.models import User, Beer, Session

import flight_club.models.db_helper as db_helper
from sqlalchemy.sql import func


class FCSession:
    """FCSession class, interacts with db
    creates easier to work with object.
    """

    def __init__(self, session_id: int):
        self._id = session_id
        self._get_session_from_db()
        self._get_session_winner()

    def _get_session_from_db(self):
        self._session = Session.query.filter_by(id=self._id).first()
        self._beers = self._session.beers
        self._date = self._session.date

    def _get_session_winner(self):
        # This might not need to be it's own query :shrug:
        self._winner = Beer.query.filter_by(session_id=self._id, win=1).first().username

    @property
    def id(self):
        return self._id

    @property
    def session(self):
        return self._session

    @property
    def beers(self):
        return self._beers

    @property
    def date(self):
        return self._date

    @property
    def winner(self):
        return self._winner
