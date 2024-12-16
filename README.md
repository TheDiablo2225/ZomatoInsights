# ZomatoInsights
A management tool which incorporating machine learning insights

##File Overview
The encapsulated_streamlit_app.py contains the main code for the project encapsulated with classes and the streamlit_app1.py is just a non-encapsulated version of the same code. dbsetup3.py contains the code for DDL for the tables and also the DML whose data is generated using the faker library. This file is used to create tables and insert the records into them.

##Project Documentation
The Zomato Database Management and Insights Tool is a Streamlit-based web application designed to facilitate efficient database management, querying, and insights generation for a Zomato-style restaurant management system. The app interacts with a MySQL database to perform various tasks such as adding, updating, and deleting records, as well as providing visual insights into the database using interactive charts and graphs.

Features
1. Database Management
Add Records: Allows users to insert new records into the selected table by specifying column values.
Update Records: Provides an interface to update existing records based on a condition column.
Delete Records: Allows users to delete records from a selected table based on a condition column.
Create Tables: Enables the creation of new tables by specifying the table name and columns.
Add Columns: Allows the addition of new columns to an existing table.
2. Data Insights
The application generates various insights related to orders, customers, deliveries, and restaurants. These insights are displayed in the form of interactive charts using Plotly.

Order Management Insights:
Peak Ordering Times: Visualizes the distribution of orders over different hours of the day to identify peak ordering times.
Delayed Deliveries: Displays all deliveries where the delivery_time exceeded the estimated_time.
Customer Analytics:
Top Customers: Lists the top 5 customers based on the total number of orders.
Customer Preferences: Analyzes and displays the most ordered items by customers.
Delivery Optimization:
Delivery Times and Delays: Shows a histogram of delivery delays, calculated as the difference between delivery_time and estimated_time.
Restaurant Insights:
Most Popular Restaurants: Displays the restaurants with the most orders in descending order.
Database Structure
The tool operates on a MySQL database (zomato1) with multiple tables related to orders, customers, restaurants, and deliveries. These tables are dynamically fetched from the database, allowing users to interact with any table present in the system.

Key Tables:
orders: Contains order-related information, including order_time, restaurant_id, and customer_id.
customers: Contains customer details like name, total_orders, etc.
restaurants: Stores restaurant data, such as name and restaurant_id.
deliveries: Contains data regarding the delivery_time, estimated_time, and delivery status.
Application Workflow
Initialization:
Upon starting the app, a connection to the MySQL database is established.
The user is presented with options via the sidebar to choose between database management or data insights.
Dynamic fetching of table names and columns from the database allows the user to interact with the existing schema.
Database Management:
Users can interact with any table in the database to:
Add a new record: Input values for all columns in the selected table.
Update existing records: Modify a record based on a condition column.
Delete a record: Remove a record based on a condition column.
Create a new table: Define a new table with specified columns.
Add a new column: Add a column to an existing table.
Data Insights:
Users can select various options related to Order Management, Customer Analytics, Delivery Optimization, and Restaurant Insights.
Interactive charts (using Plotly) are displayed for the selected insights, with options to view data in graphical or tabular form.
Technologies Used
Streamlit: For building the interactive web application.
MySQL: For database management.
Plotly: For generating interactive charts and graphs.
pandas: For handling dataframes and easy data manipulation.
faker: To generate the dataset.
