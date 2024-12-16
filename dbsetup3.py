import mysql.connector
from faker import Faker
import random
import uuid

def create_connection():
    try:
        print("Creating connection...")
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="zomato1"
        )
        print("Connection successful!")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def create_tables(connection):
    cursor = connection.cursor()
    print("Creating tables in the database...")

    # Create Customers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customers (
        customer_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255),
        email VARCHAR(255),
        phone VARCHAR(50),
        location TEXT,
        signup_date DATE,
        is_premium BOOLEAN,
        preferred_cuisine VARCHAR(50),
        total_orders INT,
        average_rating FLOAT
    );
    """)

    # Create Restaurants Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Restaurants (
        restaurant_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255),
        cuisine_type VARCHAR(50),
        location TEXT,
        owner_name VARCHAR(255),
        average_delivery_time INT,
        contact_number VARCHAR(50),
        rating FLOAT,
        total_orders INT,
        is_active BOOLEAN
    );
    """)

    # Create Orders Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Orders (
        order_id VARCHAR(36) PRIMARY KEY,
        customer_id VARCHAR(36),
        restaurant_id VARCHAR(36),
        order_date DATETIME,
        delivery_time DATETIME,
        status VARCHAR(50),
        total_amount FLOAT,
        payment_mode VARCHAR(50),
        discount_applied FLOAT,
        feedback_rating FLOAT,
        FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
        FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
    );
    """)

    # Create OrderItems Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS OrderItems (
        order_item_id VARCHAR(36) PRIMARY KEY,
        order_id VARCHAR(36),
        dish_name VARCHAR(255),
        quantity INT,
        price FLOAT,
        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
    );
    """)

    # Create DeliveryPersons Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DeliveryPersons (
        delivery_person_id VARCHAR(36) PRIMARY KEY,
        name VARCHAR(255),
        contact_number VARCHAR(15),
        vehicle_type VARCHAR(50),
        total_deliveries INT,
        average_rating FLOAT,
        location TEXT
    );
    """)

    # Create Deliveries Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Deliveries (
        delivery_id VARCHAR(36) PRIMARY KEY,
        order_id VARCHAR(36),
        delivery_person_id VARCHAR(36),
        delivery_status VARCHAR(50),
        distance FLOAT,
        delivery_time INT,
        estimated_time INT,
        delivery_fee FLOAT,
        vehicle_type VARCHAR(50),
        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
        FOREIGN KEY (delivery_person_id) REFERENCES DeliveryPersons(delivery_person_id)
    );
    """)

    connection.commit()
    print("Tables created successfully!")

def generate_fake_data(connection):
    print("Generating fake data...")
    fake = Faker()

    # Generate Customers Data
    customers = []
    for i in range(100):
        customers.append({
            'customer_id': fake.uuid4(),
            'name': fake.name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'location': fake.address(),
            'signup_date': fake.date_this_decade(),
            'is_premium': fake.boolean(),
            'preferred_cuisine': random.choice(['Indian', 'Chinese', 'Italian', 'Mexican']),
            'total_orders': random.randint(1, 50),
            'average_rating': round(random.uniform(1, 5), 1)
        })

    # Generate Restaurants Data
    restaurants = []
    for i in range(50):
        restaurants.append({
            'restaurant_id': fake.uuid4(),
            'name': fake.company(),
            'cuisine_type': random.choice(['Indian', 'Chinese', 'Italian', 'Mexican']),
            'location': fake.address(),
            'owner_name': fake.name(),
            'average_delivery_time': random.randint(20, 60),
            'contact_number': fake.phone_number(),
            'rating': round(random.uniform(1, 5), 1),
            'total_orders': random.randint(10, 200),
            'is_active': fake.boolean()
        })

    # Generate Orders Data
    orders = []
    for i in range(200):
        orders.append({
            'order_id': fake.uuid4(),
            'customer_id': random.choice(customers)['customer_id'],
            'restaurant_id': random.choice(restaurants)['restaurant_id'],
            'order_date': fake.date_time_this_year(),
            'delivery_time': fake.date_time_this_year(),
            'status': random.choice(['Pending', 'Delivered', 'Cancelled']),
            'total_amount': round(random.uniform(100, 1000), 2),
            'payment_mode': random.choice(['Credit Card', 'Cash', 'UPI']),
            'discount_applied': round(random.uniform(0, 100), 2),
            'feedback_rating': round(random.uniform(1, 5), 1)
        })

    # Generate OrderItems Data
    order_items = []
    for order in orders:
        for _ in range(random.randint(1, 5)):  # Random number of items per order
            order_items.append({
                'order_item_id': fake.uuid4(),
                'order_id': order['order_id'],
                'dish_name': fake.word(),
                'quantity': random.randint(1, 5),
                'price': round(random.uniform(50, 500), 2)
            })

    # Generate DeliveryPersons Data
    delivery_persons = []
    for i in range(30):
        delivery_persons.append({
            'delivery_person_id': fake.uuid4(),
            'name': fake.name(),
            'contact_number': fake.phone_number()[:15],
            'vehicle_type': random.choice(['Bike', 'Car', 'Scooter']),
            'total_deliveries': random.randint(20, 200),
            'average_rating': round(random.uniform(1, 5), 1),
            'location': fake.address()
        })

    # Fetch existing Orders to link delivery data to (order_id)
    cursor = connection.cursor()
    cursor.execute("SELECT order_id FROM Orders")
    order_ids = [row[0] for row in cursor.fetchall()]

    # Generate Deliveries Data
    deliveries = []
    for i in range(100):
        deliveries.append({
            'delivery_id': fake.uuid4(),
            'order_id': random.choice(order_ids),
            'delivery_person_id': random.choice(delivery_persons)['delivery_person_id'],
            'delivery_status': random.choice(['On the way', 'Delivered', 'Pending']),
            'distance': round(random.uniform(1, 20), 2),
            'delivery_time': random.randint(10, 60),
            'estimated_time': random.randint(10, 60),
            'delivery_fee': round(random.uniform(20, 200), 2),
            'vehicle_type': random.choice(['Bike', 'Car', 'Scooter'])
        })

    return customers, restaurants, orders, order_items, delivery_persons, deliveries

