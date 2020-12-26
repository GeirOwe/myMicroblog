#  The application then imports the routes module.
# The routes are the different URLs that the application implements.
# remember that al of this is created in a virual environment
# which is a package (container) for all the app files
# to launch the virtual environment: source virtublog/bin/activate

from flask import Flask

app = Flask(__name__)

from app import routes