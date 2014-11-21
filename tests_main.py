import os
import unittest

from project import app, db, bcrypt
from config import basedir
from project.models import Task, User


TEST_DB = 'test.db'

class ALLTests(unittest.TestCase):

	# setup and teardown #
	
	# executed prior to each test
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
			os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()

	# executed after each test
	def tearDown(self):
		db.drop_all()


	# logs a user in so we dont have to rewrite code
	def login(self, name, password):
		return self.app.post('/users/', data=dict(name=name, password=password), 
			follow_redirects=True)

	## TESTS ##

	def test_404_error(self):
		response = self.app.get('/this-route-does-not-exist')
		self.assertEquals(response.status_code, 404)
		self.assertIn('Sorry. There\'s nothing here.', response.data)

	def test_500_error(self):
		bad_user = User(
			name='Rkelly',
			email='rkelly@olg.ca',
			password='yssirk123')
		db.session.add(bad_user)
		db.session.commit()
		response = self.login('Rkelly', 'yssirk123')
		self.assertEquals(response.status_code, 500)
		# Make sure user never sees this.
		self.assertNotIn('ValueError: Invalid salt', response.data)
		self.assertIn('Something went quite wrong!', response.data)