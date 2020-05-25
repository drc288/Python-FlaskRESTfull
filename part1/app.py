#!/usr/bin/python3.8
"""
Items - Property for the end point /item/<string:name>
ItemList - Property for the end point /items
"""
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = "My_secret"
api = Api(app)  # Activate the Resource in the app, using api
jwt = JWT(app, authenticate, identity)  # /auth

items = []


class Items(Resource):

    def __init__(self):
        """
        Constructor - initialice the parser request, to add more security
        """
        parser = reqparse.RequestParser()
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help="This filed cannot be left blank!"
                            )
        self.parse = parser.parse_args()

    def get(self, name: str) -> tuple:
        """
        GET - This should return a list items in Json format
        :param name: name to get in the database
        :return: one object or error if not found
        """
        item = next(filter(lambda x: x['name'] == name, items), None)  # for x in items if x['name'] == name else None
        return {'item': item}, 200 if item is not None else 404

    def post(self, name: str) -> dict or tuple:
        """
        POST - This will be create one item.
        If the item aredy exists, Error
        :param name: name to create
        :return: the object
        """
        if next(filter(lambda x: x['name'] == name, items), None):
            return {"Message": f"An item with the name {name} already exists"}, 400
        data = self.parse
        item = {
            'name': name,
            'price': data['price']
        }
        items.append(item)
        return item, 201

    def delete(self, name):
        """
        DELETE - Delete a spesific object in the database
        :param name: name of the object to will be delete
        :return: message
        """
        global items  # Call the items variable in the head of the file
        items = list(filter(lambda x: x['name'] != name, items))
        return {"Message": "Item delete"}

    def put(self, name) -> tuple:
        """
        PUT - Update or create a item in the database
        :param name: name of the object to will be update or create
        :return: a object
        """
        data = self.parse
        update = next(filter(lambda x: x['name'] == name, items), None)
        if update is not None:
            update['price'] = data['price']
            return update, 202
        item = {
            "name": name,
            "price": data["price"]
        }
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self) -> dict:
        """
        GET - Get all the items
        :return: Json representation
        """
        return {'items': items}


api.add_resource(Items, "/item/<string:name>")  # http://127.0.0.1:5000/student/David
api.add_resource(ItemList, "/items")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
