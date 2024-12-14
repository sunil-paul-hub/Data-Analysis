from flask import Flask, jsonify, render_template
from schema import create_connection, create_tables, get_table_stats, get_table_data
import threading
import logging
from data_simulation import simulation_thread

app = Flask(__name__)

# Set up SQLite connection and create tables
conn = create_connection("app.db")
create_tables(conn)

# Endpoint to get row count for each table
@app.route('/table_stats', methods=['GET'])
def table_stats():
    stats = get_table_stats(conn)
    return jsonify(stats)

# Endpoint to get data from any table in JSON format
@app.route('/table_data/<table_name>', methods=['GET'])
def table_data(table_name):
    if table_name not in ['customer', 'sales', 'product', 'transactions', 'store', 'location']:
        return jsonify({"error": "Invalid table name"}), 400
    data = get_table_data(conn, table_name)
    return jsonify(data)

# Index page showing table stats
@app.route('/')
def index():
    stats = get_table_stats(conn)
    return render_template('index.html', stats=stats)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
