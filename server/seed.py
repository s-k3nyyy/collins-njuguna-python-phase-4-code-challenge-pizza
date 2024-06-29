from app import app, db
from models import RestaurantPizza, Restaurant, Pizza

def seed_database():
    with app.app_context():
        # Delete existing data
        db.session.query(RestaurantPizza).delete()
        db.session.query(Pizza).delete()
        db.session.query(Restaurant).delete()

        # Create new data
        restaurant1 = Restaurant(name="Karen's Pizza Shack", location="address1")
        restaurant2 = Restaurant(name="Sanjay's Pizza", location="address2")
        restaurant3 = Restaurant(name="Kiki's Pizza", location="address3")

        pizza1 = Pizza(name='Emma', ingredients='Dough, Tomato Sauce, Cheese')
        pizza2 = Pizza(name='Geri', ingredients='Dough, Tomato Sauce, Cheese, Pepperoni')
        pizza3 = Pizza(name='Melanie', ingredients='Dough, Sauce, Ricotta, Red peppers, Mustard')

        restaurant_pizza1 = RestaurantPizza(restaurant=restaurant1, pizza=pizza1, price=10.5)
        restaurant_pizza2 = RestaurantPizza(restaurant=restaurant2, pizza=pizza2, price=12.0)
        restaurant_pizza3 = RestaurantPizza(restaurant=restaurant3, pizza=pizza3, price=15.75)

        db.session.add_all([restaurant1, restaurant2, restaurant3, pizza1, pizza2, pizza3,
                            restaurant_pizza1, restaurant_pizza2, restaurant_pizza3])
        db.session.commit()

        print('Database seeded!')

if __name__ == '__main__':
    seed_database()
