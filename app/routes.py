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
from flask import request
from app import app
from app import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse

#the default start page
@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = [
        {
            'author': {'username': 'Philip Pullman'},
            'body': 'His Dark Materials'
        },
        {
            'author': {'username': 'Leo Tolstoy'},
            'body': 'War and Peace'
        },
        {
            'author': {'username': 'Fyodor Dostoyevsky'},
            'body': 'Crime and Punishment'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

# the login page
# The methods argument in the route decorator tells Flask that this view function accepts 
# GET and POST requests. When the browser sends the POST request as a result of the user 
# pressing the submit button, form.validate_on_submit() is going to gather all the data, 
# run all the validators attached to fields, and if everything is all right it will return 
# True, indicating that the data is valid and can be processed by the application. 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

# I will also need to offer users the option to log out of the application. This can 
# be done with Flask-Login's logout_user() function
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

#the view function that is going to handle user registrations
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)