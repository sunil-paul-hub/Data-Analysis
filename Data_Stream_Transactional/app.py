from flask import Flask, jsonify, render_template
from schema import create_connection, create_tables, insert_fake_data
from data_simulation import start_simulation_thread

app = Flask(__name__)

# Database initialization
DB_PATH = 'app.db'
conn = create_connection(DB_PATH)
create_tables(conn)
insert_fake_data(conn)

# Endpoint to get row count for each table
@app.route('/row_count', methods=['GET'])
def get_row_count():
    cursor = conn.cursor()
    row_counts = {}
    tables = ['customer', 'sales', 'product', 'transactions', 'store', 'location']
    for table in tables:
        cursor.execute(f'SELECT COUNT(*) FROM {table}')
        row_counts[table] = cursor.fetchone()[0]
    return jsonify(row_counts)

# Index route (renders the HTML page)
@app.route('/')
def index():
    return render_template('index.html')

# Main method to start the Flask app and the data simulation thread
if __name__ == '__main__':
    start_simulation_thread()
    app.run(host='0.0.0.0', port=5000)
