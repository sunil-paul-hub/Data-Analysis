from flask import Flask, render_template, jsonify
from threading import Thread
import time
from data_simulation import simulate_data_changes
from schema import create_tables, insert_fake_data, log_changes

app = Flask(__name__)

# Run the background data simulation every minute
def background_task():
    while True:
        simulate_data_changes()
        time.sleep(60)  # Sleep for 1 minute

# Initialize DB and log system
create_tables()
insert_fake_data()

# Start the background simulation thread
thread = Thread(target=background_task)
thread.daemon = True
thread.start()

@app.route('/')
def index():
    # Show index page with stats
    return render_template('index.html', stats=get_db_stats())

@app.route('/api/data', methods=['GET'])
def get_data():
    # Endpoint to get JSON data for the tables
    data = {
        'customers': get_customers(),
        'sales': get_sales(),
        'products': get_products(),
        'transactions': get_transactions(),
        'stores': get_stores(),
        'locations': get_locations(),
    }
    return jsonify(data)

def get_db_stats():
    # Return stats for the index page (could be row counts or other metrics)
    return {
        'customers': count_rows('customers'),
        'sales': count_rows('sales'),
        'products': count_rows('products'),
        'transactions': count_rows('transactions'),
        'stores': count_rows('stores'),
        'locations': count_rows('locations'),
    }

# Database interaction functions
def count_rows(table_name):
    # Helper function to count rows in a table
    pass

def get_customers():
    pass

def get_sales():
    pass

def get_products():
    pass

def get_transactions():
    pass

def get_stores():
    pass

def get_locations():
    pass

if __name__ == '__main__':
    app.run(debug=True)
