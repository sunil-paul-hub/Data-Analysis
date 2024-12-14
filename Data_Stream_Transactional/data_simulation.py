import random
import time
import logging
import threading
import os
from schema import create_connection

# Ensure the logs directory exists
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(filename='logs/app.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

DB_PATH = 'app.db'
conn = create_connection(DB_PATH)

# Log database changes
def log_change(action, table, record_id):
    logging.info(f'{action} - Table: {table}, Record ID: {record_id}')

# Function to delete random record for simulation
def delete_random_record(conn):
    tables = ['customer', 'sales', 'product', 'transactions', 'store', 'location']
    table = random.choice(tables)
    c = conn.cursor()
    c.execute(f"DELETE FROM {table} WHERE rowid = (SELECT rowid FROM {table} ORDER BY RANDOM() LIMIT 1)")
    conn.commit()
    log_change('Delete', table, 'Random')

# Function to simulate data changes (insert, update, delete)
def simulate_data_changes():
    while True:
        action = random.choice(['insert', 'update', 'delete'])
        table = random.choice(['customer', 'sales', 'product', 'transactions', 'store', 'location'])
        
        if action == 'insert':
            log_change('Insert', table, random.randint(1, 1000))

        elif action == 'update':
            log_change('Update', table, random.randint(1, 1000))

        elif action == 'delete':
            delete_random_record(conn)
            log_change('Delete', table, random.randint(1, 1000))

        time.sleep(60)  # simulate data changes every minute

# Thread to run data simulation in the background
def start_simulation_thread():
    simulation_thread = threading.Thread(target=simulate_data_changes)
    simulation_thread.daemon = True
    simulation_thread.start()
