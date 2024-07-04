from sqlalchemy.exc import IntegrityError
from contextlib import contextmanager
from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strava_id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(512), nullable=False)


class Gear(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strava_gear_id = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(512), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('gear', lazy=True))
    description = db.Column(db.String(512), nullable=True)
    type = db.Column(db.String(128), nullable=False)


@contextmanager
def db_session():
    try:
        yield
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise
    except Exception:
        db.session.rollback()
        raise
    finally:
        db.session.close()
