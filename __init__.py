from flask import Flask
from flask_restx import Api
from .api.Auth import auth_namespace
from .utils import db
from flask_migrate import Migrate
from .api.Config import config_dict
from .api.Model import users
from .api.Model import contacts
from flask_jwt_extended import JWTManager


def create_app(config=config_dict ['dev']):
    app=Flask(__name__)



    app.config.from_object(config)

    db.init_app(app)


    jwt = JWTManager(app)

    migrate = Migrate(app,db)

    api = Api(app)


    api.add_namespace(auth_namespace, path="/auth")


    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'User':User,
            'Contact':contacts
        }
    

    return app