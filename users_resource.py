from api.users_parser import parser
from flask_restful import abort, Resource
from flask import jsonify
from data.users import User
from data import db_session


class UserResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify({
            'users': user.to_dict(only=(
                'id',
                'surname',
                'name',
                'age',
                'position',
                'speciality',
                'address',
                'email',
                'modified',
                'city_from',
            )),
        })

    def put(self, user_id):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == args['id']).first()

        if not user:
            return jsonify({'error': 'Bad request'})
        if 'email' in args:
            temp_user = db_sess.query(User).filter(
                User.email == args['email']).first()
            if temp_user:
                return jsonify(
                    {'error': 'User with this email already exists'})

        user.surname = args.get('surname', user.surname)
        user.name = args.get('name', user.name)
        user.age = args.get('age', user.age)
        user.position = args.get('position', user.position)
        user.speciality = args.get('speciality', user.speciality)
        user.address = args.get('address', user.address)
        user.email = args.get('email', user.email)
        user.city_from = args.get('city_from', user.city_from)

        db_sess.commit()
        return jsonify({'success': 'OK'})

    def delete(self, user_id):
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)

        db_sess.delete(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


class UserListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({
            'users': [item.to_dict(only=(
                'id',
                'surname',
                'name',
                'age',
                'position',
                'speciality',
                'address',
                'email',
                'modified',
                'city_from',
            )) for item in users],
        })

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(args['id'])
        if user:
            return jsonify({'error': 'Id already exists'})
        if not all(key and args[key] in args.keys() for key in [
            'id',
            'surname',
            'name',
            'age',
            'position',
            'speciality',
            'address',
            'email',
            'password',
            'city_from',
        ]):
            return jsonify({'error': 'Bad request'})

        user = db_sess.query(User).filter(
            User.email == args['email']).first()
        if user:
            return jsonify({'error': 'User with this email already exists'})

        user = User(
            id=args['id'],
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            city_from=args['city_from']
        )

        user.set_password(args['password'])

        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})
