import flask
from flask import jsonify, request
import flask
from flask import jsonify, request
from . import db_session
from .jobs import Jobs

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs': [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished')) for
                     item in jobs],
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({'error': 'Not found'})
    else:
        return jsonify(
            {'jobs': job.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished'))})


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(
            key in request.json for key in ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    j = db_sess.query(Jobs).get(request.json['id'])
    j = Jobs(id=request.json['id'], team_leader=request.json['team_leader'],
             job=request.json['job'], work_size=request.json['work_size'],
             collaborators=request.json['collaborators'], is_finished=request.json['is_finished']
             )
    db_sess.add(j)
    db_sess.commit()
    return jsonify({'success': 'OK'})
