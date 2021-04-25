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

    
@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['id', 'surname',  'name', 'age', 'position', 'speciality', 'address', 'email', 'password']):
        return jsonify({'error': 'Bad request'})
    db = db_session.create_session()
    if db.query(User).get(request.json['id']):
        return jsonify({'error': 'Id already exists'})
    if db.query(User).filter(User.email == request.json['email']).first():
        return jsonify({'error': 'User with this email already exists'})
    user = User(id=request.json['id'], surname=request.json['surname'], name=request.json['name'], age=request.json['age'],
                position=request.json['position'], speciality=request.json['speciality'], address=request.json['address'], email=request.json['email'])
    user.set_password(request.json['password'])
    db.add(user)
    db.commit()
    return jsonify({'success': 'OK'})
