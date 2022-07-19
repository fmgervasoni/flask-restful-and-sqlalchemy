import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager

from utils.db import db
# from security import authenticate, identity
from resources.user import UserRegister, User
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)

app.config['DEBUG'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get ["DATABASE_URL", "sqlite:///data.db"]
app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = os.environ.get["APP_SECRET_KEY", ""]

api = Api(app)

# JWT Configuration

app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
jwt = JWTManager(app)

# Custom callbacks

@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                    'access_token': access_token.decode('utf-8'),
                    'user_id': identity.id
            })


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(UserRegister, "/register")
api.add_resource(User, "/user/<int:user_id>")


if __name__ == "__main__":
    db.init_app(app)

    if app.config["DEBUG"]:
        @app.before_first_request
        def create_tables():
            db.create_all()
    
    app.run(port=5000, debug=True)
