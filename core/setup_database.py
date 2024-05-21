import sqlite3
import pandas as pd
import streamlit as st
from core.query_database import calculate_total_sales, calculate_total_orders, calculate_total_averages, get_total_sales_history

def drop_existing_tables(cursor):
    """Drop existing tables if they exist."""
    tables = ['Customers', 'Orders', 'OrderItems', 'Products']
    for table in tables:
        cursor.execute(f'DROP TABLE IF EXISTS {table}')

def create_tables(cursor):
    """Create database tables."""
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customers (
        CustomerID INTEGER PRIMARY KEY,
        Name TEXT,
        Phone TEXT
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID INTEGER PRIMARY KEY,
        CustomerID INTEGER,
        OrderDate TEXT,
        TotalAmount REAL,
        SalesChannel TEXT,
        FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS OrderItems (
        OrderID INTEGER,
        ItemID INTEGER,
        Quantity INTEGER,
        UnitPrice REAL,
        TotalItemPrice REAL,
        PRIMARY KEY (OrderID, ItemID),
        FOREIGN KEY (OrderID) REFERENCES Orders (OrderID),
        FOREIGN KEY (ItemID) REFERENCES Products (ItemID)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products (
        ItemID INTEGER PRIMARY KEY,
        Description TEXT,
        Category TEXT,
        RegularPrice REAL,
        CateringPrice REAL
    )
    ''')

def load_data_from_csv():
    """Load data from CSV files into DataFrames."""
    df_customers = pd.read_csv('data/customers.csv')
    df_orders = pd.read_csv('data/orders.csv', parse_dates=['OrderDate'])
    df_order_items = pd.read_csv('data/order_items.csv')
    df_products = pd.read_csv('data/products.csv')
    return df_customers, df_orders, df_order_items, df_products

def insert_data_into_tables(conn, df_customers, df_orders, df_order_items, df_products):
    """Insert data into database tables."""
    df_customers.to_sql('Customers', conn, if_exists='replace', index=False)
    df_orders.to_sql('Orders', conn, if_exists='replace', index=False)
    df_order_items.to_sql('OrderItems', conn, if_exists='replace', index=False)
    df_products.to_sql('Products', conn, if_exists='replace', index=False)

def setup_database():
    """Set up the customer sales database."""
    with sqlite3.connect('customer_sales.db') as conn:
        cursor = conn.cursor()
        drop_existing_tables(cursor)
        create_tables(cursor)

        df_customers, df_orders, df_order_items, df_products = load_data_from_csv()
        insert_data_into_tables(conn, df_customers, df_orders, df_order_items, df_products)

        # Store the initial data into session state
        st.session_state['total_customers'] = len(df_customers)
        st.session_state['total_sales'] = calculate_total_sales()
        st.session_state['total_orders'] = calculate_total_orders()
        avg_order_value, avg_items_per_order = calculate_total_averages()
        st.session_state['avg_order_value'] = avg_order_value
        st.session_state['avg_items_per_order'] = avg_items_per_order
        st.session_state['sales_history'] = get_total_sales_history()

        conn.commit()
