from flask import redirect, render_template, request, url_for, Blueprint, session, flash
from project.users.forms import UserForm
from project.users.models import User
from project import db
from functools import wraps
from flask_login import login_user, logout_user, login_required, current_user

from sqlalchemy.exc import IntegrityError

users_blueprint = Blueprint(
    'users',
    __name__,
    template_folder='templates'
)

def ensure_correct_user(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if kwargs.get('id') != current_user.id:
            flash("Not Authorized")
            return redirect(url_for('users.welcome'))
        return fn(*args, **kwargs)
    return wrapper

@users_blueprint.route('/signup', methods =["GET", "POST"])
def signup():
    form = UserForm(request.form)
    if request.method == "POST" and form.validate():
        try:
            new_user = User(form.data['username'], form.data['password'])
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError as e:
            flash("Invalid submission. Please try again.")
            return render_template('signup.html', form=form)
        return redirect(url_for('users.login'))
    return render_template('signup.html', form=form)


@users_blueprint.route('/login', methods = ["GET", "POST"])
def login():
    form = UserForm(request.form)
    if request.method == "POST":
        if form.validate():
            user = User.authenticate(form.data['username'], form.data['password'])
            if user:
                login_user(user)
                flash("You've successfully logged in!")
                return redirect(url_for('users.welcome'))
        flash("Invalid credentials. Please try again.")
    return render_template('login.html', form=form)

@users_blueprint.route('/logout')
def logout():
    logout_user()
    flash('You have been signed out.')
    return redirect(url_for('users.login'))

@users_blueprint.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@users_blueprint.route('/<int:id>/fruit')
@ensure_correct_user
def fruit(id):
    return render_template('fruit.html')





