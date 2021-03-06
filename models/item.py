from sqlalchemy.orm.query import Query
from utils.db import db

class ItemModel(db.Model):
    __tablename__ = "items"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name:str, price:float, store_id:int) -> None:
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "store_id": self.store_id
        }

    @classmethod
    def find_by_name(cls, item_name:str) -> Query:
        # SELECT * FROM items WHERE name=name LIMIT 1
        return cls.query.filter_by(name=item_name).first()

    @classmethod
    def find_all(cls) -> Query:
        return cls.query.all()
    
    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
