#  The application then imports the routes module.
# The routes are the different URLs that the application implements.
# remember that al of this is created in a virual environment
# which is a package (container) for all the app files
# to launch the virtual environment: source venv/bin/activate

from flask import Flask
from config import Config

app = Flask(__name__)

# Now that I have a config file, I need to tell Flask to read it and apply it. 
app.config.from_object(Config)

from app import routes