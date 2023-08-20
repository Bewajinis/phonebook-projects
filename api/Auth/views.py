from flask_restx import Namespace, Resource, fields
from flask import request
from ..Model.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required,get_jwt_identity



auth_namespace = Namespace('auth', description='a namespace for authentication')


signup_model = auth_namespace.model(
    'SignUp',{
        'id':fields.Integer(),
        'username':fields.String(required=True,description='A username'),
        'email':fields.String(required=True,description="An email"),
        "password": fields.String(required=True,description="A password")
    }
)


user_model = auth_namespace.model(
    "User" ,{
        'id':fields.Integer(),
        'username':fields.String(required=True,description="A username"),
        'email':fields.String(required=True,description="An email"),
        'password_hash': fields.String(required=True, description='A password'),
        'is_active':fields.Boolean(description= 'This shows that User is active')
    }
)


# @auth_namespace.route('/signup')
# class Signup(Resource):