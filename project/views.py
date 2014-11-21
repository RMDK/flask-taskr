# views.py

#################
#### imports ####
#################

from project import app, db
from flask import flash, redirect, session, url_for, render_template
from functools import wraps
import logging


##########################
#### helper functions ####
##########################

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('users.login'))
    return wrap

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the {} field - {} error").format(
                getattr(form, field).label.text, error)

################
#### logging ###
################

# ADMINS = ['kellyrm321@gmail.com']
# if not app.debug:
#     from logging.handlers import SMTPHandler
#     mail_handler = SMTPHandler('127.0.0.1',
#                                'server-error@example.com',
#                                ADMINS, 'YourApplication Failed')
#     mail_handler.setLevel(logging.ERROR)
#     app.logger.addHandler(mail_handler)

if not app.debug:
    from logging.handlers import RotatingFileHandler
    # Get error location
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('log.txt', maxBytes=10000000, backupCount=1)
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    # Get wekzeug errors
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.DEBUG)
    log.addHandler(handler)

################
#### routes ####
################

@app.route('/', defaults={'page': 'index'})

def index(page):
    return redirect(url_for('tasks.tasks'))
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    app.logger.info('Info')

@app.errorhandler(404)
def internal_error(error):
    app.logger.warning('404 Warning')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    app.logger.warning('500 Error')
    return render_template('500.html'), 500
