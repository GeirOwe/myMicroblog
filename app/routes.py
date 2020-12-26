# the first attempt to ceck if the flask app is running
# So what goes in the routes module? The routes are the different URLs that the application implements. 
# In Flask, handlers for the application routes are written as Python functions, called view functions. 
# View functions are mapped to one or more route URLs so that Flask knows what logic to execute when a client requests a given URL.

from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Wake up Neo ......"