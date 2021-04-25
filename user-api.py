import flask
from flask import jsonify, request
from . import db_session
from .users import User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_users():
    db = db_session.create_session()
    return jsonify({'users': [item.to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password', 'modified', 'city_from')) for item in db.query(User).all()]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db = db_session.create_session()
    if not db.query(User).get(user_id):
        return jsonify({'error': 'Not found'})
    else:
        return jsonify({'users': db.query(User).get(user_id).to_dict(only=('id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email', 'hashed_password', 'modified', 'city_from'))})
