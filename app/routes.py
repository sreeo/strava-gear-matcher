from flask import Blueprint, render_template,  session, jsonify, request, current_app
from app.auth import auth_required, update_user_gears
from app.strava_api import get_athlete, get_activities, update_activity
from app.models import User, Gear, db_session, db
from app.image_processing import find_best_match, load_model

from PIL import Image

main = Blueprint('main', __name__)
model, processor = load_model()


@main.route('/api/gear')
@auth_required
def get_gear():
    user_id = session.get('user_id')
    user = User.query.get(user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    gear_list = Gear.query.filter_by(user_id=user.id).all()
    gear_data = [{
        'id': gear.id,
        'strava_gear_id': gear.strava_gear_id,
        'name': gear.name,
        'type': gear.type,
        'description': gear.description or ''
    } for gear in gear_list]

    return jsonify(gear_data)


@main.route('/api/gear/<int:gear_id>', methods=['PUT'])
@auth_required
def update_gear_description(gear_id):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    gear = Gear.query.filter_by(id=gear_id, user_id=user.id).first()
    if not gear:
        return jsonify({'error': 'Gear not found'}), 404

    data = request.json
    description = data.get('description')
    if description is None:
        return jsonify({'error': 'Description is required'}), 400

    gear.description = description
    db.session.commit()

    return jsonify({
        'message': 'Gear description updated successfully',
        'gear': {
            'id': gear.id,
            'strava_gear_id': gear.strava_gear_id,
            'name': gear.name,
            'type': gear.type,
            'description': gear.description
        }
    }), 200


@main.route('/')
def index():
    return render_template('auth.html')


@main.route('/dashboard')
@auth_required
def dashboard():
    athlete_detail = get_athlete(session['access_token'])
    user = User.query.get(session['user_id'])

    with db_session():
        update_user_gears(session['user_id'], athlete_detail)

    gear_list = athlete_detail.get(
        'bikes', []) + athlete_detail.get('shoes', [])
    return render_template('dashboard.html', user=user, gear_list=gear_list)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/api/upload_image', methods=['POST'])
@auth_required
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        image = Image.open(file.stream)
        user_id = session.get('user_id')
        gear_array = Gear.query.filter_by(user_id=user_id).all()

        best_matched_gear, score = find_best_match(
            image, gear_array, model, processor)
        activities = get_activities(session['access_token'])
        current_app.logger.info("Best matched gear %s", best_matched_gear.name)
        if activities:
            activity_to_update = activities[0]
            activity_to_update['gear_id'] = best_matched_gear.strava_gear_id
            update_activity(
                session['access_token'], activity_to_update)
            current_app.logger.info("Updating activity %s with gear_id %s",
                                    activity_to_update, best_matched_gear.strava_gear_id)
        return jsonify({'message': best_matched_gear.name, 'score': score}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400