def insert_data(connection, table, data):
    try:
        cursor = connection.cursor()
        print(f"Inserting data into {table}...")
        if table == 'Customers':
            cursor.executemany("""
            INSERT INTO Customers (customer_id, name, email, phone, location, signup_date, is_premium, preferred_cuisine, total_orders, average_rating)
            VALUES (%(customer_id)s, %(name)s, %(email)s, %(phone)s, %(location)s, %(signup_date)s, %(is_premium)s, %(preferred_cuisine)s, %(total_orders)s, %(average_rating)s)
            """, data)
        elif table == 'Restaurants':
            cursor.executemany("""
            INSERT INTO Restaurants (restaurant_id, name, cuisine_type, location, owner_name, average_delivery_time, contact_number, rating, total_orders, is_active)
            VALUES (%(restaurant_id)s, %(name)s, %(cuisine_type)s, %(location)s, %(owner_name)s, %(average_delivery_time)s, %(contact_number)s, %(rating)s, %(total_orders)s, %(is_active)s)
            """, data)
        elif table == 'Orders':
            cursor.executemany("""
            INSERT INTO Orders (order_id, customer_id, restaurant_id, order_date, delivery_time, status, total_amount, payment_mode, discount_applied, feedback_rating)
            VALUES (%(order_id)s, %(customer_id)s, %(restaurant_id)s, %(order_date)s, %(delivery_time)s, %(status)s, %(total_amount)s, %(payment_mode)s, %(discount_applied)s, %(feedback_rating)s)
            """, data)
        
        
        elif table == 'DeliveryPersons':
            cursor.executemany("""
            INSERT INTO DeliveryPersons (delivery_person_id, name, contact_number, vehicle_type, total_deliveries, average_rating, location)
            VALUES (%(delivery_person_id)s, %(name)s, %(contact_number)s, %(vehicle_type)s, %(total_deliveries)s, %(average_rating)s, %(location)s)
            """, data)
        elif table == 'Deliveries':
            cursor.executemany("""
            INSERT INTO Deliveries (delivery_id, order_id, delivery_person_id, delivery_status, distance, delivery_time, estimated_time, delivery_fee, vehicle_type)
            VALUES (%(delivery_id)s, %(order_id)s, %(delivery_person_id)s, %(delivery_status)s, %(distance)s, %(delivery_time)s, %(estimated_time)s, %(delivery_fee)s, %(vehicle_type)s)
            """, data)

        connection.commit()
        print(f"Data inserted into {table} successfully!")
    except mysql.connector.Error as err:
        print(f"Error inserting data into {table}: {err}")

if __name__ == "__main__":
    conn = create_connection()
    if conn:
        create_tables(conn)
        customers, restaurants, orders, order_items, delivery_persons, deliveries = generate_fake_data(conn)
        insert_data(conn, 'Customers', customers)
        insert_data(conn, 'Restaurants', restaurants)
        insert_data(conn, 'Orders', orders)
        insert_data(conn, 'OrderItems', order_items)
        insert_data(conn, 'DeliveryPersons', delivery_persons)
        insert_data(conn, 'Deliveries', deliveries)
        conn.close()
        print("Database setup and data insertion completed!")
