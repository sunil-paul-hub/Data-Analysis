from flask_sqlalchemy import SQLAlchemy
import random
from faker import Faker

db = SQLAlchemy()

class Customer(db.Model):
    customer_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Store(db.Model):
    store_id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer)

class Location(db.Model):
    location_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100))

class Sales(db.Model):
    receipt_id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))
    product = db.relationship('Product', backref='sales')

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.customer_id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.store_id'))
    amount = db.Column(db.Float)

# Function to initialize the database
def init_db():
    db.create_all()

# Function to insert fake data
def insert_fake_data():
    fake = Faker()
    for _ in range(10):
        customer = Customer(name=fake.name())
        product = Product(name=fake.word())
        store = Store(location_id=random.randint(1, 5))
        location = Location(address=fake.address())
        transaction = Transaction(
            customer_id=random.randint(1, 10),
            store_id=random.randint(1, 10),
            amount=random.uniform(10, 100)
        )
        sales = Sales(
            receipt_id=random.randint(1, 100),
            amount=random.uniform(10, 100),
            product_id=random.randint(1, 10)
        )
        db.session.add(customer)
        db.session.add(product)
        db.session.add(store)
        db.session.add(location)
        db.session.add(transaction)
        db.session.add(sales)
    db.session.commit()
