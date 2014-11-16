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
	
	def register(self, name, email, password, confirm):
		return self.app.post('register/', data=dict(name=name,email=email,
			password=password, confirm=confirm), follow_redirects=True)

	def create_user(self):
		new_user = User(name='kellyrm', email='email.ryan@gmail.com', password='yssirk123')
		db.session.add(new_user)
		db.session.commit()

	def create_user2(self):
		new_user = User(name='cacolvil', email='cacolvil@gmail.com', password='yssirk123')
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

	### TESTS ###
	
	# Each test should start with 'test'
	def test_user_setup(self):
		new_user = User('kellyrm', 'kellyrm321@gmail.com', 'yssirk123')
		db.session.add(new_user)
		db.session.commit()
		test = db.session.query(User).all()
		for t in test:
			t.name 
		assert t.name == 'kellyrm'

	def test_form_is_present_on_login_page(self):
		response = self.app.get('/')
		self.assertEquals(response.status_code, 200)
		self.assertIn('Please sign in to access your task list', response.data)


	def test_users_cannot_login_unless_registered(self):
		response = self.login('foo', 'bar')
		self.assertIn('Invalid username or password.', response.data)


	def test_users_can_login(self):
		self.register('kellyrm', 'email.ryan.kelly@gmail.com', 'yssirk123', 'yssirk123')
		response = self.login('kellyrm', 'yssirk123')
		self.assertIn('You are logged in. Go Crazy.', response.data)

	def test_invalid_form_data(self):
		self.register('kellyrm', 'email.ryan.kelly@gmail.com', 'yssirk123', 'yssirk123')
		response = self.login('alert("alert box!);', 'foo')
		self.assertIn('Invalid username or password.', response.data)

	def test_form_is_present_on_register_page(self):
		response = self.app.get('register/')
		self.assertEquals(response.status_code, 200)
		self.assertIn('Please register to access the task list', response.data)

	def test_user_registration(self):
		self.app.get('register/', follow_redirects=True)
		response = self.register('kellyrm', 'email.ryan.kelly@gmail.com', 
			'yssirk123', 'yssirk123')
		assert 'Thanks for registering. Please login.' in response.data

	def test_user_registration_error(self):
		self.app.get('register/', follow_redirects=True)
		self.register('kellyrm', 'email.ryan.kelly@gmail.com',
		 'yssirk123', 'yssirk123')
		self.app.get('register/', follow_redirects=True)
		self.register('kellyrm', 'email.ryan.kelly@gmail.com', 
			'yssirk123', 'yssirk123')
		response = self.register('kellyrm', 'email.ryan.kelly@gmail.com', 'yssirk123', 'yssirk123')
		self.assertIn('Snooze you lose. That username and/or email already exists.', 
			response.data)

	def test_loggin_in_users_can_logout(self):
		self.register('Fletcher', 'email.ryan.kelly@gmail.com',
		 'yssirk123', 'yssirk123')
		self.login('Fletcher', 'yssirk123')
		response = self.logout()
		self.assertIn('You are logged out. Bye. :(', response.data)

	def test_not_logged_in_cannot_logout(self):
		response = self.logout()
		self.assertNotIn('You are logged out. Bye. :(', response.data)
		
	def test_logged_in_users_can_access_tasks_page(self):
		self.register('kellyrm', 'email.ryan.kelly@gmail.com',
		 'yssirk123', 'yssirk123')
		self.login('kellyrm','yssirk123')
		response = self.app.get('tasks/')
		self.assertEquals(response.status_code, 200)
		self.assertIn('Add a new request:', response.data)

	def test_not_loggin_in_users_cannot_access_tasks(self):
		response = self.app.get('tasks/', follow_redirects=True)
		self.assertIn('You need to login first.', response.data)

	def test_users_can_add_tasks(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		response = self.create_task()
		self.assertIn('New entry was successfully posted. Thanks.', 
			response.data)

	def test_users_cannot_add_tasks_when_error(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.post('add/', data=dict(
			name='Go to the bank'), follow_redirects=True)
		self.assertIn('This field is required.', response.data)

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

	def test_users_cannot_complete_tasks_that_arnt_thiers(self):
		self.create_user()
		self.login('kellyrm', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		self.create_task()
		self.logout()
		self.create_user2()
		self.login('cacolvil', 'yssirk123')
		self.app.get('tasks/', follow_redirects=True)
		response = self.app.get('complete/1/', follow_redirects=True)
		self.assertNotIn('The task was marked as complete. Nice.', response.data)

if __name__ == '__main__':
	unittest.main()
