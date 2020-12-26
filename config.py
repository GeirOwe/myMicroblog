# A format that I really like because it is very extensible, is to use a class to store 
# configuration variables. To keep things nicely organized, I'm going to create the 
# configuration class in a separate Python module.

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # During development, I'm going to use a SQLite database. SQLite databases are the most 
    # convenient choice for developing small applications, sometimes even not so small ones, 
    # as each database is stored in a single file on disk and there is no need to run a database 
    # server like MySQL and PostgreSQL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # The SQLALCHEMY_TRACK_MODIFICATIONS configuration option is set to False to disable a feature
    # of Flask-SQLAlchemy that I do not need, which is to signal the application every time a 
    # change is about to be made in the database.