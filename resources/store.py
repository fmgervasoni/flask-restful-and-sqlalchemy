from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name:str):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store not found"}, 404

    def post(self, name:str) -> tuple:
        if StoreModel.find_by_name(name):
            return {f"message": "A store with name {} already exists"}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error ocurred while creating the store"}, 500
        return store.json(), 201

    def delete(self, name:str) -> tuple:
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": "Store deleted"}, 200
        else:
            return {"message": "Store not found"}, 400
        

class StoreList(Resource):
    def get(self):
        return {"stores": [store.json() for store in StoreModel.find_all()]}
