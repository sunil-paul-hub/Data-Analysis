import random
from schema import session, Customer, Sales, Product, Transactions, Store, Location, log_changes

# Simulate data changes (insert, update, delete)
def simulate_data_changes():
    # Choose a random table
    table = random.choice([Customer, Sales, Product, Transactions, Store, Location])
    action = random.choice(['insert', 'update', 'delete'])

    if action == 'insert':
        insert_random_data(table)
    elif action == 'update':
        update_random_data(table)
    elif action == 'delete':
        delete_random_data(table)

def insert_random_data(table):
    # Insert fake data
    if table == Customer:
        record = Customer(customer_id=random.randint(1000, 9999), name=f"New Customer {random.randint(1, 100)}")
    elif table == Sales:
        record = Sales(receipt_id=random.randint(1000, 9999), amount=random.randint(10, 500))
    elif table == Product:
        record = Product(product_id=random.randint(1000, 9999), name=f"New Product {random.randint(1, 100)}")
    elif table == Transactions:
        record = Transactions(transaction_id=random.randint(1000, 9999), amount=random.randint(10, 500))
    elif table == Store:
        record = Store(store_id=random.randint(1000, 9999), name=f"New Store {random.randint(1, 100)}")
    elif table == Location:
        record = Location(location_id=random.randint(1000, 9999), name=f"New Location {random.randint(1, 100)}")

    session.add(record)
    session.commit()
    log_changes('insert', table.__tablename__, record.__dict__.get('customer_id', record.__dict__.get('receipt_id', 'unknown')))

def update_random_data(table):
    # Update a random record
    record = session.query(table).order_by(random.choice([Customer.customer_id, Sales.receipt_id])).first()
    if record:
        record.name = f"Updated {record.name}" if hasattr(record, 'name') else record.name
        session.commit()
        log_changes('update', table.__tablename__, record.__dict__.get('customer_id', record.__dict__.get('receipt_id', 'unknown')))

def delete_random_data(table):
    # Delete a random record
    record = session.query(table).order_by(random.choice([Customer.customer_id, Sales.receipt_id])).first()
    if record:
        session.delete(record)
        session.commit()
        log_changes('delete', table.__tablename__, record.__dict__.get('customer_id', record.__dict__.get('receipt_id', 'unknown')))
