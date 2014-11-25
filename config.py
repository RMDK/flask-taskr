#config.py

import os

#grabs folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
CSRF_ENABLED = True
SECRET_KEY = 'my_precious'  # must be more random key
DEBUG = False
# Define full path for DATABASE
DATABASE_PATH = os.path.join(basedir, DATABASE)

# Database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
DEFAULT_MAIL_SENDER = os.environ.get('DEFAULT_MAIL_SENDER')

# administrator list
ADMINS = os.environ.get('DEFAULT_MAIL_SENDER')