from flask_restful import reqparse, abort, Resource
from flask import jsonify

from data import db_session
from data.users import User


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id).first()
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        return jsonify(
            {
                'user': user.to_dict(only=('id', 'surname', 'name',
                                           'age', 'position', 'speciality',
                                           'address', 'city_from', 'email',
                                           'hashed_password', 'modified_date'))
            }
        )

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('surname', required=True)
    parser.add_argument('name', required=True)
    parser.add_argument('age', required=True, type=int)
    parser.add_argument('position', required=True)
    parser.add_argument('speciality', required=True)
    parser.add_argument('address', required=True)
    parser.add_argument('city_from', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('password', required=True)

    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
            {'users':
                 [item.to_dict(only=('id', 'surname', 'name',
                                     'age', 'position', 'speciality',
                                     'address', 'city_from', 'email',
                                     'hashed_password', 'modified_date')) for item in users]
             }
        )

    def post(self):
        args = self.parser.parse_args()
        session = db_session.create_session()
        if not args:
            return jsonify({'error': 'Empty request'})
        elif not all(key in args for key in
                     ['surname', 'name',
                      'age', 'position', 'speciality',
                      'address', 'city_from', 'email',
                      'password']):
            return jsonify({'error': 'Bad request'})
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            city_from=args['city_from'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})