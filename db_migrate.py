# db_migrate.py

""" 
Use if you need to migrate data over to a new database schema
"""

from views import db
# from datetime import datetime
from config import DATABASE_PATH 
import sqlite3

# with sqlite3.connect(DATABASE_PATH) as connection:
# 	c = connection.cursor()

# 	# temp change name of tasks table
# 	c.execute('ALTER TABLE tasks RENAME TO old_tasks')

# 	# recreate new tasks table with updated schema
# 	db.create_all()

# 	# retrieve data from old tasks table
# 	c.execute("""SELECT name, due_date, priority, status
# 					FROM old_tasks ORDER BY task_id ASC""")

# 	# save all rows as a list of tuples; set posted_date to now and user_id to 1
# 	data = [(row[0], row[1], row[2], row[3],
# 		datetime.now(), 1) for row in c.fetchall()]

# 	c.executemany("""INSERT INTO tasks (name, due_date, priority, status, posted_date, user_id)
# 			VALUES(?,?,?,?,?,?)""", data)


# 	# delete old_tasks table
# 	c.execute('DROP TABLE old_tasks')

with sqlite3.connect(DATABASE_PATH) as connection:

	c = connection.cursor()

	# Temp change the name of the users table
	c.execute("ALTER TABLE user RENAME TO old_users ")

	# Recreate the new users table with updated schema
	db.create_all()

	# Get old data from old_users
	c.execute('''SELECT * FROM old_users
					ORDER BY id ASC''')

	data = [(row[0], row[1], row[2], 'user') for row in c.fetchall()]

	c.executemany("""INSERT INTO user (name, email, password, role)
						VALUES (?,?,?,?)""", data)

	c.execute('DROP TABLE old_users')


