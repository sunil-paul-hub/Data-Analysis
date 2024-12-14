import os
import threading
import time
import random
from schema import db, Customer, Sales, Product, Transactions, Store, Location
import logging

# Ensure the 'logs' directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')
    
# Setup logging
logging.basicConfig(filename='logs/data_simulation.log', level=logging.INFO)

def log_change(action, table, record_id):
    logging.info(f"Action: {action}, Table: {table}, Record ID: {record_id}, Time: {time.ctime()}")

# Function to simulate data changes (insert, update, delete)
def simulate_data_changes():
    while True:
        action = random.choice(['insert', 'update', 'delete'])
        table = random.choice([Customer, Sales, Product, Transactions, Store, Location])

        if action == 'insert':
            # Insert random data
            record = table(name="Random " + str(random.randint(1000, 9999))) if table == Customer else table()
            db.session.add(record)
            db.session.commit()
            log_change('insert', table.__name__, record.id)

        elif action == 'update':
            # Update random record
            record = table.query.first()
            if record:
                record.name = "Updated " + str(random.randint(1000, 9999))
                db.session.commit()
                log_change('update', table.__name__, record.id)

        elif action == 'delete':
            # Delete random record
            record = table.query.first()
            if record:
                db.session.delete(record)
                db.session.commit()
                log_change('delete', table.__name__, record.id)

        time.sleep(60)  # Wait for 1 minute

# Run the data simulation in a background thread
def start_simulation_thread():
    simulation_thread = threading.Thread(target=simulate_data_changes)
    simulation_thread.daemon = True  # Allow thread to exit when main program exits
    simulation_thread.start()
