# app.py

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

# Routes

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict() for restaurant in restaurants])

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    print(f"Fetching details for restaurant ID: {id}") 
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify(restaurant.to_dict(include_pizzas=True))
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict() for pizza in pizzas])

@app.route('/pizzas/<int:id>', methods=['GET'])
def get_pizza(id):
    pizza = Pizza.query.get(id)
    if pizza:
        return jsonify(pizza.to_dict())
    else:
        return jsonify({'error': 'Pizza not found'}), 404

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.json
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')

    if not all([price, pizza_id, restaurant_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Validate price range
    if not (1 <= price <= 30):
        return jsonify({'error': 'Price must be between 1 and 30'}), 400

    pizza = Pizza.query.get(pizza_id)
    restaurant = Restaurant.query.get(restaurant_id)

    if not pizza or not restaurant:
        return jsonify({'error': 'Pizza or Restaurant not found'}), 404

    restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
    db.session.add(restaurant_pizza)
    db.session.commit()

    return jsonify(restaurant_pizza.to_dict()), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
