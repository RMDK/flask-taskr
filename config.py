#config.py

import os

#grabs folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'flasktaskr.db'
CSRF_ENABLED = True
SECRET_KEY = 'my_precious'  # must be more random key

# Define full path for DATABASE
DATABASE_PATH = os.path.join(basedir, DATABASE)

# Database uri
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH
