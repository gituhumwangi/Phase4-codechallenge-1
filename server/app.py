#import necessary modules
from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from model import Restaurant, Pizza, RestaurantPizza, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Restaurants(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Restaurant.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

    def delete(self, id):
        record = Restaurant.query.get(id)

        if record:
            Restaurant.query.filter_by(id=id).delete

            db.session.delete(record)
            db.session.commit()
            response_dict = {"message": "Record successfully deleted"}
            return jsonify(response_dict), 200
        else:
            return {"message": "Not Found"}, 404

api.add_resource(Restaurants, '/restaurants')

class RestaurantById(Resource):
    def get(self, id):
        record = Restaurant.query.filter_by(id=id).first()

        if record:
            return make_response(jsonify(record.to_dict()), 200)
        else:
            return {"message": "Not Found"}, 404

api.add_resource(RestaurantById, '/restaurants/<int:id>')

class Pizzas(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in Pizza.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):
    def get(self):
        response_dict_list = [n.to_dict() for n in RestaurantPizza.query.all()]

        response = make_response(
            jsonify(response_dict_list),
            200,
        )

        return response

    def post(self):
        data = request.get_json()
        
        price=data.get('price')
        pizza_id=data.get('pizza_id')
        restaurant_id=data.get('restaurant_id')

        if pizza_id and restaurant_id:

            new_record = RestaurantPizza(
                price=price,
                pizza_id=pizza_id,
                restaurant_id=restaurant_id
            )

            db.session.add(new_record)
            db.session.commit()

            pizza = Pizza.query.get(pizza_id)
            if pizza:
                response = make_response(
                    {"id": pizza.id,
                    "ingredients" : pizza.ingredients,
                    "name" : pizza.name},

                    201
                )

                return response
            else:
                return {"Error": "invalid pizza or restaurant id"}

api.add_resource(RestaurantPizzas, '/restaurant_pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
