from flask_restx import Namespace, Resource, fields
from flask import request
from ..Model.users import User
from passlib.hash import pbkdf2_sha256 as sha256
from http import HTTPStatus
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from ..func import create_tokens


auth_namespace = Namespace("auth", description="a namespace for authentication")


signup_model = auth_namespace.model(
    "SignUp",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True, description="A username"),
        "email": fields.String(required=True, description="An email"),
        "first_name": fields.String(required=True, description="A first name"),
        "last_name": fields.String(required=True, description="A last name"),
        "password": fields.String(
            required=True, description="A password", writeOnly=True
        ),
        "confirm_password": fields.String(
            required=True, description="Confirm password", writeOnly=True
        ),
    },
)


user_model = auth_namespace.model(
    "User",
    {
        "id": fields.Integer(),
        "username": fields.String(required=True, description="A username"),
        "email": fields.String(required=True, description="An email"),
        "is_active": fields.Boolean(description="This shows that User is active"),
    },
)

login_model = auth_namespace.model(
    "Login",
    {
        "username": fields.String(required=True, description="A username"),
        "password": fields.String(
            required=True, description="A password", writeOnly=True
        ),
    },
)


@auth_namespace.route("/signup")
class Signup(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.response(
        HTTPStatus.CREATED, "User created successfully", user_model
    )
    # @auth_namespace.response(HTTPStatus.BAD_REQUEST, "Bad request")
    # @auth_namespace.response(HTTPStatus.CONFLICT, "Username or email already exists")
    def post(self):
        data = request.get_json()
        data["username"] = data["username"].lower()
        data["email"] = data["email"].lower()

        if data["password"] != data["confirm_password"]:
            auth_namespace.abort(HTTPStatus.BAD_REQUEST, "Passwords do not match")
        user = User(**data)
        user.save()
        return user, HTTPStatus.CREATED


@auth_namespace.route("/login")
class Login(Resource):
    @auth_namespace.expect(login_model)
    @auth_namespace.response(HTTPStatus.OK, "User logged in successfully", user_model)
    @auth_namespace.response(HTTPStatus.UNAUTHORIZED, "Invalid credentials")
    def post(self):
        data = request.get_json()
        username = data["username"].lower()
        password = data["password"]
        user = User.query.filter_by(username=username).first()
        if user and sha256.verify(password, user.password):
            return (
                create_tokens(user),
                HTTPStatus.OK,
            )
        else:
            auth_namespace.abort(HTTPStatus.UNAUTHORIZED, "Invalid credentials")


@auth_namespace.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    @auth_namespace.response(
        HTTPStatus.OK, "Access token refreshed successfully", user_model
    )
    @auth_namespace.response(HTTPStatus.UNAUTHORIZED, "Invalid credentials")
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        access_token = create_access_token(identity=user)
        return {"access_token": access_token}, HTTPStatus.OK
