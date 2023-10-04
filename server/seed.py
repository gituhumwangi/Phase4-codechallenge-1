
#!/usr/bin/env python3

from faker import Faker
import random

from app import app
from model import db, Restaurant, RestaurantPizza, Pizza

fake = Faker()

with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Generate Restaurants
    restaurants = []
    for i in range(12):
        restaurant = Restaurant(
            name=fake.company(),
            address=fake.address(),
        )
        restaurants.append(restaurant)

    db.session.add_all(restaurants)
    db.session.commit()

    # Generate Pizza Ingredients
    random_ingredients = ["Tomato", "Onion", "Garlic", "Basil", "Cucumber", "Lemon", "Mushroom", "Spinach", "Avocado", "Cheddar Cheese"]

    # Define pizza names
    pizza_names = [
        'Margherita Pizza', 'Pepperoni Pizza', "Hawaiian Pizza", "Mushroom Pizza",
        "BBQ Chicken Pizza", "Buffalo Chicken Pizza", "Vegetarian Pizza",
        "Chicago Deep-Dish Pizza", "Neapolitan Pizza", "Sicilian Pizza", "White Pizza"
    ]

    # Generate Pizzas
    pizzas = []
    for i in range(10):
     pizza = Pizza(
        name=random.choice(pizza_names),
        ingredients=', '.join(random.sample(random_ingredients, random.randint(1, len(random_ingredients)))),  # Convert list to string
        created_at=fake.date_time(),
        updated_at=fake.date_time(),
    )
    pizzas.append(pizza)

    db.session.add_all(pizzas)
    db.session.commit()

    # Generate Restaurant Pizzas
    restaurant_pizzas = []
    for restaurant in restaurants:
        for _ in range(13):
            restaurant_pizza = RestaurantPizza(
                price=random.randint(1, 30),
                restaurant_id=restaurant.id,
                pizza_id=random.choice(pizzas).id,
                created_at=fake.date_time(),
                updated_at=fake.date_time(),
            )
            restaurant_pizzas.append(restaurant_pizza)

    db.session.add_all(restaurant_pizzas)
    db.session.commit()



