from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/so-much-auth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super secret' # bad practice in general, but we'll live with it for now
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.users.models import User

login_manager.init_app(app)
login_manager.login_view = "users.login"
login_manager.login_message = "Please log in!"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

app.register_blueprint(users_blueprint, url_prefix='/users')

