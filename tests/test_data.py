import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

def load_data(table_name):
    """Load data from a specific table."""
    # Get the path to the top-level directory
    top_level_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    db_path = os.path.join(top_level_dir, 'customer_sales.db')
    
    # Connect to the database
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f'SELECT * FROM {table_name}', conn)
    conn.close()
    return df

def print_summary_statistics(df, table_name):
    """Print summary statistics of the data."""
    print(f"\nSummary statistics for {table_name} table:")
    print(df.describe())

def print_sample_data(df, table_name, num_samples=20):
    """Print a sample of data from the table."""
    print(f"\nSample data from {table_name} table:")
    print(df.head(num_samples))

def validate_average_items_per_order(df_order_items):
    """Validate the average items per order calculation."""
    items_per_order = df_order_items.groupby('OrderID')['Quantity'].sum()
    
    avg_items_per_order = items_per_order.mean()
    median_items_per_order = items_per_order.median()
    total_quantity = df_order_items['Quantity'].sum()
    total_orders = df_order_items['OrderID'].nunique()
    calculated_avg_items_per_order = total_quantity / total_orders
    
    print(f"\nCalculated Average Items per Order (mean): {avg_items_per_order}")
    print(f"Calculated Average Items per Order (median): {median_items_per_order}")
    print(f"Total Quantity: {total_quantity}")
    print(f"Total Orders: {total_orders}")
    print(f"Recalculated Average Items per Order: {calculated_avg_items_per_order}")

def validate_total_sales(df_order_items):
    """Validate the total sales calculation."""
    total_sales = df_order_items['TotalItemPrice'].sum()
    print(f"\nTotal Sales: ${total_sales:.2f}")

def validate_total_orders(df_orders):
    """Validate the total orders calculation."""
    total_orders = df_orders['OrderID'].nunique()
    print(f"\nTotal Orders: {total_orders}")

def plot_items_per_order_distribution(df_order_items):
    """Plot a histogram of the distribution of items per order."""
    items_per_order = df_order_items.groupby('OrderID')['Quantity'].sum()

    # Plot histogram
    plt.hist(items_per_order, bins=50)
    plt.xlabel('Items per Order')
    plt.ylabel('Frequency')
    plt.title('Distribution of Items per Order')
    plt.show()

if __name__ == "__main__":
    tables = ['Customers', 'Orders', 'OrderItems', 'Products']
    for table in tables:
        df = load_data(table)
        print_summary_statistics(df, table)
        print_sample_data(df, table)

    df_order_items = load_data('OrderItems')
    validate_average_items_per_order(df_order_items)
    validate_total_sales(df_order_items)

    df_orders = load_data('Orders')
    validate_total_orders(df_orders)

    plot_items_per_order_distribution(df_order_items)
