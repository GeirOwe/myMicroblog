# The error functions work very similarly to view functions. For these two errors, I'm 
# returning the contents of their respective templates. Note that both functions return 
# a second value after the template, which is the error code number. 
from flask import render_template
from app import app, db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500