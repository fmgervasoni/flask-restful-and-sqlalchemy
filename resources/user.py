from hmac import compare_digest
from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required
)
from models.user import UserModel
from utils.blocklist import BLOCKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument("username",
    type=str,
    required=True,
    help="This field cannot be blank."
)
_user_parser.add_argument("password",
    type=str,
    required=True,
    help="This field cannot be blank."
)

class UserRegister(Resource):
    def post(self) -> tuple:
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data["username"]):
            return {"message": "A user with that username already exists"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created Successfully"}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id:int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id) -> tuple:
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "user not found"}, 404
        user.delete_from_db()
        return {"message": f"User {user_id} deleted."}, 201


class UserLogin(Resource):
    def post(self) -> tuple:
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and compare_digest(user.password, data['password']):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                    }, 200
        return {"message": "Invalid Credentials!"}, 401

class UserLogout(Resource):
    @jwt_required(fresh=True)
    def post(self) -> tuple:
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self) -> tuple:
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
