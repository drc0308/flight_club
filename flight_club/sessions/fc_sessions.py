from flight_club import db
from flight_club.models.models import User, Beer, Session

import flight_club.models.db_func as db_func
from sqlalchemy.sql import func


class FCSession:
    """FCSession class, interacts with db
    creates easier to work with object.
    """

    def __init__(self, session_id: int):
        self._id = session_id
        self._get_session_from_db()
        self._get_session_winner()
        self._determine_avg_session_abv()

    def _get_session_from_db(self):
        self._session = Session.query.filter_by(id=self._id).first()
        self._beers = self._session.beers
        self._date = self._session.date

    def _get_session_winner(self):
        # This might not need to be it's own query :shrug:
        win_beer = Beer.query.filter_by(session_id=self._id, win=1).first()
        self._winning_beer = win_beer.beer_name
        self._winning_brewery = win_beer.brewery
        self._winner = win_beer.username

    def _determine_avg_session_abv(self):
        self._session_avg_abv = round(
            Beer.query.with_entities(func.avg(Beer.beer_abv).label("avg"))
            .filter_by(session_id=self._id)
            .all()[0][0],
            2,
        )

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
    
    @property
    def winning_beer(self):
        return self._winning_beer

    @property
    def winning_brewery(self):
        return self._winning_brewery

    @property
    def session_avg_abv(self):
        return self._session_avg_abv
