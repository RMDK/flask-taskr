# project/__init__.py

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.bcrypt import Bcrypt
from flask.ext.moment import Moment
from flask_bootstrap import Bootstrap
from flask.ext.mail import Mail



app = Flask(__name__)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)


moment = Moment(app)

app.config.from_object('config')
db = SQLAlchemy(app)
manager = Manager(app)
mail = Mail(app)

migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

from project.tasks.views import tasks_blueprint
from project.users.views import users_blueprint
from project.api.views import api_blueprint

# Register blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(api_blueprint)