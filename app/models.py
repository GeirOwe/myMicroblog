from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

# Let's add followers to the database first. Here is the followers association table.
# Since this is an auxiliary table that has no data other than the foreign keys, I created 
# it without an associated model class.
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

# The User class created above inherits from db.Model, a base class for all models 
# from Flask-SQLAlchemy.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)   #call password hashing is Werkzeug

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    #call password hashing is Werkzeug

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    
    # Adding and Removing "follows"
    # The follow() and unfollow() methods use the append() and remove() methods of the 
    # relationship object, but before they touch the relationship they use the 
    # is_following() supporting method to make sure the requested action makes sense. 
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    #In the index page of the application I'm going to show blog posts written by all the 
    # people that are followed by the logged in user, so I need to come up with a database 
    # query that returns these posts.
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


# the class to represent the Post database table
# inherits from db.Model, a base class for all models from Flask-SQLAlchemy.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# The __repr__ method tells Python how to print objects of this class, 
# which is going to be useful for debugging.
    def __repr__(self):
        return '<Post {}>'.format(self.body)

# Because Flask-Login knows nothing about databases, it needs the application's help in 
# loading a user. For that reason, the extension expects that the application will configure 
# a user loader function, that can be called to load a user given the ID.
@login.user_loader
def load_user(id):
    return User.query.get(int(id))
