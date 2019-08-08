from app import app
from app.models.user import User
from flask import render_template

@app.route('/users')
def show_users():
    select = User.query.all()
    return render_template('users.html', select=select)

