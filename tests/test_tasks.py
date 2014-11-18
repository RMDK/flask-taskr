import os
import unittest

from views import app, db
from config import basedir
from models import User

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

### Helper functions ###
	
	# logs a user in so we dont have to rewrite code
	def login(self, name, password):
		return self.app.post('/', data=dict(name=name, password=password), 
			follow_redirects=True)
	
	def register(self):
		return self.app.post('register/', data=dict(name='kellyrm',email='kellyrm321@gmail.com',
			password='yssirk123', confirm='yssirk123'), follow_redirects=True)

	def register_error(self):
		return self.app.post('register/', data=dict(name='kellyrm',email='kellyrm321fkew.com',
			password='yssirk123', confirm=''), follow_redirects=True)


	def create_user(self):
		new_user = User(name='kellyrm', email='email.ryan@gmail.com', password='yssirk123')
		db.session.add(new_user)
		db.session.commit()

	def create_user2(self):
		new_user = User(name='cacolvil', email='cacolvil@gmail.com', password='yssirk123')
		db.session.add(new_user)
		db.session.commit()

	def create_admin_user(self):
		new_user = User(name='jimbob', email='jimbob@nocondoms.com', password='yssirk123', role='admin')
		db.session.add(new_user)
		db.session.commit()

	def create_task(self):
		return self.app.post('add/', data=dict(
			name='Go to the bank', 
			due_date='02-05-2014',
			priority='1',
			posted_date='02-04-2014',
			status='1'), 
			follow_redirects=True)

	def logout(self):
		return self.app.get('logout/', follow_redirects=True)

#### TESTS ####

## FORMS ##
	def test_users_cannot_add_error_tasks(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.post('add/', data=dict(
			name='Go to the bank',
			), follow_redirects=True)
		self.assertIn('This field is required', response.data)

	def test_users_can_complete_tasks(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		response = self.app.get('complete/1/', follow_redirects=True)
		self.assertIn('The task was marked as complete. Nice.', response.data)

	def test_users_can_delete_tasks(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		response = self.app.get('delete/1/', follow_redirects=True)
		self.assertIn('The task was deleted.', response.data)

	def test_users_can_add_tasks(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		response = self.create_task()
		self.assertIn('New entry was successfully posted. Thanks.', 
			response.data)


## VIEWS ##

	def test_logged_in_out_users_can_access_tasks_page(self):
		self.register()
		self.login('kellyrm','yssirk123')
		response = self.app.get('tasks/')
		self.assertEquals(response.status_code, 200)
		self.assertIn('Add a new request:', response.data)
		# Logged out users shouldnt be able to check tasks
		self.logout()
		response = self.app.get('tasks/', follow_redirects=True)
		self.assertIn('You need to login first.', response.data)

	def test_users_cannot_complete_or_delete_tasks_that_arnt_thiers(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_user2()
		self.login('cacolvil', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.get('complete/1/', follow_redirects=True)
		self.assertIn('You can only update tasks that belong to you.', response.data)
		response = self.app.get('delete/1/', follow_redirects=True)
		self.assertIn('You can only delete a task that belongs to you.', response.data)

	def test_admins_can_complete_or_delete_any_task(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_admin_user()
		self.login('jimbob', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.get('complete/1/', follow_redirects=True)
		self.assertNotIn('You can only update tasks that belong to you.', response.data)
		response = self.app.get('delete/1/', follow_redirects=True)
		self.assertNotIn('You can only delete a task that belongs to you.', response.data)

if __name__ == '__main__':
	unittest.main()
