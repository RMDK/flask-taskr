# project/__init__.py

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_object('config')
db = SQLAlchemy(app)

from project.tasks.views import tasks_blueprint
from project.users.views import users_blueprint
from project.api.views import api_blueprint

# Register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)