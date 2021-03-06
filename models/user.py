from sqlalchemy.orm.query import Query
from utils.db import db

class UserModel(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username:str, password:str) -> None:
        self.username = username
        self.password = password

    def json(self) -> dict:
        return {
            "id": self.id,
            "username": self.username
        }
        
    @classmethod
    def find_by_username(cls, user_name:str) -> Query:
        return cls.query.filter_by(username=user_name).first()

    @classmethod
    def find_by_id(cls, _id:str) -> Query:
        return cls.query.filter_by(id=_id).first()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
