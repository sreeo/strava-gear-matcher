import requests


def get_activities(access_token):
    headers = {'Authorization': f"Bearer {access_token}"}
    response = requests.get(
        'https://www.strava.com/api/v3/athlete/activities', headers=headers)
    return response.json()


def get_athlete(access_token):
    headers = {'Authorization': f"Bearer {access_token}"}
    response = requests.get(
        'https://www.strava.com/api/v3/athlete', headers=headers)
    return response.json()


def update_activity(access_token, activity):
    headers = {'Authorization': f"Bearer {access_token}"}
    response = requests.put(
        f'https://www.strava.com/api/v3/activities/{activity['id']}', json=activity, headers=headers)
    return response.json()
