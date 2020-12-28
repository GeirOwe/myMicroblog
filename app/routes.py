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
from app.forms import EditProfileForm
from app.forms import EmptyForm
from app.models import User
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
from datetime import datetime

# The @before_request decorator from Flask register the decorated function to be executed right 
# before the view function. This is extremely useful because now I can insert code that I want 
# to execute before any view function in the application, and I can have it in a single place. 
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

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

# To create a user profile page, let's first write a new view function that 
# maps to the /user/<username> URL. Flask will accept any text in that portion of the URL, and 
# will invoke the view function with the actual text as an argument. For example, if the client 
# browser requests URL /user/susan, the view function is going to be called with the argument 
# username set to 'susan'. 
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)

# I also need to give users a form in which they can enter some information about themselves. 
# This view function is slightly different to the other ones that process a form. If 
# validate_on_submit() # returns True I copy the data from the form into the user object and 
# then write the object to the database. 
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)

# Let's add two new routes in the application to follow and unfollow a user
@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))