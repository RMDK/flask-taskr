# db_create.py

from project import db

# Create the database and tables
db.create_all()

db.session.commit()