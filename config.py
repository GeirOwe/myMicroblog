# A format that I really like because it is very extensible, is to use a class to store 
# configuration variables. To keep things nicely organized, I'm going to create the 
# configuration class in a separate Python module.

import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'