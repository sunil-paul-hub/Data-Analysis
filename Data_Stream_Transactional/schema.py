import sqlite3
from sqlite3 import Error
from faker import Faker
import random
import os

fake = Faker()

# Function to connect to SQLite database (or create it)
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

# Function to create tables
def create_tables(conn):
    try:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS customer (
                        customer_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT
                    )''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS sales (
                        receipt_id INTEGER PRIMARY KEY,
                        customer_id INTEGER,
                        store_id INTEGER,
                        total DECIMAL(10, 2),
                        FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
                        FOREIGN KEY (store_id) REFERENCES store(store_id)
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS product (
                        product_id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        price DECIMAL(10, 2)
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        transaction_id INTEGER PRIMARY KEY,
                        product_id INTEGER,
                        sale_id INTEGER,
                        quantity INTEGER,
                        FOREIGN KEY (product_id) REFERENCES product(product_id),
                        FOREIGN KEY (sale_id) REFERENCES sales(receipt_id)
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS store (
                        store_id INTEGER PRIMARY KEY,
                        store_name TEXT NOT NULL,
                        location_id INTEGER
                    )''')

        c.execute('''CREATE TABLE IF NOT EXISTS location (
                        location_id INTEGER PRIMARY KEY,
                        address TEXT
                    )''')

        conn.commit()
    except Error as e:
        print(e)

# Function to insert fake data with randomness (duplicates, missing data, junk)
def insert_fake_data(conn):
    c = conn.cursor()
    # Insert fake customers
    for _ in range(10):
        c.execute("INSERT INTO customer (name, email) VALUES (?, ?)", 
                  (fake.name(), fake.email()))

    # Insert fake stores
    for _ in range(5):
        c.execute("INSERT INTO store (store_name, location_id) VALUES (?, ?)", 
                  (fake.company(), random.randint(1, 5)))

    # Insert fake products
    for _ in range(20):
        c.execute("INSERT INTO product (name, price) VALUES (?, ?)", 
                  (fake.word(), round(random.uniform(1, 100), 2)))

    conn.commit()
