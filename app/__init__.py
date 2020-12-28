#  The application then imports the routes module.
# The routes are the different URLs that the application implements.
# remember that al of this is created in a virual environment
# which is a package (container) for all the app files
# to launch the virtual environment: source venv/bin/activate

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler
import os

# Now that I have a config file, I need to tell Flask to read it and apply it. 
app = Flask(__name__)
app.config.from_object(Config)

# The database is going to be represented in the application by the database instance.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# users can log in to the application and then navigate to different pages while 
# the application "remembers" that the user is logged in.
login = LoginManager(app)
login.login_view = 'login'

from app import routes, models, errors
# a new module called models at the bottom to define the structure of the database

# send errors to a mail, when not debugging
if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
        file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')