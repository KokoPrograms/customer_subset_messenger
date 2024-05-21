import sqlite3
import pandas as pd
import streamlit as st

def query_database(sql_query, params=None):
    """Execute an SQL query and return the result as a DataFrame."""
    try:
        with sqlite3.connect('customer_sales.db') as conn:
            df = pd.read_sql_query(sql_query, conn, params=params)
        return df
    except Exception as e:
        st.error(f"An error occurred while executing the SQL query: {e}")
        return pd.DataFrame()

def execute_aggregate_query(sql_query, column_name, params=None):
    """Execute an aggregate SQL query and return the result."""
    df = query_database(sql_query, params)
    return df[column_name][0] if not df.empty else 0

def format_date(date):
    """Format a date to a readable string."""
    return pd.to_datetime(date).strftime('%Y-%m-%d')

def get_customer_sales_history(customer_id):
    """Retrieve the sales history for a specific customer."""
    sql_query = """
    SELECT o.OrderID, o.OrderDate, o.TotalAmount, o.SalesChannel, 
           oi.ItemID, oi.Quantity, oi.UnitPrice, oi.TotalItemPrice, 
           p.Description, p.Category
    FROM Orders o
    JOIN OrderItems oi ON o.OrderID = oi.OrderID
    JOIN Products p ON oi.ItemID = p.ItemID
    WHERE o.CustomerID = ?
    """
    sales_history = query_database(sql_query, params=(customer_id,))
    
    # Calculate additional details
    total_spent = sales_history['TotalItemPrice'].sum()
    first_order_date = format_date(sales_history['OrderDate'].min())
    most_recent_order_date = format_date(sales_history['OrderDate'].max())
    
    return sales_history, total_spent, first_order_date, most_recent_order_date

def calculate_total_sales():
    """Calculate the total sales for all customers."""
    sql_query = """
    SELECT SUM(oi.TotalItemPrice) AS TotalSales
    FROM OrderItems oi
    """
    return execute_aggregate_query(sql_query, 'TotalSales')

def calculate_total_orders():
    """Calculate the total number of orders."""
    sql_query = """
    SELECT COUNT(OrderID) AS TotalOrders
    FROM Orders
    """
    return execute_aggregate_query(sql_query, 'TotalOrders')

def calculate_total_averages():
    """Calculate the total average order value and average items per order."""
    sql_query = """
    SELECT AVG(TotalAmount) AS AvgOrderValue, AVG(TotalItems) AS AvgItemsPerOrder
    FROM (
        SELECT o.TotalAmount, SUM(oi.Quantity) AS TotalItems
        FROM Orders o
        JOIN OrderItems oi ON o.OrderID = oi.OrderID
        GROUP BY o.OrderID
    )
    """
    averages_df = query_database(sql_query)
    avg_order_value = averages_df['AvgOrderValue'][0] if not averages_df.empty else 0
    avg_items_per_order = averages_df['AvgItemsPerOrder'][0] if not averages_df.empty else 0
    return avg_order_value, avg_items_per_order

def get_total_sales_history():
    """Retrieve the complete sales history."""
    sql_query = """
    SELECT o.OrderID, o.OrderDate, o.TotalAmount, o.SalesChannel, 
           oi.ItemID, oi.Quantity, oi.UnitPrice, oi.TotalItemPrice, 
           p.Description, p.Category
    FROM Orders o
    JOIN OrderItems oi ON o.OrderID = oi.OrderID
    JOIN Products p ON oi.ItemID = p.ItemID
    """
    sales_history_df = query_database(sql_query)
    sales_history_df['OrderDate'] = pd.to_datetime(sales_history_df['OrderDate'])
    return sales_history_df

def calculate_subset_sales(customers_data):
    """Calculate the total sales for a subset of customers."""
    if customers_data.empty:
        return None
    
    customer_ids = tuple(customers_data['CustomerID'])
    placeholders = ','.join('?' for _ in customer_ids)
    sql_query = f"""
    SELECT SUM(oi.TotalItemPrice) AS SubsetSales
    FROM Orders o
    JOIN OrderItems oi ON o.OrderID = oi.OrderID
    WHERE o.CustomerID IN ({placeholders})
    """
    return execute_aggregate_query(sql_query, 'SubsetSales', params=customer_ids)

def get_subset_sales_history(customers_data):
    """Retrieve the sales history for a subset of customers."""
    if customers_data.empty:
        return pd.DataFrame()  # Return an empty DataFrame if no customers found

    customer_ids = tuple(customers_data['CustomerID'])
    placeholders = ','.join('?' for _ in customer_ids)
    sql_query = f"""
    SELECT o.OrderID, o.OrderDate, o.TotalAmount, o.SalesChannel, 
           oi.ItemID, oi.Quantity, oi.UnitPrice, oi.TotalItemPrice, 
           p.Description, p.Category, o.CustomerID
    FROM Orders o
    JOIN OrderItems oi ON o.OrderID = oi.OrderID
    JOIN Products p ON oi.ItemID = p.ItemID
    WHERE o.CustomerID IN ({placeholders})
    """
    sales_history = query_database(sql_query, params=customer_ids)
    sales_history['OrderDate'] = pd.to_datetime(sales_history['OrderDate'])  # Convert to datetime
    return sales_history
