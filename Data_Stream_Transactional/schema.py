from flask_sqlalchemy import SQLAlchemy
import random
from faker import Faker

db = SQLAlchemy()
fake = Faker()

# Database Models

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Sales(db.Model):
    receipt_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    amount = db.Column(db.Float)

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Transactions(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    amount = db.Column(db.Float)

class Store(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('location.location_id'))

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))

# Database Initialization
def init_db():
    db.create_all()

# Function to insert fake data
def insert_fake_data():
    for _ in range(10):
        customer = Customer(name=fake.name())
        db.session.add(customer)
        db.session.commit()

        sales = Sales(receipt_id=random.randint(1, 1000), customer_id=customer.customer_id, amount=random.uniform(10.0, 500.0))
        db.session.add(sales)
        db.session.commit()

        product = Product(name=fake.word())
        db.session.add(product)
        db.session.commit()

        transaction = Transactions(product_id=product.product_id, amount=random.uniform(1.0, 100.0))
        db.session.add(transaction)
        db.session.commit()

        location = Location(city=fake.city())
        db.session.add(location)
        db.session.commit()

        store = Store(location_id=location.location_id)
        db.session.add(store)
        db.session.commit()
