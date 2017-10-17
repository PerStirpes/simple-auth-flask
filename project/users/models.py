from project import db, bcrypt
from flask_login import UserMixin
from random import choice

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    secret_fruit = db.Column(db.Text)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.secret_fruit = choice([
            'apple',
            'banana',
            'cherry',
            'strawberry'
            'grape',
            'orange',
            'pineapple',
            'peach',
            'pear',
            'mango',
            'grapefruit',
            'cantaloupe',
            'kiwi',
            'avocado',
            'watermelon',
            'lemon',
            'guava',
            'blackberry',
            'papaya'
        ])

    @classmethod
    def authenticate(cls, username, password):
        found_user = cls.query.filter_by(username = username).first()
        if found_user:
            authenticated_user = bcrypt.check_password_hash(found_user.password, password)
            if authenticated_user:
                return found_user
        return False