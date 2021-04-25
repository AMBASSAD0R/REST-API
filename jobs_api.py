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
    return jsonify(
            {'jobs': job.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished'))})


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(
            key in request.json for key in ['id', 'team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db = db_session.create_session()
    job = db.query(Jobs).get(request.json['id'])
    if j:
        return jsonify({'error': 'Id already exists'})
    else:
        job = Jobs(id=request.json['id'], team_leader=request.json['team_leader'],
                 job=request.json['job'], work_size=request.json['work_size'],
                 collaborators=request.json['collaborators'], is_finished=request.json['is_finished']
                 )
        db.add(j)
        db.commit()
        return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    
    if not job:
        return jsonify({'error': 'Not found'})
    
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs', methods=['PUT'])
def edit_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif 'id' not in request.json:
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first()
    
    if not job:
        return jsonify({'error': 'Bad request'})
    
    job.team_leader = request.json.get('team_leader', job.team_leader)
    job.job = request.json.get('job', job.job)
    job.work_size = request.json.get('work_size', job.work_size)
    job.collaborators = request.json.get('collaborators', job.collaborators)
    job.is_finished = request.json.get('is_finished', job.is_finished)
    
    db_sess.commit()
    return jsonify({'success': 'OK'})
