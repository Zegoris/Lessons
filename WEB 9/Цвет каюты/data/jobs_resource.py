from flask_restful import reqparse, abort, Resource
from flask import jsonify

from data import db_session
from data.jobs import Jobs
from datetime import datetime


def abort_if_job_not_found(jobs_id):
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id).first()
    if not jobs:
        abort(404, message=f"Job {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        if not jobs:
            return jsonify({'error': 'Not found'})
        return jsonify(
            {
                'jobs': jobs.to_dict(only=('id', 'start_date', 'user.name',
                                           'job', 'work_size', 'collaborators',
                                           'hazard.type', 'is_finished'))
            }
        )

    def delete(self, jobs_id):
        abort_if_job_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('id', required=True, type=int)
    parser.add_argument('team_leader', required=True, type=int)
    parser.add_argument('job', required=True)
    parser.add_argument('work_size', required=True, type=int)
    parser.add_argument('hazard', required=True, type=int)
    parser.add_argument('collaborators', required=True)
    parser.add_argument('is_finished', required=True, type=bool)

    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify(
            {'jobs':
                 [item.to_dict(only=('id', 'start_date', 'user.name',
                                     'job', 'work_size', 'collaborators',
                                     'hazard.type', 'is_finished')) for item in jobs]
             }
        )

    def post(self):
        args = self.parser.parse_args()
        session = db_session.create_session()
        if not args:
            return jsonify({'error': 'Empty request'})
        elif not all(key in args for key in
                     ["id", "team_leader", "job", "work_size",
                      "collaborators", "hazard", "is_finished"]):
            return jsonify({'error': 'Bad request'})
        if session.query(Jobs).filter(Jobs.id == args["id"]).first():
            return jsonify({'error': 'Id already exists'})
        jobs = Jobs(
            id=args["id"],
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            hazard=args['hazard'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished']
        )
        if jobs.is_finished:
            jobs.end_date = datetime.now()
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})