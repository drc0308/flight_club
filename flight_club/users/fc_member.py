from flight_club import db
from flight_club.models.models import User, Beer, Session

import flight_club.models.db_func as db_func
from sqlalchemy.sql import func


class FCMember:
    """Class for creating an FCMember object.
    This handles communication with the database
    and putting it into a easy to work with format.
    """

    def __init__(self, username: str):
        # TODO (dan) For now I think I'll check before making this
        # There should probably be so better "loader" system...
        # if not db_func.check_if_user_exists(username):
        self._username = username
        self._get_user_data_from_db()
        self._determine_wins()
        self._determine_scores()
        self._determine_average_abv()

    def _get_user_data_from_db(self):
        self._user = User.query.filter_by(username=self._username).first()
        self._beers = self._user.beers

    def _determine_wins(self):
        self._wins = Beer.query.filter_by(username=self._username, win=1).all()
        self._win_count = len(self._wins)

    def _determine_scores(self):
        self._avg_score = (
            Beer.query.with_entities(func.avg(Beer.votes).label("avg"))
            .filter_by(username=self._username)
            .all()[0][0]
        )

    def _determine_average_abv(self):
        query_result = (
            Beer.query.with_entities(func.avg(Beer.beer_abv).label("avg"))
            .filter_by(username=self._username)
            .all()[0][0]
        )
        if query_result is None:
            self._avg_abv = 0.0
        else:
            self._avg_abv = round(query_result, 2)

    @property
    def username(self):
        return self._username

    @property
    def beers(self):
        return self._beers

    @property
    def wins(self):
        return self._wins

    @property
    def win_count(self):
        return self._win_count

    @property
    def avg_score(self):
        return self._avg_score

    @property
    def avg_abv(self):
        return self._avg_abv
