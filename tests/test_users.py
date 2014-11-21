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

## VIEWS ##

	def test_users_can_login(self):
		self.register()
		response = self.login('kellyrm', 'yssirk123')
		self.assertIn('You are logged in. Go Crazy.', response.data)

	def test_loggin_in_users_can_logout(self):
		self.register()
		self.login('kellyrm', 'yssirk123')
		response = self.logout()
		self.assertIn('You are logged out.', response.data)

	def test_not_logged_in_cannot_logout(self):
		response = self.logout()
		self.assertNotIn('You are logged out.', response.data)
		
	def test_duplicate_user_registration_error(self):
		self.register()
		response = self.register()
		self.assertIn('Snooze you lose. That username and/or email already exists.', 
			response.data)

	def test_user_registration(self):
		response = self.register()
		assert 'Thanks for registering. Please login.' in response.data

	def test_users_cannot_login_unless_registered(self):
		response = self.login('foo', 'bar')
		self.assertIn('Cannot find that username.', response.data)

	def test_task_template_displays_loggedin_username(self):
		self.register()
		self.login('kellyrm', 'yssirk123')
		response = self.app.get('tasks/tasks/', follow_redirects=True)
		self.assertIn('kellyrm', response.data)

## MODELS ##

	def test_default_user_role(self):
		db.session.add(User(
			'Jimbob',
			'jimwith19kids@nocondoms.com',
			'password'))
		db.session.commit()

		users = db.session.query(User).all()
		print users
		for user in users:
			self.assertEquals(user.role, 'user')

## FORMS ##

	def test_form_is_present_on_login_page(self):
		response = self.app.get('/users/')
		self.assertEquals(response.status_code, 200)
		self.assertIn('Please sign in to access your task list', response.data)


	def test_invalid_login_data(self):
		self.register()
		response = self.login('kellyrm', 'alert(SELECT*)')
		self.assertIn("Invalid password / username combination.", response.data)

	def test_form_is_present_on_register_page(self):
		response = self.app.get('users/register/')
		self.assertEquals(response.status_code, 200)
		self.assertIn('Please register to access the task list', response.data)


	def test_user_registration_field_errors(self):
		response = self.register_error()
		self.assertIn('This field is required', response.data)
		self.assertIn('Invalid email address', response.data)


if __name__ == '__main__':
	unittest.main()
