import random
import time
import logging
import threading
from datetime import datetime
from schema import create_connection, insert_fake_data

logging.basicConfig(filename='logs/app.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

DB_PATH = 'app.db'
conn = create_connection(DB_PATH)

# Log database changes
def log_change(action, table, record_id):
    logging.info(f'{action} - Table: {table}, Record ID: {record_id}')

# Function to simulate data changes (insert, update, delete)
def simulate_data_changes():
    while True:
        action = random.choice(['insert', 'update', 'delete'])
        table = random.choice(['customer', 'sales', 'product', 'transactions', 'store', 'location'])
        
        # Perform Insert
        if action == 'insert':
            log_change('Insert', table, random.randint(1, 1000))

        # Perform Update
        elif action == 'update':
            log_change('Update', table, random.randint(1, 1000))

        # Perform Delete
        elif action == 'delete':
            log_change('Delete', table, random.randint(1, 1000))

        time.sleep(60)  # simulate data changes every minute

# Thread to run data simulation in the background
def start_simulation_thread():
    simulation_thread = threading.Thread(target=simulate_data_changes)
    simulation_thread.daemon = True
    simulation_thread.start()
