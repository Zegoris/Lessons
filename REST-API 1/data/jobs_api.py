from flask import jsonify, request, Blueprint

from data import db_session
from data.jobs import Jobs

blueprint = Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {'jobs':
             [item.to_dict(only=('id', 'start_date', 'user.name',
                                 'job', 'work_size', 'collaborators',
                                 'hazard.type', 'is_finished')) for item in jobs]
         }
    )

@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_news(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': jobs.to_dict(only=('id', 'start_date', 'user.name',
                                 'job', 'work_size', 'collaborators',
                                 'hazard.type', 'is_finished'))
        }
    )

@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["id", "team_leader", "job", "work_size",
                  "collaborators", "hazard", "is_finished"]):
        return jsonify({'error': 'Bad request'})
    if db_sess.query(Jobs).filter(Jobs.id == request.json["id"]).first():
        return jsonify({'error': 'Id already exists'})
    jobs = Jobs(
        id=request.json["id"],
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        hazard=request.json['hazard'],
        collaborators=request.json['collaborators'],
        is_finished = request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_job(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})

@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def change_job(jobs_id):
    db_sess = db_session.create_session()
    if not request.json:
        return jsonify({'error': 'Empty request'})
    jobs = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()
    if not jobs:
        return jsonify({'error': 'Not found'})
    jobs.team_leader = request.json['team_leader']
    jobs.job = request.json['job']
    jobs.work_size = request.json['work_size']
    jobs.collaborators = request.json['collaborators']
    jobs.hazard = request.json['hazard']
    jobs.is_finished = request.json['is_finished']
    db_sess.commit()
    return jsonify({'success': 'OK'})
