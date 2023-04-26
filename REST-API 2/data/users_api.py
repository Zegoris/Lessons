from flask import jsonify, request, Blueprint

from data import db_session
from data.users import User

blueprint = Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {'users':
             [item.to_dict(only=('id', 'surname', 'name',
                                 'age', 'position', 'speciality',
                                 'address', 'city_from', 'email',
                                 'hashed_password', 'modified_date')) for item in users]
         }
    )

@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def get_one_news(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'user': user.to_dict(only=('id', 'surname', 'name',
                                       'age', 'position', 'speciality',
                                       'address', 'city_from', 'email',
                                       'hashed_password', 'modified_date'))
        }
    )

@blueprint.route('/api/users', methods=['POST'])
def create_job():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['surname', 'name',
                  'age', 'position', 'speciality',
                  'address', 'city_from', 'email',
                  'password']):
        return jsonify({'error': 'Bad request'})
    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address = request.json['address'],
        city_from=request.json['city_from'],
        email=request.json['email']
    )
    user.set_password(request.json['password'])
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_job(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/users/<int:user_id>', methods=['PUT'])
def change_job(user_id):
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'Not found'})
    user.surname = request.json['surname']
    user.name = request.json['name']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.city_from = request.json['city_from']
    user.email = request.json['email']
    user.set_password(request.json['password'])
    db_sess.commit()
    return jsonify({'success': 'OK'})
