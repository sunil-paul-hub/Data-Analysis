import threading
from schema import simulate_data_changes, create_connection

# Function to start the data simulation thread
def start_data_simulation():
    conn = create_connection("app.db")
    simulate_data_changes(conn)

simulation_thread = threading.Thread(target=start_data_simulation, daemon=True)
simulation_thread.start()
