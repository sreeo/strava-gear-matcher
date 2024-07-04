from flask import Blueprint, request, redirect, session, url_for
from functools import wraps
import requests
import os
from app.models import User, Gear, db_session
from app import db
from app.strava_api import get_athlete
auth = Blueprint('auth', __name__)

REDIRECT_URI = os.getenv('REDIRECT_URI')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'access_token' not in session:
            return redirect(url_for('auth.strava_auth'))
        return f(*args, **kwargs)
    return decorated_function


@auth.route('/auth')
def strava_auth():
    return redirect(f"http://www.strava.com/oauth/authorize?client_id={CLIENT_ID}"
                    f"&response_type=code&redirect_uri={REDIRECT_URI}"
                    f"&approval_prompt=force&scope=read,profile:read_all,activity:read_all,activity:write")


@auth.route('/callback')
def callback():

    def exchange_code_for_tokens(code):
        token_url = "https://www.strava.com/oauth/token"
        params = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
        response = requests.post(token_url, params=params)
        return response.json()

    def get_or_create_user(athlete_detail):
        user = User.query.filter_by(strava_id=athlete_detail['id']).first()
        if not user:
            user = User(strava_id=athlete_detail['id'],
                        name=f"{athlete_detail['firstname']} {athlete_detail['lastname']}")
            db.session.add(user)
        return user.id

    def set_session_data(user_id, tokens):
        session['user_id'] = user_id
        session['access_token'] = tokens['access_token']
        session['refresh_token'] = tokens['refresh_token']
    code = request.args.get('code')
    tokens = exchange_code_for_tokens(code)
    athlete_detail = get_athlete(access_token=tokens['access_token'])

    with db_session():
        user_id = get_or_create_user(athlete_detail)
        update_user_gears(user_id, athlete_detail)

    set_session_data(user_id, tokens)
    return redirect(url_for('main.dashboard'))


def update_user_gears(user_id, athlete_detail):
    gears = []
    for gear_type in ['shoes', 'bikes']:
        for gear in athlete_detail.get(gear_type, []):
            gear_obj = Gear.query.filter_by(
                strava_gear_id=gear['id'], user_id=user_id).first()
            if not gear_obj:
                gear_obj = Gear(strava_gear_id=gear['id'],
                                # Remove 's' to get singular form
                                type=gear_type[:-1],
                                name=gear['name'],
                                user_id=user_id)
                gears.append(gear_obj)

    if gears:
        db.session.bulk_save_objects(gears)
