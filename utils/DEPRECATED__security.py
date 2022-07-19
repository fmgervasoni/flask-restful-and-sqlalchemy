from hmac import compare_digest
from resources.user import UserModel


def authenticate(username:str, password:str) -> UserModel:
    user = UserModel.find_by_username(username)
    if user and compare_digest(user.password, password):
        return user


def identity(payload:dict) -> str:
    user_id = payload["identity"]
    return UserModel.find_by_id(user_id)
