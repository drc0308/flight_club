from flight_club import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column("password", db.String, nullable=False)
    beers = db.relationship('Beer', backref='User', lazy=True)


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    beers = db.relationship('Beer', backref='Session', lazy=True)


class Beer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    beer_name = db.Column(db.String, nullable=False)
    beer_abv = db.Column(db.Float, nullable=False)
    brewery = db.Column(db.String, nullable=False)
    style = db.Column(db.String, nullable=False)
    votes = db.Column(db.Integer, nullable=False)
    win = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String, db.ForeignKey(User.username),
                         nullable=False)
    session_id = db.Column(db.Integer, db.ForeignKey(Session.id),
                           nullable=False)
