from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import random
import logging

Base = declarative_base()

# Define the database models (tables)
class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    name = Column(String)

class Sales(Base):
    __tablename__ = 'sales'
    receipt_id = Column(Integer, primary_key=True)
    amount = Column(Integer)

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    name = Column(String)

class Transactions(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    amount = Column(Integer)

class Store(Base):
    __tablename__ = 'stores'
    store_id = Column(Integer, primary_key=True)
    name = Column(String)

class Location(Base):
    __tablename__ = 'locations'
    location_id = Column(Integer, primary_key=True)
    name = Column(String)

# Set up the database connection
DATABASE_URL = "sqlite:///mydatabase.db"  # Change this for your actual DB
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Function to create tables
def create_tables():
    Base.metadata.create_all(engine)

# Function to insert fake data
def insert_fake_data():
    customers = [Customer(customer_id=i, name=f"Customer {i}") for i in range(1, 6)]
    sales = [Sales(receipt_id=i, amount=random.randint(10, 500)) for i in range(1, 6)]
    products = [Product(product_id=i, name=f"Product {i}") for i in range(1, 6)]
    transactions = [Transactions(transaction_id=i, amount=random.randint(10, 500)) for i in range(1, 6)]
    stores = [Store(store_id=i, name=f"Store {i}") for i in range(1, 6)]
    locations = [Location(location_id=i, name=f"Location {i}") for i in range(1, 6)]

    session.add_all(customers + sales + products + transactions + stores + locations)
    session.commit()

def log_changes(action, table_name, record_id):
    logging.basicConfig(filename='logs/app.log', level=logging.INFO)
    logging.info(f'{action} on {table_name}: {record_id}')
