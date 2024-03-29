from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument("store_id",
        type=int,
        required=True,
        help="Every item needs a store id."
    )

    @jwt_required(fresh=True)
    def get(self, name:str) -> tuple:
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @jwt_required(fresh=True)
    def post(self, name:str) -> tuple:
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists."}, 400
        data = self.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred while inserting the item."}, 500
        return item.json(), 201

    @jwt_required(fresh=True)
    def delete(self, name:str) -> tuple:
        claims = get_jwt()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted.'}, 200
        return {'message': 'Item not found.'}, 404

    @jwt_required(fresh=True)
    def put(self, name:str) -> dict:
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    @jwt_required(optional=True)
    def get(self) -> tuple:
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        # If user logged, get all attributes of items
        if user_id:
            return {'items': items}, 200
        # else, return only the names of items
        return {
            'items': [item['name'] for item in items],
            'message': 'More data available if you log in.'
        }, 200
