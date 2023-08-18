from utils import db
import uuid
from sqlalchemy.orm import validates
import re
from passlib.hash import pbkdf2_sha256 as sha256


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

    # this is to validate the username
    @validates('username')
    # declare the function, key is the column name, username is the value
    def validate_username(self, key, username):
        # if username is not provided, raise an error
        if not username:
            raise AssertionError('No username provided')
        # if username is already in use, raise an error
        if User.query.filter(User.username == username).first():
            raise AssertionError('Username is already in use')
        # if username is less than 5 characters or more than 20 characters, raise an error
        if len(username) < 5 or len(username) > 20:
            raise AssertionError('Username must be between 5 and 20 characters')
        # return the username
        return username

    # this is to validate the email
    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        if User.query.filter(User.email == email).first():
            raise AssertionError('Email is already in use')
        if not check_for_valid_email(email):
            raise AssertionError('Provided email is not an email address')
        return email

    # this is to validate the first name
    @validates('first_name')
    def validate_first_name(self, key, first_name):
        if not first_name:
            raise AssertionError('No first name provided')
        if len(first_name) < 2 or len(first_name) > 50:
            raise AssertionError('First name must be between 2 and 50 characters')
        return first_name

    # this is to validate the last name
    @validates('last_name')
    def validate_last_name(self, key, last_name):
        if not last_name:
            raise AssertionError('No last name provided')
        if len(last_name) < 2 or len(last_name) > 100:
            raise AssertionError('Last name must be between 2 and 100 characters')
        return last_name

    # this is to validate the password
    @validates('password')
    def validate_password(self, key, password):
        if not password:
            raise AssertionError('No password provided')
        if len(password) < 8 or len(password) > 100:
            raise AssertionError('Password must be between 8 and 100 characters')
        return password

    # this is to check if the password is correct
    def check_password(self, password):
        return sha256.verify(password, self.password)
    
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


# this is to check if the email is in the right format
def check_for_valid_email(email):
    # this is to check if the email is valid
    # this check if the email has @ and .
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True
