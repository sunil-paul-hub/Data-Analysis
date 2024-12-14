from flask import Flask, jsonify, render_template
from schema import db, init_db, insert_fake_data
from data_simulation import run_data_simulation
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# Initialize the database
@app.before_request
def before_request():
    # Check if the database exists and initialize it if needed
    if not os.path.exists('app.db'):
        init_db()  # Create the database and tables
        insert_fake_data()  # Populate it with some initial data
    # Start the background simulation if it hasn't started yet
    if not hasattr(app, 'data_simulation_thread'):
        run_data_simulation()  # Start the background thread for data simulation
        app.data_simulation_thread = True

# Home route to show index page with table stats
@app.route('/')
def index():
    customers = Customer.query.count()
    products = Product.query.count()
    stores = Store.query.count()
    locations = Location.query.count()
    sales = Sales.query.count()
    transactions = Transaction.query.count()

    return render_template('index.html', customers=customers, products=products,
                           stores=stores, locations=locations, sales=sales, transactions=transactions)


# API endpoint to get JSON dataset of all tables
@app.route('/api/data')
def api_data():
    data = {
        "customers": [customer.name for customer in Customer.query.all()],
        "products": [product.name for product in Product.query.all()],
        "stores": [store.store_id for store in Store.query.all()],
        "locations": [location.address for location in Location.query.all()],
        "sales": [sale.amount for sale in Sales.query.all()],
        "transactions": [transaction.amount for transaction in Transaction.query.all()]
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
