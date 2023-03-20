#!/usr/bin/env python3

from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/restaurants')
def restaurants():
    rests = [rest for rest in Restaurant.query.all()]

    response = make_response(
        jsonify(rests),
        200,
    )
    
    return response
    

@app.route('/restaurants/<int:id>', methods = ['GET', 'DELETE'])
def restaurant_by_id(id):
    rest = Restaurant.query.filter_by(id=id).first()

    if not rest:
        error = { "error": "Restaurant not found"}

        response = make_response(
            jsonify(error),
            404,
        )
        return response
    
    if request.method == 'GET':
        get_response = make_response(
            jsonify(rest),
            200,
        )
        return get_response
    
    if request.method == 'DELETE':
        rest_pizza = RestaurantPizza.query.filter(RestaurantPizza.restaurant_id == rest.id)
        db.session.delete(rest_pizza)
        db.session.commit()

        db.session.delete(rest)
        db.session.commit()
    

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
