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
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
			os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()

		self.assertEquals(app.debug, False)

	# executed after each test
	def tearDown(self):
		db.drop_all()

### Helper functions ###
	
	# logs a user in so we dont have to rewrite code
	def login(self, name, password):
		return self.app.post('/users/', data=dict(name=name, password=password), 
			follow_redirects=True)
	
	def register(self):
		return self.app.post('users/register/', data=dict(name='kellyrm',email='kellyrm321@gmail.com',
			password='yssirk123', confirm='yssirk123'), follow_redirects=True)

	def register_error(self):
		return self.app.post('users/register/', data=dict(name='kellyrm',email='kellyrm321fkew.com',
			password='yssirk123', confirm=''), follow_redirects=True)


	def create_user(self):
		new_user = User(name='kellyrm', email='email.ryan@gmail.com', 
			password=bcrypt.generate_password_hash('yssirk123'))
		db.session.add(new_user)
		db.session.commit()

	def create_user2(self):
		new_user = User(name='cacolvil', email='cacolvil@gmail.com',
		password=bcrypt.generate_password_hash('yssirk123'))
		db.session.add(new_user)
		db.session.commit()

	def create_admin_user(self):
		new_user = User(name='jimbob', email='jimbob@nocondoms.com', 
			password=bcrypt.generate_password_hash('yssirk123'), 
			role='admin')
		db.session.add(new_user)
		db.session.commit()

	def create_task(self):
		return self.app.post('tasks/add/', data=dict(
			name='Go to the bank', 
			due_date='02-05-2014',
			priority='1',
			posted_date='02-04-2014',
			status='1'), 
			follow_redirects=True)

	def logout(self):
		return self.app.get('users/logout/', follow_redirects=True)

#### TESTS ####

## FORMS ##
	def test_users_cannot_add_error_tasks(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/tasks/', follow_redirects=True)
		response = self.app.post('tasks/add/', data=dict(
			name='Go to the bank',
			), follow_redirects=True)
		self.assertIn('This field is required', response.data)

	def test_users_can_complete_tasks(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/tasks/', follow_redirects=True)
		self.create_task()
		response = self.app.get('tasks/complete/1/', follow_redirects=True)
		self.assertIn('The task was completed. Nice.', response.data)

	def test_users_can_delete_tasks(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/tasks/', follow_redirects=True)
		self.create_task()
		response = self.app.get('tasks/delete/1/', follow_redirects=True)
		self.assertIn('The task was deleted.', response.data)

	def test_users_can_add_tasks(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/tasks/', follow_redirects=True)
		response = self.create_task()
		self.assertIn('New entry was successfully posted. Thanks.', 
			response.data)

## VIEWS ##

	def test_logged_in_out_users_can_access_tasks_page(self):
		self.register()
		self.login('kellyrm','yssirk123')
		response = self.app.get('tasks/tasks/')
		self.assertEquals(response.status_code, 200)
		self.assertIn('Add a new request:', response.data)
		# Logged out users shouldnt be able to check tasks
		self.logout()
		response = self.app.get('tasks/tasks/', follow_redirects=True)
		self.assertIn('You need to login first.', response.data)

	def test_users_cannot_complete_or_delete_tasks_that_arnt_thiers(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/tasks/', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_user2()
		# Can they see links they shouldnt?
		response = self.login('cacolvil', 'yssirk123')
		# self.app.get('tasks/tasks/', follow_redirects=True)
		self.assertNotIn('Mark as complete', response.data)
		self.assertNotIn('Delete', response.data)
		# Can they complete of delete tasks they shouldnt?
		self.login('cacolvil', 'yssirk123')
		response = self.app.get('tasks/complete/1/', follow_redirects=True)
		self.assertIn('You can only update tasks that belong to you.', response.data)
		response = self.app.get('tasks/delete/1/', follow_redirects=True)
		self.assertIn('You can only delete tasks that belong to you.', response.data)

	def test_admins_can_complete_or_delete_any_task(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/tasks/', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_admin_user()
		# Can admins see all links?
		response = self.login('jimbob', 'yssirk123')
		self.assertIn('Mark as Complete', response.data)
		self.assertIn('Delete', response.data)
		
		# Can admins delete and complete anything?
		self.login('jimbob', 'yssirk123')
		# self.app.get('tasks/tasks/', follow_redirects=True)
		response = self.app.get('tasks/complete/1/', follow_redirects=True)
		self.assertNotIn('You can only update tasks that belong to you.', response.data)
		response = self.app.get('tasks/delete/1/', follow_redirects=True)
		self.assertNotIn('You can only delete tasks that belong to you.', response.data)

if __name__ == '__main__':
	unittest.main()
