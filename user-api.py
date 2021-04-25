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
