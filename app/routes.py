# the first attempt to ceck if the flask app is running
# So what goes in the routes module? The routes are the different URLs that the application implements. 
# In Flask, handlers for the application routes are written as Python functions, called view functions. 
# View functions are mapped to one or more route URLs so that Flask knows what logic to execute when a 
# client requests a given URL.

#If you could keep the logic of your application separate from the layout or presentation of your web pages, 
# then things would be much better organized, don't you think? You could even hire a web designer to create 
# a killer web site while you code the application logic in Python.
#Templates help achieve this separation between presentation and business logic. In Flask, templates are 
# written as separate files, stored in a templates folder that is inside the application package.

from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

#the default start page
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'GeirOwe'}
    posts = [
        {
            'author': {'username': 'Philip Pullman'},
            'body': 'His Dark Materials'
        },
        {
            'author': {'username': 'Leo Tolstoy'},
            'body': 'War and Peace'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

# the login page
# The methods argument in the route decorator tells Flask that this view function accepts 
# GET and POST requests. When the browser sends the POST request as a result of the user 
# pressing the submit button, form.validate_on_submit() is going to gather all the data, 
# run all the validators attached to fields, and if everything is all right it will return 
# True, indicating that the data is valid and can be processed by the application. 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)