import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Configuration
num_customers = 2000
num_products = 43  # Updated to reflect the new product list
num_orders = 8000
num_order_items = 16000

# Generate customers
customers = []
customer_patterns = {
    'Regular': 0.3,  # 30% regular customers
    'Occasional': 0.4,  # 40% occasional customers
    'Bulk': 0.2,  # 20% bulk buyers
    'Seasonal': 0.1  # 10% seasonal buyers
}

for customer_id in range(1, num_customers + 1):
    pattern = random.choices(list(customer_patterns.keys()), list(customer_patterns.values()))[0]
    customer = {
        'CustomerID': customer_id,
        'Name': fake.name(),
        'Phone': fake.phone_number(),
        'Pattern': pattern
    }
    customers.append(customer)

df_customers = pd.DataFrame(customers)
df_customers.to_csv('data/customers.csv', index=False)

# Load products from 'data/products.csv'
df_products = pd.read_csv('data/products.csv')

# Define product popularity
popular_products = random.sample(list(df_products['ItemID']), k=int(num_products * 0.2))

# Helper functions for generating orders based on customer patterns
def generate_order_date(pattern):
    now = datetime.now()
    one_year_ago = now - timedelta(days=365)
    if pattern == 'Regular':
        return fake.date_time_between(start_date=one_year_ago, end_date=now)
    elif pattern == 'Occasional':
        return fake.date_time_between(start_date=one_year_ago, end_date=now)
    elif pattern == 'Bulk':
        return fake.date_time_between(start_date=one_year_ago, end_date=now)
    elif pattern == 'Seasonal':
        # Increase likelihood of orders during the holiday season
        holiday_start = datetime(now.year - 1, 11, 1)
        holiday_end = datetime(now.year - 1, 12, 31)
        if random.random() < 0.7:
            return fake.date_time_between(start_date=holiday_start, end_date=holiday_end)
        else:
            return fake.date_time_between(start_date=one_year_ago, end_date=now)

def generate_num_items(pattern):
    if pattern == 'Regular':
        return random.randint(1, 3)
    elif pattern == 'Occasional':
        return random.randint(1, 2)
    elif pattern == 'Bulk':
        return random.randint(5, 10)
    elif pattern == 'Seasonal':
        return random.randint(1, 5)

def generate_sales_channel(pattern):
    if pattern == 'Regular':
        return random.choice(['Store', 'Market'])
    elif pattern == 'Occasional':
        return random.choice(['Store', 'Market', 'Catering'])
    elif pattern == 'Bulk':
        return 'Catering'
    elif pattern == 'Seasonal':
        return random.choice(['Store', 'Market'])

def adjust_catering_order(order_items, total_amount):
    if total_amount < 100:
        deficit = 100 - total_amount
        while deficit > 0:
            item_id = random.choice(df_products['ItemID'])
            product = df_products[df_products['ItemID'] == item_id].iloc[0]
            quantity = random.randint(1, 5)
            unit_price = product['RegularPrice']
            total_item_price = quantity * unit_price

            order_item = {
                'OrderID': order_items[0]['OrderID'],
                'ItemID': item_id,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'TotalItemPrice': total_item_price
            }
            order_items.append(order_item)
            total_amount += total_item_price
            deficit -= total_item_price
    return order_items, total_amount

# Generate orders
orders = []
order_items = []

# Ensure every customer has at least one order
for customer in customers:
    order_id = len(orders) + 1001
    customer_id = customer['CustomerID']
    pattern = customer['Pattern']
    order_date = generate_order_date(pattern)
    sales_channel = generate_sales_channel(pattern)
    total_amount = 0.0

    order = {
        'OrderID': order_id,
        'CustomerID': customer_id,
        'OrderDate': order_date,
        'TotalAmount': 0,  # This will be updated later
        'SalesChannel': sales_channel
    }
    orders.append(order)

    # Generate order items for this order
    num_items = generate_num_items(pattern)
    for _ in range(num_items):
        item_id = random.choice(df_products['ItemID'])
        product = df_products[df_products['ItemID'] == item_id].iloc[0]
        quantity = random.randint(1, 10)
        unit_price = product['RegularPrice']
        total_item_price = quantity * unit_price

        order_item = {
            'OrderID': order_id,
            'ItemID': item_id,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'TotalItemPrice': total_item_price
        }
        order_items.append(order_item)

        # Update total amount for the order
        total_amount += total_item_price

    # Adjust catering orders to have a minimum of $100
    if sales_channel == 'Catering':
        order_items, total_amount = adjust_catering_order(order_items, total_amount)

    # Update the order's total amount
    orders[-1]['TotalAmount'] = round(total_amount, 2)

# Generate additional orders
for _ in range(num_orders - num_customers):
    order_id = len(orders) + 1001
    customer = random.choice(customers)
    customer_id = customer['CustomerID']
    pattern = customer['Pattern']
    order_date = generate_order_date(pattern)
    sales_channel = generate_sales_channel(pattern)
    total_amount = 0.0

    order = {
        'OrderID': order_id,
        'CustomerID': customer_id,
        'OrderDate': order_date,
        'TotalAmount': 0,  # This will be updated later
        'SalesChannel': sales_channel
    }
    orders.append(order)

    # Generate order items for this order
    num_items = generate_num_items(pattern)
    for _ in range(num_items):
        item_id = random.choice(df_products['ItemID'])
        product = df_products[df_products['ItemID'] == item_id].iloc[0]
        quantity = random.randint(1, 10)
        unit_price = product['RegularPrice']
        total_item_price = quantity * unit_price

        order_item = {
            'OrderID': order_id,
            'ItemID': item_id,
            'Quantity': quantity,
            'UnitPrice': unit_price,
            'TotalItemPrice': total_item_price
        }
        order_items.append(order_item)

        # Update total amount for the order
        total_amount += total_item_price

    # Adjust catering orders to have a minimum of $100
    if sales_channel == 'Catering':
        order_items, total_amount = adjust_catering_order(order_items, total_amount)

    # Update the order's total amount
    orders[-1]['TotalAmount'] = round(total_amount, 2)

df_orders = pd.DataFrame(orders)
df_orders.to_csv('data/orders.csv', index=False)

df_order_items = pd.DataFrame(order_items)
df_order_items.to_csv('data/order_items.csv', index=False)

print("Customers, orders, and order items CSV files have been created successfully!")
