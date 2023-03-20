#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/restaurants', methods = ['GET', 'POST'])
def restaurants():
    
    if request.method == 'GET':
        restaurants = Restaurant.query.all()
        restaurants_dict = [restaurant.to_dict() for restaurant in restaurants]
        response = make_response(
            jsonify(restaurants_dict),
            200,
        )
    return response
    

@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    pizzas = RestaurantPizza.query.filter_by(restaurant_id = id).all()
    pizza_dict = [pizza.pizza.to_dict() for pizza in pizzas]

    if not restaurant:
        error = {"error": "Restaurant not found"}
        reponse = make_response(
            jsonify(error),
            404,
        )
        return reponse
    
    if request.method == 'GET':
        restaurant_dict = restaurant.to_dict()
        pizza_resp = {"pizzas": pizza_dict}
        restaurant_dict.update(pizza_resp)
        get_response = make_response(
            jsonify(restaurant_dict),
            200,
        )
        return get_response

@app.route('/pizzas')
def pizzas():
    pizzas = [pizza for pizza in Pizza.query.all()]

    response = make_response(
        jsonify(pizzas),
        200,
    )

    return response

@app.route('/restaurant_pizzas')
def restaurant_pizzas():
    data = request.get_json()
    new_rest_pizza = RestaurantPizza()

    for field in data:
        setattr(new_rest_pizza, field, data)

    db.session.add(new_rest_pizza)
    db.session.commit()

    if not new_rest_pizza:
        error = {"errors": "['validation errors']"}
        error_response = make_response(
            jsonify(error),
            404,
        )
        return error_response

    response = make_response(
            jsonify(new_rest_pizza.pizza),
            202,
        )
    return response
    



if __name__ == '__main__':
    app.run(port=5555)
