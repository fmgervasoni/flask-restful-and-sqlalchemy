import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from utils.db import db
from utils.blocklist import BLOCKLIST
from resources.user import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

app.config['DEBUG'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True

api = Api(app)

"""
JWT related configuration.
"""

app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY", "default")
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
app.config['JWT_BLACKLIST_ENABLED'] = True # deprecated, to be removed
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']  # deprecated, to be removed
jwt = JWTManager(app)


"""
`claims` are data we choose to attach to each jwt payload
and for each jwt protected endpoint, we can retrieve these claims via `get_jwt_claims()`
one possible use case for claims are access level control, which is shown below
"""

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:   # instead of hard-coding, we should read from a config file to get a list of admins instead (AD?)
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_data):
    return jwt_data['jti'] in BLOCKLIST

# The following callbacks are used for customizing jwt response/error messages.
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_data):
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_data):
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(TokenRefresh, '/refresh')


if __name__ == "__main__":
    db.init_app(app)

    if app.config["DEBUG"]:
        @app.before_first_request
        def create_tables():
            db.create_all()
    
    app.run(port=5000, debug=True)
