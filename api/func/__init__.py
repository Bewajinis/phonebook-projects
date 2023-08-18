from flask_jwt_extended import create_access_token, create_refresh_token


def create_tokens(user):
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
