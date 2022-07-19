from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
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

    @jwt_required()
    def get(self, name:str) -> str:
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    def post(self, name:str) -> str:
        if ItemModel.find_by_name(name):
            return {"message": f"An item with name '{name}' already exists"}, 400

        data = Item.parser.parse_args()
        
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {"message": "An error occured inserting the item."}, 500 # Internal server error
        return item.json(), 201

    @jwt_required()
    def delete(self, name: str) -> str:
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, name: str) -> str:
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data["price"]
        
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self) -> str:
        return {"items": [x.json() for x in ItemModel.find_all()]}
        # return {"items": list(map(lambda x: x.json(), ItemModel.query.al()))}
