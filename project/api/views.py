# /project/users/views.py

#################
#### imports ####
#################

from flask import request, Blueprint, jsonify, make_response

from project import app, db
from project.models import Task


################
#### config ####
################

api_blueprint = Blueprint(
    'api', __name__,
    url_prefix='/api',
    template_folder='templates',
    static_folder='static')

################
#### routes ####
################


@app.route('/api/tasks/', methods=['GET'])
def tasks():
	if request.method == 'GET':
		results = db.session.query(Task).limit(10).offset(0).all()
		json_results = []
		for r in results:
			data = {
				'task_id': r.task_id,
				'task_name': r.name,
				'due date': str(r.due_date), 
				'priority': r.priority,
				'posted date': str(r.posted_date), 
				'status': r.status,
				'user id': r.user_id
			}
			json_results.append(data)
		return jsonify(items=json_results)

@app.route('/api/tasks/<int:task_id>')
def task(task_id):
	if request.method == 'GET':
		r = db.session.query(Task).filter_by(task_id=task_id).first()
		if r:
			r = {
					'task_id': r.task_id,
					'task_name': r.name,
					'due date': str(r.due_date), 
					'priority': r.priority,
					'posted date': str(r.posted_date), 
					'status': r.status,
					'user id': r.user_id
				}
			code = 200
		else:
			r = {"Sorry": "What you are searching for does not exist."}
			code = 404
		
		return make_response(jsonify(r), code)



