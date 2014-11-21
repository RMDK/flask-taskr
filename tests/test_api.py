# /tests/test_api.py

import os
import unittest
from datetime import date

from project import app, db
from config import basedir
from project.models import Task

TEST_DB = 'test_db'

class ApiTests(unittest.TestCase):

	# Setup and teardown
	# Executed before each test

	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
			os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()

		self.assertEquals(app.debug, False)

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	##################
	##### Helpers ####
	##################
	
	def add_tasks(self):
		db.session.add(
			Task(
				'count to ten', 
				date(2015,1,22),
				10,
				date(2015,1,05),
				1,1))
		db.session.commit()
		db.session.add(
			Task(
				'eat some breakfast',
				date(2016,2,23),
				10,
				date(2016,2,07),
				1,1))
		db.session.commit()

	##################
	##### views ######
	##################

	def test_collection_endpoint_returns_crrent_data(self):
		self.add_tasks()
		response = self.app.get('api/tasks/', follow_redirects=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.mimetype, 'application/json')
		self.assertIn('count to ten', response.data)
		self.assertIn('eat some breakfast', response.data)

if __name__ == '__main__':
	unittest.main()



