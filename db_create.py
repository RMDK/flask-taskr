# db_create.py

from views import db
from models import Task
from datetime import date

# Create the database and tables
db.create_all()

# Insert some dummy data

# db.session.add(Task('Finish this app', date(2014, 12, 30), 10, 1))
# db.session.add(Task('Finish v1.0 of dashboard', date(2014, 12, 10), 10, 1))

# db.session.commit()