# /project/users/views.py

#################
#### imports ####
#################

from flask import request, Blueprint, jsonify

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






