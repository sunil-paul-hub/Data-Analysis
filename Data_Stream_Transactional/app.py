import random
import sqlite3
import threading
from datetime import datetime
from flask import Flask, jsonify
from faker import Faker
import time

# Initialize Flask app
app = Flask(__name__)

# Initialize Faker for generating fake data
fake = Faker()

# Connect to SQLite database (or create it)
conn = sqlite3.connect('fake_data.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables function
def create_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS customer (
                        customer_id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT,
                        phone TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                        receipt_id INTEGER PRIMARY KEY,
                        customer_id INTEGER,
                        total_amount REAL,
                        date TEXT,
                        FOREIGN KEY (customer_id) REFERENCES customer(customer_id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS product (
                        product_id INTEGER PRIMARY KEY,
                        name TEXT,
                        price REAL,
                        description TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        transaction_id INTEGER PRIMARY KEY,
                        receipt_id INTEGER,
                        product_id INTEGER,
                        quantity INTEGER,
                        FOREIGN KEY (receipt_id) REFERENCES sales(receipt_id),
                        FOREIGN KEY (product_id) REFERENCES product(product_id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS store (
                        store_id INTEGER PRIMARY KEY,
                        name TEXT,
                        location_id INTEGER,
                        FOREIGN KEY (location_id) REFERENCES location(location_id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS location (
                        location_id INTEGER PRIMARY KEY,
                        city TEXT,
                        state TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS change_log (
                        log_id INTEGER PRIMARY KEY,
                        action TEXT,
                        table_name TEXT,
                        record_id INTEGER,
                        timestamp TEXT)''')

    conn.commit()

# Function to insert fake data with randomness (duplicates, missing data, junk)
def insert_fake_data():
    # Insert customers
    for _ in range(5):  # Insert a small number for testing
        if random.random() < 0.1:
            name = None  # Missing data
        else:
            name = fake.name()
        email = fake.email() if random.random() > 0.1 else None  # 10% missing emails
        phone = fake.phone_number() if random.random() > 0.2 else "junk_phone"  # Junk phone numbers

        cursor.execute('''INSERT INTO customer (name, email, phone) VALUES (?, ?, ?)''',
                       (name, email, phone))

    # Insert sales
    for _ in range(5):  # Insert a small number for testing
        customer_id = random.randint(1, 5)  # Simulating up to 5 customers
        total_amount = round(random.uniform(10.0, 500.0), 2)
        date = fake.date_this_year()
        cursor.execute('''INSERT INTO sales (customer_id, total_amount, date) VALUES (?, ?, ?)''',
                       (customer_id, total_amount, date))

    # Insert products
    for _ in range(3):  # Insert a small number for testing
        name = fake.word()
        price = round(random.uniform(5.0, 100.0), 2)
        description = fake.sentence()
        cursor.execute('''INSERT INTO product (name, price, description) VALUES (?, ?, ?)''',
                       (name, price, description))

    # Insert transactions
    for _ in range(5):  # Insert a small number for testing
        receipt_id = random.randint(1, 5)
        product_id = random.randint(1, 3)
        quantity = random.randint(1, 10)
        cursor.execute('''INSERT INTO transactions (receipt_id, product_id, quantity) VALUES (?, ?, ?)''',
                       (receipt_id, product_id, quantity))

    # Insert locations
    for _ in range(2):  # Insert a small number for testing
        city = fake.city()
        state = fake.state()
        cursor.execute('''INSERT INTO location (city, state) VALUES (?, ?)''',
                       (city, state))

    # Insert stores
    for _ in range(2):  # Insert a small number for testing
        name = fake.company()
        location_id = random.randint(1, 2)
        cursor.execute('''INSERT INTO store (name, location_id) VALUES (?, ?)''',
                       (name, location_id))

    # Commit changes
    conn.commit()

# Function to log changes (insert, update, delete)
def log_change(action, table_name, record_id):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''INSERT INTO change_log (action, table_name, record_id, timestamp) VALUES (?, ?, ?, ?)''',
                   (action, table_name, record_id, timestamp))
    conn.commit()

# Function to delete random record (for simulation of delete actions)
def delete_random_record():
    table_names = ['customer', 'sales', 'product', 'transactions', 'store', 'location']
    table_name = random.choice(table_names)
    cursor.execute(f'SELECT {table_name}_id FROM {table_name}')
    ids = cursor.fetchall()
    if ids:
        record_id = random.choice(ids)[0]
        cursor.execute(f'DELETE FROM {table_name} WHERE {table_name}_id = ?', (record_id,))
        log_change('delete', table_name, record_id)
        conn.commit()

# Function to simulate data changes (insert, update, delete) every minute
def simulate_data_changes():
    while True:
        insert_fake_data()  # Insert new fake data
        if random.random() < 0.1:
            delete_random_record()  # Random delete action
        time.sleep(60)  # Wait for 1 minute before making another change

# Thread to run the background data simulation
def start_data_simulation_thread():
    simulation_thread = threading.Thread(target=simulate_data_changes)
    simulation_thread.daemon = True
    simulation_thread.start()

# Endpoint to get row count for each table
def get_table_row_count():
    cursor.execute('''SELECT COUNT(*) FROM customer''')
    customer_count = cursor.fetchone()[0]

    cursor.execute('''SELECT COUNT(*) FROM sales''')
    sales_count = cursor.fetchone()[0]

    cursor.execute('''SELECT COUNT(*) FROM product''')
    product_count = cursor.fetchone()[0]

    cursor.execute('''SELECT COUNT(*) FROM transactions''')
    transactions_count = cursor.fetchone()[0]

    cursor.execute('''SELECT COUNT(*) FROM store''')
    store_count = cursor.fetchone()[0]

    cursor.execute('''SELECT COUNT(*) FROM location''')
    location_count = cursor.fetchone()[0]

    return {
        'customer': customer_count,
        'sales': sales_count,
        'product': product_count,
        'transactions': transactions_count,
        'store': store_count,
        'location': location_count
    }

# Flask Routes
@app.route('/total_rows', methods=['GET'])
def total_rows():
    row_counts = get_table_row_count()
    return jsonify(row_counts)

@app.route('/customers', methods=['GET'])
def customers():
    cursor.execute('SELECT * FROM customer')
    customers_data = cursor.fetchall()
    return jsonify(customers_data)

@app.route('/sales', methods=['GET'])
def sales():
    cursor.execute('SELECT * FROM sales')
    sales_data = cursor.fetchall()
    return jsonify(sales_data)

@app.route('/products', methods=['GET'])
def products():
    cursor.execute('SELECT * FROM product')
    products_data = cursor.fetchall()
    return jsonify(products_data)

@app.route('/transactions', methods=['GET'])
def transactions():
    cursor.execute('SELECT * FROM transactions')
    transactions_data = cursor.fetchall()
    return jsonify(transactions_data)

@app.route('/stores', methods=['GET'])
def stores():
    cursor.execute('SELECT * FROM store')
    stores_data = cursor.fetchall()
    return jsonify(stores_data)

@app.route('/locations', methods=['GET'])
def locations():
    cursor.execute('SELECT * FROM location')
    locations_data = cursor.fetchall()
    return jsonify(locations_data)

# Main method to start the Flask app and the data simulation thread
if __name__ == '__main__':
    create_tables()  # Create the tables at startup
    start_data_simulation_thread()  # Start background data simulation in a thread
    app.run(debug=True, use_reloader=False)  # Disable reloader to prevent starting the thread twice
