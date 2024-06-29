# models.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()
class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='restaurant')

    def to_dict(self, include_pizzas=False):
        restaurant_dict = {
            'id': self.id,
            'name': self.name,
            'location': self.location
        }

        if include_pizzas:
            restaurant_dict['restaurant_pizzas'] = [rp.to_dict() for rp in self.restaurant_pizzas]

        return restaurant_dict

class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)

    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients
        }

class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))

    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')

    @validates('price')
    def validate_price(self, key, price):
        if not (1 <= price <= 30):
            raise ValueError("Price must be between 1 and 30.")
        return price

    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id,
            'pizza': self.pizza.to_dict(),
            'restaurant': self.restaurant.to_dict()
        }
