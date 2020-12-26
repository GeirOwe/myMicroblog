#  The application then imports the routes module.
# The routes are the different URLs that the application implements.
# remember that al of this is created in a virual environment
# which is a package (container) for all the app files
# to launch the virtual environment: source venv/bin/activate

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Now that I have a config file, I need to tell Flask to read it and apply it. 
app.config.from_object(Config)

# The database is going to be represented in the application by the database instance.
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
# a new module called models at the bottom to define the structure of the database