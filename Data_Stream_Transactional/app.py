from flask import Flask, render_template, jsonify
from schema import db, init_db, insert_fake_data
from data_simulation import start_simulation_thread

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    # Fetch table statistics
    customers_count = Customer.query.count()
    sales_count = Sales.query.count()
    product_count = Product.query.count()
    transaction_count = Transactions.query.count()
    store_count = Store.query.count()
    location_count = Location.query.count()

    return render_template('index.html', customers_count=customers_count,
                           sales_count=sales_count, product_count=product_count,
                           transaction_count=transaction_count, store_count=store_count,
                           location_count=location_count)

@app.route('/data/customers')
def get_customers():
    customers = Customer.query.all()
    return jsonify([customer.name for customer in customers])

@app.route('/data/sales')
def get_sales():
    sales = Sales.query.all()
    return jsonify([{'receipt_id': sale.receipt_id, 'customer_id': sale.customer_id, 'amount': sale.amount} for sale in sales])

@app.route('/data/products')
def get_products():
    products = Product.query.all()
    return jsonify([product.name for product in products])

if __name__ == "__main__":
    with app.app_context():
        init_db()  # Create tables if not already created
        insert_fake_data()  # Insert initial fake data
        start_simulation_thread()  # Start the background data simulation
    app.run(debug=True, host='0.0.0.0', port=5000)
