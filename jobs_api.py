import flask
import flask
from flask import jsonify, request
from . import db_session
from .jobs import Jobs
from flask import jsonify, request

blueprint = flask.Blueprint('jobs_api', __name__, template_folder='templates')


@blueprint.route('/api/jobs', methods=['GET'])
def get_jobs():
    db = db_session.create_session()
    return jsonify(
        {
            'jobs': [item.to_dict(only=(
                'id',
                'team_leader',
                'job',
                'work_size',
                'collaborators',
                'is_finished',
            )) for item in db.query(Jobs).all()],
        }
    )


@blueprint.route('/api/jobs/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db = db_session.create_session()
    if not db.query(Jobs).get(job_id):
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': db.query(Jobs).get(job_id).to_dict(only=(
                'id',
                'team_leader',
                'job',
                'work_size',
                'collaborators',
                'is_finished',
            )),
        }
    )
