from utils import db
import uuid
from sqlalchemy.orm import validates


def generate_hex():
    return uuid.uuid4().hex


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default=generate_hex())
    username = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phone_book = db.relationship('PhoneBook', backref='user', lazy=True)

    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise AssertionError('No username provided')
        if User.query.filter(User.username == username).first():
            raise AssertionError('Username is already in use')
        if len(username) < 5 or len(username) > 20:
            raise AssertionError('Username must be between 5 and 20 characters')
        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        if User.query.filter(User.email == email).first():
            raise AssertionError('Email is already in use')
        return email

    def __init__(self, username, first_name, last_name, email, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.username}>'


# Phone book model
class PhoneBook(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default=generate_hex())
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __init__(self, name, phone_number, user_id):
        self.name = name
        self.phone_number = phone_number
        self.user_id = user_id

    def __repr__(self):
        return f'<PhoneBook {self.name}>'
