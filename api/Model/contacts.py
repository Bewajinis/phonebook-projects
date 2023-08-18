from utils import db
from sqlalchemy.orm import validates
from users import generate_hex


class Contacts(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, default=generate_hex())
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), default='')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number.isdigit():
            raise ValueError('Phone number must be a number')

    def __init__(self, name, phone_number, user_id):
        self.name = name
        self.phone_number = phone_number
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<PhoneBook {self.name}>'
