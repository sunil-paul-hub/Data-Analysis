import sqlite3
import random
import time
import logging
from datetime import datetime

# Set up logging to file
logging.basicConfig(filename='logs/app.log', level=logging.INFO)

# Function to connect to SQLite database (allowing multi-threading)
def create_connection(db_file="app.db"):
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except sqlite3.Error as e:
        logging.error(f"Error creating connection: {e}")
        return None

# Create tables in the database
def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        receipt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        amount REAL,
        FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        price REAL
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        receipt_id INTEGER,
        product_id INTEGER,
        quantity INTEGER,
        FOREIGN KEY(receipt_id) REFERENCES sales(receipt_id),
        FOREIGN KEY(product_id) REFERENCES product(product_id)
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS store (
        store_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS location (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER,
        address TEXT,
        FOREIGN KEY(store_id) REFERENCES store(store_id)
    );
    """)
    conn.commit()

# Insert fake data with randomness
def insert_fake_data(conn):
    cursor = conn.cursor()
    customers = ["Alice", "Bob", "Charlie", "David", "Eva"]
    products = ["Product A", "Product B", "Product C", "Product D"]
    stores = ["Store 1", "Store 2", "Store 3"]

    customer_name = random.choice(customers)
    cursor.execute("INSERT INTO customer (name, email) VALUES (?, ?)", (customer_name, f"{customer_name.lower()}@example.com"))
    customer_id = cursor.lastrowid

    product_name = random.choice(products)
    cursor.execute("INSERT INTO product (name, price) VALUES (?, ?)", (product_name, random.uniform(5, 100)))
    product_id = cursor.lastrowid

    cursor.execute("INSERT INTO store (name) VALUES (?)", (random.choice(stores),))
    store_id = cursor.lastrowid

    cursor.execute("INSERT INTO location (store_id, address) VALUES (?, ?)", (store_id, f"Address {random.randint(1, 100)}"))
    
    # Simulate sales and transactions
    cursor.execute("INSERT INTO sales (customer_id, amount) VALUES (?, ?)", (customer_id, random.uniform(20, 200)))
    receipt_id = cursor.lastrowid
    cursor.execute("INSERT INTO transactions (receipt_id, product_id, quantity) VALUES (?, ?, ?)", 
                   (receipt_id, product_id, random.randint(1, 5)))
    
    conn.commit()

# Log changes (insert, update, delete)
def log_change(action, table, record_id):
    logging.info(f"{datetime.now()} - {action} {table} with ID {record_id}")

# Function to delete a random record (for simulation of delete actions)
def delete_random_record(conn):
    cursor = conn.cursor()
    tables = ['customer', 'sales', 'product', 'transactions', 'store', 'location']
    table = random.choice(tables)
    cursor.execute(f"SELECT rowid FROM {table} ORDER BY RANDOM() LIMIT 1")
    row = cursor.fetchone()
    
    if row:
        row_id = row[0]
        cursor.execute(f"DELETE FROM {table} WHERE rowid = ?", (row_id,))
        conn.commit()
        log_change("DELETE", table, row_id)

# Simulate data changes (insert, update, delete) every minute
def simulate_data_changes(conn):
    while True:
        action = random.choice(['insert', 'update', 'delete'])
        if action == 'insert':
            insert_fake_data(conn)
            log_change("INSERT", "various", "N/A")
        elif action == 'update':
            # You can add an update simulation here
            pass
        elif action == 'delete':
            delete_random_record(conn)
        time.sleep(60)  # Simulate data changes every minute

# Function to get row count for each table
def get_table_stats(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    stats = {}
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        stats[table_name] = count
    return stats

# Function to get data from any table in JSON format
def get_table_data(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    return [dict(zip(columns, row)) for row in rows]
