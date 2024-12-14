import random
import time
import threading
import logging
from schema import db, Customer, Product, Store, Location, Sales, Transaction

# Setup logging
logging.basicConfig(filename='logs/app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Log data changes (insert, update, delete)
def log_change(change_type, table, record_id):
    logging.info(f"{change_type} operation on {table} with ID {record_id}")

# Insert a random record into the database
def insert_random_record():
    random_choice = random.choice([Customer, Product, Store, Location, Sales, Transaction])
    record = random_choice(name="Random Record")  # Simple example for all tables
    db.session.add(record)
    db.session.commit()
    log_change("INSERT", random_choice.__name__, record.id)

# Delete a random record from the database
def delete_random_record():
    random_choice = random.choice([Customer, Product, Store, Location, Sales, Transaction])
    record = random_choice.query.order_by(db.func.random()).first()
    if record:
        db.session.delete(record)
        db.session.commit()
        log_change("DELETE", random_choice.__name__, record.id)

# Update a random record
def update_random_record():
    random_choice = random.choice([Customer, Product, Store, Location, Sales, Transaction])
    record = random_choice.query.order_by(db.func.random()).first()
    if record:
        record.name = f"Updated {record.name}"
        db.session.commit()
        log_change("UPDATE", random_choice.__name__, record.id)

# Function to simulate data changes every minute
def simulate_data_changes():
    while True:
        time.sleep(60)
        action = random.choice([insert_random_record, delete_random_record, update_random_record])
        action()

# Thread to run background data simulation
def run_data_simulation():
    thread = threading.Thread(target=simulate_data_changes)
    thread.daemon = True
    thread.start()
