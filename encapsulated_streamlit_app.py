import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
import plotly.express as px

class ZomatoApp:
    def __init__(self):
        self.connection = None

    # Function to connect to the MySQL database
    def create_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mysql",
                database="zomato1"
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            st.error(f"Error: {e}")
            return None

    # Function to execute a query
    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            st.error(f"Error: {e}")
            return False

    # Function to fetch data from the database
    def fetch_data(self, query):
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            st.error(f"Error: {e}")
            return None

    # Function to fetch table names dynamically
    def fetch_table_names(self):
        query = "SHOW TABLES"
        result = self.fetch_data(query)
        if result:
            return [list(table.values())[0] for table in result]
        return []

    # Function to fetch table columns
    def fetch_table_columns(self, table_name):
        query = f"SHOW COLUMNS FROM {table_name}"
        result = self.fetch_data(query)
        if result:
            return [col['Field'] for col in result]
        return []

    # Function to generate peak order times
    def get_peak_order_times(self):
        query = "SELECT HOUR(order_time) AS order_hour, COUNT(*) AS total_orders FROM orders GROUP BY order_hour ORDER BY order_hour;"
        return self.fetch_data(query)

    # Function to fetch delayed deliveries
    def get_delayed_deliveries(self):
        query = "SELECT * FROM deliveries WHERE delivery_time > estimated_time;"
        return self.fetch_data(query)

    # Function to fetch top customers
    def get_top_customers(self):
        query = "SELECT name, total_orders FROM customers ORDER BY total_orders DESC LIMIT 5;"
        return self.fetch_data(query)

    # Function to get customer preferences (Customer Analytics)
    def get_customer_preferences(self):
        query = """
            SELECT customer_id, item_name, COUNT(*) AS frequency
            FROM orders
            JOIN order_items ON orders.order_id = order_items.order_id
            GROUP BY customer_id, item_name
            ORDER BY frequency DESC;
        """
        return self.fetch_data(query)

    # Function to get delivery times and delays (Delivery Optimization)
    def get_delivery_times(self):
        query = """
        SELECT delivery_time, estimated_time, 
               (delivery_time - estimated_time) AS delay
        FROM deliveries;
    """
        return self.fetch_data(query)

    # Function to get most popular restaurants (Restaurant Insights)
    def get_popular_restaurants(self):
        query = """
            SELECT r.name, COUNT(o.order_id) AS total_orders
            FROM restaurants r
            JOIN orders o ON r.restaurant_id = o.restaurant_id
            GROUP BY r.name
            ORDER BY total_orders DESC
            LIMIT 5;
        """
        return self.fetch_data(query)

    def main(self):
        st.title("Zomato Management and Insights Tool")

        # Database connection
        self.create_connection()
        if not self.connection:
            st.stop()

        # Sidebar options
        action = st.sidebar.selectbox(
            "Select an action:",
            ["Add Record", "Update Record", "Delete Record", "Create Table", "Add Column", "View Records", "Data Insights"]
        )

        # Fetch table names dynamically
        table_names = self.fetch_table_names()

        # Add Record
        if action == "Add Record":
            table_name = st.selectbox("Select the table:", table_names)
            if table_name:
                columns = self.fetch_table_columns(table_name)
                form_data = {col: st.text_input(f"Enter value for {col}:") for col in columns}

                if st.button("Insert Record"):
                    keys = ", ".join(form_data.keys())
                    values = ", ".join(["%s"] * len(form_data))
                    insert_query = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"
                    if self.execute_query(insert_query, tuple(form_data.values())):
                        st.success("Record added successfully!")

        # Update Record
        elif action == "Update Record":
            table_name = st.selectbox("Select the table to update:", table_names)
            if table_name:
                columns = self.fetch_table_columns(table_name)
                condition_column = st.selectbox("Select condition column:", columns)
                condition_value = st.text_input(f"Enter value for {condition_column} (condition):")
                update_column = st.selectbox("Select column to update:", columns)
                new_value = st.text_input(f"Enter new value for {update_column}:")

                if st.button("Update Record"):
                    update_query = f"UPDATE {table_name} SET {update_column} = %s WHERE {condition_column} = %s"
                    if self.execute_query(update_query, (new_value, condition_value)):
                        st.success("Record updated successfully!")

        # Delete Record
        elif action == "Delete Record":
            table_name = st.selectbox("Select the table to delete from:", table_names)
            if table_name:
                columns = self.fetch_table_columns(table_name)
                condition_column = st.selectbox("Select condition column:", columns)
                condition_value = st.text_input(f"Enter value for {condition_column} (condition):")

                if st.button("Delete Record"):
                    delete_query = f"DELETE FROM {table_name} WHERE {condition_column} = %s"
                    if self.execute_query(delete_query, (condition_value,)):
                        st.success("Record deleted successfully!")

        # Create Table
        elif action == "Create Table":
            table_name = st.text_input("Enter the new table name:")
            columns = st.text_area("Define columns (e.g., id INT PRIMARY KEY, name VARCHAR(50)):")
            if st.button("Create Table"):
                create_query = f"CREATE TABLE {table_name} ({columns})"
                if self.execute_query(create_query):
                    st.success(f"Table '{table_name}' created successfully!")

        # Add Column
        elif action == "Add Column":
            table_name = st.selectbox("Select the table:", table_names)
            if table_name:
                column_name = st.text_input("Enter the new column name:")
                column_type = st.text_input("Enter the column type (e.g., VARCHAR(50), INT):")
                if st.button("Add Column"):
                    add_query = f"ALTER TABLE {table_name} ADD {column_name} {column_type}"
                    if self.execute_query(add_query):
                        st.success(f"Column '{column_name}' added successfully to table '{table_name}'!")

        # View Records
        elif action == "View Records":
            table_name = st.selectbox("Select the table:", table_names)
            if table_name:
                records = self.fetch_data(f"SELECT * FROM {table_name}")
                if records:
                    st.write(pd.DataFrame(records))
                else:
                    st.info("No records found in the table.")

        # Data Insights
        elif action == "Data Insights":
            st.subheader("Data Insights")
            insight_option = st.selectbox("Select an insight to view:", [
                "Order Management",
                "Customer Analytics",
                "Delivery Optimization",
                "Restaurant Insights"
            ])

            # Order Management Insights
            if insight_option == "Order Management":
                order_suboption = st.selectbox("Select Order Insight:", ["Peak Ordering Times", "Delayed Deliveries"])

                if order_suboption == "Peak Ordering Times":
                    data = self.get_peak_order_times()
                    if data:
                        df = pd.DataFrame(data)
                        st.write("### Peak Ordering Times")
                        fig = px.bar(df, x="order_hour", y="total_orders", title="Peak Order Times", labels={"order_hour": "Hour of Day", "total_orders": "Number of Orders"})
                        st.plotly_chart(fig)
                    else:
                        st.info("No data available for peak order times.")

                elif order_suboption == "Delayed Deliveries":
                    data = self.get_delayed_deliveries()
                    if data:
                        st.write("### Delayed Deliveries")
                        st.dataframe(pd.DataFrame(data))
                    else:
                        st.info("No delayed deliveries found.")

            # Customer Analytics Insights
            elif insight_option == "Customer Analytics":
                customer_suboption = st.selectbox("Select Customer Insight:", ["Top Customers", "Customer Preferences"])

                if customer_suboption == "Top Customers":
                    data = self.get_top_customers()
                    if data:
                        df = pd.DataFrame(data)
                        st.write("### Top Customers")
                        fig = px.bar(df, x="name", y="total_orders", title="Top Customers by Total Orders", labels={"name": "Customer Name", "total_orders": "Total Orders"})
                        st.plotly_chart(fig)
                    else:
                        st.info("No data available for top customers.")

                elif customer_suboption == "Customer Preferences":
                    data = self.get_customer_preferences()
                    if data:
                        df = pd.DataFrame(data)
                        st.write("### Customer Preferences (Most Ordered Items)")
                        fig = px.bar(df, x="item_name", y="frequency", title="Most Ordered Items by Customers", labels={"item_name": "Item", "frequency": "Frequency"})
                        st.plotly_chart(fig)
                    else:
                        st.info("No data available for customer preferences.")

            # Delivery Optimization Insights
            elif insight_option == "Delivery Optimization":
                delivery_suboption = st.selectbox("Select Delivery Insight:", ["Delivery Times and Delays"])

                if delivery_suboption == "Delivery Times and Delays":
                    data = self.get_delivery_times()
                    if data:
                        df = pd.DataFrame(data)
                        st.write("### Delivery Times and Delays")
                        fig = px.histogram(df, x="delay", title="Delivery Time Delays", labels={"delay": "Delay in Minutes"})
                        st.plotly_chart(fig)
                    else:
                        st.info("No data available for delivery delays.")

            # Restaurant Insights
            elif insight_option == "Restaurant Insights":
                restaurant_suboption = st.selectbox("Select Restaurant Insight:", ["Most Popular Restaurants"])

                if restaurant_suboption == "Most Popular Restaurants":
                    data = self.get_popular_restaurants()
                    if data:
                        df = pd.DataFrame(data)
                        st.write("### Most Popular Restaurants")
                        fig = px.bar(df, x="name", y="total_orders", title="Most Popular Restaurants", labels={"name": "Restaurant", "total_orders": "Total Orders"})
                        st.plotly_chart(fig)
                    else:
                        st.info("No data available for popular restaurants.")

        # Close connection
        self.connection.close()

if __name__ == "__main__":
    app = ZomatoApp()
    app.main()
